#type:ignore
# backend/routes/escalation.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from backend.models.schemas import (
    EscalationEvent,
    EscalationTrigger,
    EscalationAction,
    Escalation,
)

router = APIRouter(prefix="/escalate", tags=["Escalation"])


# ─────────────────────────────────────────────
# REQUEST SCHEMA
# ─────────────────────────────────────────────

class EscalationCheckRequest(BaseModel):
    user_id: str
    force_level: str | None = None      # optional override for testing


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

# Keywords that immediately trigger Layer 1 escalation
_CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm",
    "want to die", "no point living", "hurt myself",
]

def _keyword_check(text: str) -> bool:
    lowered = text.lower()
    return any(kw in lowered for kw in _CRISIS_KEYWORDS)

def _evaluate_layers(user_id: str, sm) -> Escalation:
    """
    4-layer escalation evaluation.
    Escalates if 2 or more layers agree.

    Layer 1 — Keyword detection        (hard rules)
    Layer 2 — CSI threshold breach     (> 0.75)
    Layer 3 — Behavioral anomaly       (typing_irregularity > 0.7)
    Layer 4 — Trend-based risk         (risk > 0.80)
    """
    history = sm.get_history(user_id)
    if not history:
        return Escalation(triggered=False, level="low", reason=None)

    latest  = history[-1]
    session = sm.get_userID(user_id).get("session")

    layers_triggered = []

    # Layer 1 — Keywords
    last_text = session.text if session else ""
    if _keyword_check(last_text):
        layers_triggered.append("keyword")

    # Layer 2 — CSI threshold
    if latest.get("csi", 0.0) > 0.75:
        layers_triggered.append("risk")

    # Layer 3 — Behavioral anomaly (typing irregularity)
    features = latest.get("features", {})
    typing_irr = (
        features.get("typing_irregularity", 0.0)
        if isinstance(features, dict)
        else getattr(features, "typing_irregularity", 0.0)
    )
    if typing_irr > 0.70:
        layers_triggered.append("behavioral")

    # Layer 4 — Trend-based risk
    if latest.get("risk", 0.0) > 0.80:
        layers_triggered.append("risk")

    # Deduplicate
    layers_triggered = list(set(layers_triggered))

    # Escalate if 2+ layers agree
    if len(layers_triggered) >= 2:
        level  = "critical" if "keyword" in layers_triggered else "high"
        reason = "keyword" if "keyword" in layers_triggered else "risk"
        return Escalation(triggered=True, level=level, reason=reason)

    elif len(layers_triggered) == 1:
        return Escalation(triggered=True, level="medium", reason=layers_triggered[0])

    return Escalation(triggered=False, level="low", reason=None)


# ─────────────────────────────────────────────
# POST /escalate/check
# ─────────────────────────────────────────────

@router.post("/check", response_model=EscalationEvent)
async def check_escalation(body: EscalationCheckRequest, request: Request):
    """
    Runs 4-layer escalation evaluation for a user.
    Returns a full EscalationEvent if triggered.

    Layers:
        1. Keyword detection  (hard rules)
        2. CSI > 0.75         (threshold breach)
        3. Typing irregularity > 0.70 (behavioral anomaly)
        4. Risk > 0.80        (trend-based)

    Escalates if 2+ layers agree.
    """
    sm      = request.app.state.state_manager
    user_id = body.user_id

    if sm.get_userID(user_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"No session found for user '{user_id}'"
        )

    try:
        escalation = _evaluate_layers(user_id, sm)

        if not escalation.triggered:
            # Return a non-critical event — no storage needed
            history = sm.get_history(user_id)
            latest  = history[-1] if history else {}
            from backend.models.schemas import EscalationSignals
            return EscalationEvent(
                user_id=user_id,
                timestamp=latest.get("timestamp", __import__("datetime").datetime.utcnow()),
                trigger=EscalationTrigger(type="risk", details="No escalation triggered"),
                signals=EscalationSignals(
                    csi=latest.get("csi", 0.0),
                    risk=latest.get("risk", 0.0),
                    zscore=latest.get("zscore", 0.0),
                ),
                action=EscalationAction(
                    level="critical",
                    next_step="show_resources",
                ),
            )

        # Determine action based on level
        next_step = (
            "contact_support" if escalation.level == "critical"
            else "alert_contact" if escalation.level == "high"
            else "show_resources"
        )

        return sm.store_escalation(
            user_id=user_id,
            trigger=EscalationTrigger(
                type=(escalation.reason if escalation.reason in {"keyword", "risk"} else "combined"),
                details=f"Layers triggered: {escalation.level}",
            ),
            action=EscalationAction(
                level="critical",
                next_step=next_step,
            ),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# GET /escalate/history/{user_id}
# ─────────────────────────────────────────────

@router.get("/history/{user_id}", tags=["Escalation"])
async def get_escalation_history(user_id: str, request: Request):
    """
    Returns all past escalation events for a user.
    Useful for the dashboard's escalation log panel.
    """
    sm   = request.app.state.state_manager
    user = sm.get_userID(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

    escalations = user.get("escalations", [])
    return {"user_id": user_id, "count": len(escalations), "events": escalations}
