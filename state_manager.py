from datetime import datetime, timezone
from backend.models.schemas import (
    FrontendInputPayload,
    MLPipelineInput,
    MLPipelineOutput,
    FrontendResponsePayload,
    AnalysisSummary,
    EmotionSummary,
    DBLogEntry,
    DashboardPayload,
    DashboardHistoryEntry,
    DashboardAggregates,
    EscalationEvent,
    EscalationTrigger,
    EscalationSignals,
    EscalationAction,
    Intervention,
    Escalation,
    CSIHistoryEntry,
)


class StateManager:

    def __init__(self):
        # user_id → { session, history, escalations }
        self.store: dict[str, dict] = {}

    # ─────────────────────────────────────────────
    # INTERNAL
    # ─────────────────────────────────────────────

    def _init_user(self, user_id: str):
        if user_id not in self.store:
            self.store[user_id] = {
                "session":     None,   # FrontendInputPayload
                "history":     [],     # list[MLPipelineOutput + timestamp]
                "escalations": [],     # list[EscalationEvent]
            }

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    # ─────────────────────────────────────────────
    # 1. STORE FRONTEND INPUT
    # ─────────────────────────────────────────────

    def store_input(self, payload: FrontendInputPayload) -> FrontendInputPayload:
        """
        Validates and stores the incoming frontend payload.
        Returns the validated model.
        """
        self._init_user(payload.user_id)
        self.store[payload.user_id]["session"] = payload
        return payload

    # ─────────────────────────────────────────────
    # 2. BUILD ML PIPELINE INPUT
    # ─────────────────────────────────────────────

    def build_ml_input(self, user_id: str) -> MLPipelineInput:
        """
        Builds the ML pipeline input from current session + CSI history.
        """
        self._init_user(user_id)
        session: FrontendInputPayload = self.store[user_id]["session"]

        csi_history = [
            CSIHistoryEntry(csi=e["csi"], timestamp=e["timestamp"])
            for e in self.store[user_id]["history"]
        ]

        return MLPipelineInput(
            text=session.text,
            typing_metrics=session.typing_metrics,
            history=csi_history,
        )

    # ─────────────────────────────────────────────
    # 3. STORE ML OUTPUT
    # ─────────────────────────────────────────────

    def store_ml_output(self, user_id: str, ml_result: MLPipelineOutput) -> dict:
        """
        Saves the validated ML result into per-user history.
        """
        self._init_user(user_id)
        entry = {
            "timestamp": self._now(),
            **ml_result.model_dump(),
        }
        self.store[user_id]["history"].append(entry)
        return entry

    # ─────────────────────────────────────────────
    # 4. BUILD FRONTEND RESPONSE
    # ─────────────────────────────────────────────

    def build_frontend_response(
        self,
        user_id: str,
        intervention: Intervention,
        escalation: Escalation,
    ) -> FrontendResponsePayload:
        """
        Constructs the validated response sent back to the frontend.
        """
        self._init_user(user_id)
        latest = self.store[user_id]["history"][-1] if self.store[user_id]["history"] else {}

        analysis = AnalysisSummary(
            emotion=EmotionSummary(
                top_signals=latest.get("emotion", {}).get("top_signals", []),
                confidence=latest.get("emotion", {}).get("confidence", 0.0),
            ),
            csi=latest.get("csi", 0.0),
            zscore=latest.get("zscore", 0.0),
            risk=latest.get("risk", 0.0),
            state=latest.get("state", "normal"),
        )

        return FrontendResponsePayload(
            user_id=user_id,
            timestamp=latest.get("timestamp", self._now()),
            analysis=analysis,
            intervention=intervention,
            escalation=escalation,
        )

    # ─────────────────────────────────────────────
    # 5. DATABASE LOG ENTRY
    # ─────────────────────────────────────────────

    def get_db_log_entry(self, user_id: str) -> DBLogEntry:
        """
        Returns the latest entry as a validated DBLogEntry.
        """
        self._init_user(user_id)
        latest = self.store[user_id]["history"][-1] if self.store[user_id]["history"] else {}

        return DBLogEntry(
            user_id=user_id,
            timestamp=latest.get("timestamp", self._now()),
            csi=latest.get("csi", 0.0),
            risk=latest.get("risk", 0.0),
            state=latest.get("state", "normal"),
            features=latest.get("features", {}),
        )

    # ─────────────────────────────────────────────
    # 6. DASHBOARD PAYLOAD
    # ─────────────────────────────────────────────

    def get_dashboard_payload(self, user_id: str) -> DashboardPayload:
        """
        Returns full history + computed aggregates for the dashboard.
        """
        self._init_user(user_id)
        history = self.store[user_id]["history"]

        csi_values  = [e["csi"]  for e in history]
        risk_values = [e["risk"] for e in history]

        avg_csi  = sum(csi_values)  / len(csi_values)  if csi_values  else 0.0
        max_risk = max(risk_values)                     if risk_values else 0.0

        if len(csi_values) >= 2:
            trend = ("increasing" if csi_values[-1] > csi_values[-2]
                     else "decreasing" if csi_values[-1] < csi_values[-2]
                     else "stable")
        else:
            trend = "stable"

        return DashboardPayload(
            user_id=user_id,
            history=[
                DashboardHistoryEntry(
                    timestamp=e["timestamp"],
                    csi=e["csi"],
                    risk=e["risk"],
                    state=e["state"],
                )
                for e in history
            ],
            aggregates=DashboardAggregates(
                avg_csi=round(avg_csi, 4),
                max_risk=round(max_risk, 4),
                trend=trend,
            ),
        )

    # ─────────────────────────────────────────────
    # 7. ESCALATION EVENT
    # ─────────────────────────────────────────────

    def store_escalation(
        self,
        user_id: str,
        trigger: EscalationTrigger,
        action: EscalationAction,
    ) -> EscalationEvent:
        """
        Builds, stores, and returns a validated escalation event.
        """
        self._init_user(user_id)
        latest = self.store[user_id]["history"][-1] if self.store[user_id]["history"] else {}

        event = EscalationEvent(
            user_id=user_id,
            timestamp=self._now(),
            trigger=trigger,
            signals=EscalationSignals(
                csi=latest.get("csi", 0.0),
                risk=latest.get("risk", 0.0),
                zscore=latest.get("zscore", 0.0),
            ),
            action=action,
        )
        self.store[user_id]["escalations"].append(event)
        return event

    # ─────────────────────────────────────────────
    # GENERIC GETTERS (original API preserved)
    # ─────────────────────────────────────────────

    def get_history(self, user_id: str) -> list:
        return self.store.get(user_id, {}).get("history", [])

    def get_userID(self, user_id: str):
        return self.store.get(user_id)