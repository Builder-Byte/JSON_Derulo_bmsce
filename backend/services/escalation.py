# backend/services/escalation.py
#type:ignore
from models.schemas import (
    Escalation,
    EscalationEvent,
    EscalationTrigger,
    EscalationAction,
    EscalationSignals,
    MLPipelineOutput,
)
from datetime import datetime, timezone


# ─────────────────────────────────────────────
# THRESHOLDS (tune these per domain)
# ─────────────────────────────────────────────

CSI_THRESHOLD          = 0.75   # Layer 2
TYPING_IRR_THRESHOLD   = 0.70   # Layer 3
RISK_THRESHOLD         = 0.80   # Layer 4
ESCALATION_MIN_LAYERS  = 2      # layers that must agree to escalate


# ─────────────────────────────────────────────
# LAYER 1 — KEYWORD DETECTION
# ─────────────────────────────────────────────

_CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life",
    "self harm", "want to die", "no point living",
    "hurt myself", "can't go on", "not worth living",
]

def _layer1_keyword(text: str) -> bool:
    """Hard rule — any crisis keyword = immediate flag."""
    lowered = text.lower()
    return any(kw in lowered for kw in _CRISIS_KEYWORDS)


# ─────────────────────────────────────────────
# LAYER 2 — CSI THRESHOLD BREACH
# ─────────────────────────────────────────────

def _layer2_csi(ml_output: MLPipelineOutput) -> bool:
    """CSI above critical threshold."""
    return ml_output.csi > CSI_THRESHOLD


# ─────────────────────────────────────────────
# LAYER 3 — BEHAVIORAL ANOMALY
# ─────────────────────────────────────────────

def _layer3_behavioral(ml_output: MLPipelineOutput) -> bool:
    """
    Detects masked distress:
    High typing irregularity with positive/neutral sentiment
    is a strong signal of suppressed emotional state.
    """
    typing_irr      = ml_output.features.typing_irregularity
    top_signals     = ml_output.emotion.top_signals
    positive_labels = {"joy", "surprise", "neutral"}

    # High irregularity alone
    if typing_irr > TYPING_IRR_THRESHOLD:
        return True

    # Masking risk: positive emotion + high irregularity
    if typing_irr > 0.50 and all(s in positive_labels for s in top_signals):
        return True

    return False


# ─────────────────────────────────────────────
# LAYER 4 — TREND-BASED RISK
# ─────────────────────────────────────────────

def _layer4_risk(ml_output: MLPipelineOutput, history: list) -> bool:
    """
    Evaluates sustained risk over time.
    Triggers if:
        - Current risk > threshold, OR
        - Last 3 sessions all had elevated/high state (trend)
    """
    if ml_output.risk > RISK_THRESHOLD:
        return True

    # Trend check — last 3 sessions
    if len(history) >= 3:
        recent_states = [e.get("state", "normal") for e in history[-3:]]
        if all(s in {"elevated", "high"} for s in recent_states):
            return True

    return False


# ─────────────────────────────────────────────
# CORE ESCALATION EVALUATOR
# ─────────────────────────────────────────────

def evaluate(
    user_id: str,
    ml_output: MLPipelineOutput,
    last_text: str,
    history: list,
) -> Escalation:
    """
    Runs all 4 layers and returns an Escalation object.
    Escalates if ESCALATION_MIN_LAYERS (2+) agree.

    Args:
        user_id:    User identifier
        ml_output:  Latest MLPipelineOutput
        last_text:  Raw text from the user's latest message
        history:    Full session history from StateManager

    Returns:
        Escalation with triggered, level, reason
    """
    fired = {}

    fired["keyword"]    = _layer1_keyword(last_text)
    fired["csi"]        = _layer2_csi(ml_output)
    fired["behavioral"] = _layer3_behavioral(ml_output)
    fired["risk"]       = _layer4_risk(ml_output, history)

    triggered_layers = [k for k, v in fired.items() if v]
    count            = len(triggered_layers)

    # Keyword alone = immediate critical (override min layer rule)
    if fired["keyword"]:
        return Escalation(triggered=True, level="critical", reason="keyword")

    if count >= ESCALATION_MIN_LAYERS:
        level  = "critical" if count >= 3 else "high"
        reason = "risk" if "risk" in triggered_layers else "behavioral"
        return Escalation(triggered=True, level=level, reason=reason)

    if count == 1:
        return Escalation(triggered=True, level="medium", reason=triggered_layers[0])

    return Escalation(triggered=False, level="low", reason=None)


# ─────────────────────────────────────────────
# ESCALATION EVENT BUILDER
# ─────────────────────────────────────────────

def build_event(
    user_id: str,
    escalation: Escalation,
    ml_output: MLPipelineOutput,
) -> EscalationEvent:
    """
    Constructs a fully validated EscalationEvent from
    an Escalation result and the latest ML output.

    Args:
        user_id:    User identifier
        escalation: Result from evaluate()
        ml_output:  Latest MLPipelineOutput

    Returns:
        EscalationEvent ready to store or return to frontend
    """
    next_step = (
        "contact_support" if escalation.level == "critical"
        else "alert_contact" if escalation.level == "high"
        else "show_resources"
    )

    return EscalationEvent(
        user_id=user_id,
        timestamp=datetime.now(timezone.utc),
        trigger=EscalationTrigger(
            type=escalation.reason or "risk",
            details=f"Escalation level: {escalation.level}",
        ),
        signals=EscalationSignals(
            csi=ml_output.csi,
            risk=ml_output.risk,
            zscore=ml_output.zscore,
        ),
        action=EscalationAction(
            level="critical",
            next_step=next_step,
        ),
    )