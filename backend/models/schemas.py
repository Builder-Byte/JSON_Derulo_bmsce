from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# ─────────────────────────────────────────────
# SECTION 1 — Frontend → Backend (Primary Input)
# ─────────────────────────────────────────────

class TypingMetrics(BaseModel):
    speed: float
    backspaces: int
    latency: float
    pause_variance: float


class SessionMetadata(BaseModel):
    session_id: str
    device: Literal["web", "mobile"]
    local_time: str                         # "HH:MM"
    input_mode: Literal["text", "voice"]


class FrontendInputPayload(BaseModel):
    schema_version: str = "v1"
    user_id: str
    timestamp: datetime
    text: str
    audio_base64: Optional[str] = None
    typing_metrics: TypingMetrics
    session_metadata: SessionMetadata


# ─────────────────────────────────────────────
# SECTION 2 — Backend → ML Pipeline
# ─────────────────────────────────────────────

class CSIHistoryEntry(BaseModel):
    csi: float
    timestamp: datetime


class MLPipelineInput(BaseModel):
    text: str
    typing_metrics: TypingMetrics
    history: list[CSIHistoryEntry] = []


# ─────────────────────────────────────────────
# SECTION 3 — ML Pipeline Output (Raw Response)
# ─────────────────────────────────────────────

class EmotionScores(BaseModel):
    anger: float
    sadness: float
    fear: float
    joy: float
    disgust: float
    surprise: float
    neutral: float


class EmotionResult(BaseModel):
    scores: EmotionScores
    top_signals: list[str] = []
    confidence: float


class MLFeatures(BaseModel):
    negativity: float
    uncertainty: float
    typing_irregularity: float


class MLPipelineOutput(BaseModel):
    emotion: EmotionResult
    features: MLFeatures
    csi: float
    zscore: float
    risk: float
    state: Literal["normal", "elevated", "high"]


# ─────────────────────────────────────────────
# SECTION 4 — Backend → Frontend (Final Response)
# ─────────────────────────────────────────────

class EmotionSummary(BaseModel):
    top_signals: list[str]
    confidence: float


class AnalysisSummary(BaseModel):
    emotion: EmotionSummary
    csi: float
    zscore: float
    risk: float
    state: Literal["normal", "elevated", "high"]


class InterventionPayload(BaseModel):
    duration_sec: int
    prompt: str


class Intervention(BaseModel):
    type: Literal["breathing", "reflection", "none"]
    payload: Optional[InterventionPayload] = None


class Escalation(BaseModel):
    triggered: bool
    level: Literal["low", "medium", "high", "critical"]
    reason: Optional[Literal["keyword", "risk", "behavioral"]] = None


class FrontendResponsePayload(BaseModel):
    schema_version: str = "v1"
    user_id: str
    timestamp: datetime
    analysis: AnalysisSummary
    intervention: Intervention
    escalation: Escalation


# ─────────────────────────────────────────────
# SECTION 5 — Backend → Database (Log Format)
# ─────────────────────────────────────────────

class DBLogEntry(BaseModel):
    user_id: str
    timestamp: datetime
    csi: float
    risk: float
    state: str
    features: MLFeatures


# ─────────────────────────────────────────────
# SECTION 6 — Dashboard Response
# ─────────────────────────────────────────────

class DashboardHistoryEntry(BaseModel):
    timestamp: datetime
    csi: float
    risk: float
    state: str


class DashboardAggregates(BaseModel):
    avg_csi: float
    max_risk: float
    trend: Literal["increasing", "stable", "decreasing"]


class DashboardPayload(BaseModel):
    user_id: str
    history: list[DashboardHistoryEntry]
    aggregates: DashboardAggregates


# ─────────────────────────────────────────────
# SECTION 7 — Escalation Event (Critical Path)
# ─────────────────────────────────────────────

class EscalationTrigger(BaseModel):
    type: Literal["keyword", "risk", "combined"]
    details: str


class EscalationSignals(BaseModel):
    csi: float
    risk: float
    zscore: float


class EscalationAction(BaseModel):
    level: Literal["critical"]
    next_step: Literal["contact_support", "alert_contact", "show_resources"]


class EscalationEvent(BaseModel):
    user_id: str
    timestamp: datetime
    trigger: EscalationTrigger
    signals: EscalationSignals
    action: EscalationAction


# ─────────────────────────────────────────────
# SECTION 8 — Error Response
# ─────────────────────────────────────────────

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorDetail