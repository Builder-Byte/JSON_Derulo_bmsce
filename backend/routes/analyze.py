# backend/routes/analyze.py

from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime, timezone

from models.schemas import (
    FrontendInputPayload,
    FrontendResponsePayload,
    MLPipelineOutput,
    Intervention,
    InterventionPayload,
    Escalation,
)
from state_manager import StateManager
from services.ml_service import run_text_analysis, run_audio_analysis

router = APIRouter(prefix="/analyze", tags=["Analyze"])

# Shared state manager instance (import from main.py in production)
state_manager = StateManager()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def _build_intervention(ml_output: MLPipelineOutput) -> Intervention:
    """
    Maps CSI + state to an intervention type and prompt.
    """
    if ml_output.state == "high":
        return Intervention(
            type="breathing",
            payload=InterventionPayload(
                duration_sec=120,
                prompt="Let's pause. Take a slow breath in for 4 counts, hold for 4, out for 4.",
            ),
        )
    elif ml_output.state == "elevated":
        return Intervention(
            type="reflection",
            payload=InterventionPayload(
                duration_sec=60,
                prompt="You seem a little overwhelmed. Want to take a moment and reflect?",
            ),
        )
    else:
        return Intervention(type="none", payload=None)


def _build_escalation(ml_output: MLPipelineOutput) -> Escalation:
    """
    Simple threshold-based escalation for Phase 1.
    Replace with escalation_engine.py logic in Phase 5.
    """
    if ml_output.risk >= 0.85:
        return Escalation(triggered=True, level="critical", reason="risk")
    elif ml_output.risk >= 0.70:
        return Escalation(triggered=True, level="high", reason="risk")
    elif ml_output.risk >= 0.55:
        return Escalation(triggered=True, level="medium", reason="risk")
    else:
        return Escalation(triggered=False, level="low", reason=None)


def _log_to_db(user_id: str):
    """
    Background task — writes latest entry to DB.
    Plug storage.py here in Phase 2.
    """
    db_entry = state_manager.get_db_log_entry(user_id)
    # TODO: storage.save(db_entry)
    print(f"[DB LOG] {db_entry}")

@router.post("/text", response_model=FrontendResponsePayload)
async def analyze_text(
    payload: FrontendInputPayload,
    background_tasks: BackgroundTasks,
):
    """
    Core endpoint. Accepts frontend payload, runs ML analysis,
    computes intervention + escalation, returns enriched response.

    Flow:
        store_input → build_ml_input → run_text_analysis
        → store_ml_output → build_frontend_response
    """
    user_id = payload.user_id

    try:
        # 1 — Store raw frontend input
        state_manager.store_input(payload)

        # 2 — Build ML pipeline input from state
        ml_input = state_manager.build_ml_input(user_id)

        # 3 — Run ML (mock or real depending on USE_MOCK flag)
        ml_output = run_text_analysis(ml_input)

        # 4 — Persist ML output into user history
        state_manager.store_ml_output(user_id, ml_output)

        # 5 — Determine intervention + escalation
        intervention = _build_intervention(ml_output)
        escalation   = _build_escalation(ml_output)

        # 6 — Store escalation event if triggered
        if escalation.triggered:
            from models.schemas import EscalationTrigger, EscalationAction
            state_manager.store_escalation(
                user_id=user_id,
                trigger=EscalationTrigger(type="risk", details=f"risk={ml_output.risk}"),
                action=EscalationAction(level="critical", next_step="contact_support"),
            )

        # 7 — DB log in background (non-blocking)
        background_tasks.add_task(_log_to_db, user_id)

        # 8 — Build and return validated response
        return state_manager.build_frontend_response(user_id, intervention, escalation)

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# POST /analyze/audio
# ─────────────────────────────────────────────

@router.post("/audio", response_model=FrontendResponsePayload)
async def analyze_audio(
    payload: FrontendInputPayload,
    background_tasks: BackgroundTasks,
):
    """
    Audio analysis endpoint. Expects audio_base64 in the payload.
    Falls back to text analysis if audio is missing (Phase 1 safe).

    Flow:
        store_input → run_audio_analysis (or text fallback)
        → store_ml_output → build_frontend_response
    """
    user_id = payload.user_id

    try:
        # 1 — Store raw frontend input
        state_manager.store_input(payload)

        # 2 — Use audio if present, else fall back to text
        if payload.audio_base64:
            ml_output = run_audio_analysis(payload.audio_base64)
        else:
            ml_input  = state_manager.build_ml_input(user_id)
            ml_output = run_text_analysis(ml_input)

        # 3 — Persist ML output
        state_manager.store_ml_output(user_id, ml_output)

        # 4 — Intervention + escalation
        intervention = _build_intervention(ml_output)
        escalation   = _build_escalation(ml_output)

        # 5 — Background DB log
        background_tasks.add_task(_log_to_db, user_id)

        return state_manager.build_frontend_response(user_id, intervention, escalation)

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))