# backend/routes/dashboard.py

from fastapi import APIRouter, HTTPException, Request
from backend.models.schemas import DashboardPayload

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ─────────────────────────────────────────────
# GET /dashboard/{user_id}
# ─────────────────────────────────────────────

@router.get("/{user_id}", response_model=DashboardPayload)
async def get_dashboard(user_id: str, request: Request):
    """
    Returns full session history + aggregates for a given user.
    Used by the frontend dashboard to render CSI trend, risk chart,
    and state distribution.

    Response:
        DashboardPayload → history[], aggregates { avg_csi, max_risk, trend }
    """
    sm = request.app.state.state_manager

    user = sm.get_userID(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for user '{user_id}'"
        )

    history = sm.get_history(user_id)
    if not history:
        raise HTTPException(
            status_code=404,
            detail=f"No session history found for user '{user_id}'"
        )

    try:
        return sm.get_dashboard_payload(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
