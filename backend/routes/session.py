# backend/routes/session.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime, timezone

router = APIRouter(prefix="/session", tags=["Session"])


# ─────────────────────────────────────────────
# REQUEST SCHEMAS
# ─────────────────────────────────────────────

class SessionStartRequest(BaseModel):
    user_id: str
    session_id: str
    device: str = "web"
    input_mode: str = "text"
    local_time: str = ""            # "HH:MM" from frontend


class SessionEndRequest(BaseModel):
    user_id: str
    session_id: str


# ─────────────────────────────────────────────
# POST /session/start
# ─────────────────────────────────────────────

@router.post("/start", tags=["Session"])
async def start_session(body: SessionStartRequest, request: Request):
    """
    Initializes a new session for the user.
    Creates the user entry in StateManager if first time.

    Call this before sending any /analyze requests.
    """
    sm = request.app.state.state_manager

    # Initialize user slot in state manager
    sm._init_user(body.user_id)

    # Store lightweight session metadata
    sm.store[body.user_id]["session_meta"] = {
        "session_id":  body.session_id,
        "device":      body.device,
        "input_mode":  body.input_mode,
        "local_time":  body.local_time,
        "started_at":  datetime.now(timezone.utc).isoformat(),
        "ended_at":    None,
        "active":      True,
    }

    is_returning = len(sm.get_history(body.user_id)) > 0

    return {
        "status":        "session_started",
        "user_id":       body.user_id,
        "session_id":    body.session_id,
        "started_at":    sm.store[body.user_id]["session_meta"]["started_at"],
        "is_returning":  is_returning,
        "history_count": len(sm.get_history(body.user_id)),
    }


# ─────────────────────────────────────────────
# POST /session/end
# ─────────────────────────────────────────────

@router.post("/end", tags=["Session"])
async def end_session(body: SessionEndRequest, request: Request):
    """
    Closes the active session for the user.
    Records end time and marks session as inactive.
    Returns a session summary with final CSI + risk snapshot.
    """
    sm      = request.app.state.state_manager
    user_id = body.user_id

    user = sm.get_userID(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"No active session found for user '{user_id}'"
        )

    session_meta = user.get("session_meta", {})

    # Validate session ID matches
    if session_meta.get("session_id") != body.session_id:
        raise HTTPException(
            status_code=400,
            detail="session_id does not match the active session"
        )

    # Mark session as ended
    ended_at = datetime.now(timezone.utc).isoformat()
    sm.store[user_id]["session_meta"]["ended_at"] = ended_at
    sm.store[user_id]["session_meta"]["active"]   = False

    # Build snapshot from latest history entry
    history = sm.get_history(user_id)
    latest  = history[-1] if history else {}

    return {
        "status":      "session_ended",
        "user_id":     user_id,
        "session_id":  body.session_id,
        "started_at":  session_meta.get("started_at"),
        "ended_at":    ended_at,
        "summary": {
            "total_entries": len(history),
            "final_csi":     latest.get("csi",   0.0),
            "final_risk":    latest.get("risk",  0.0),
            "final_state":   latest.get("state", "normal"),
        },
    }


# ─────────────────────────────────────────────
# GET /session/status/{user_id}
# ─────────────────────────────────────────────

@router.get("/status/{user_id}", tags=["Session"])
async def session_status(user_id: str, request: Request):
    """
    Returns current session status for a user.
    Useful for frontend to check if a session is active on reconnect.
    """
    sm   = request.app.state.state_manager
    user = sm.get_userID(user_id)

    if user is None:
        return {"user_id": user_id, "active": False, "session_meta": None}

    return {
        "user_id":      user_id,
        "active":       user.get("session_meta", {}).get("active", False),
        "session_meta": user.get("session_meta"),
        "history_count": len(sm.get_history(user_id)),
    }