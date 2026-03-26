#type: ignore
# backend/services/ml_service.py
USE_MOCK = True

from models.schemas import (
    MLPipelineInput,
    MLPipelineOutput,
    EmotionResult,
    EmotionScores,
    MLFeatures,
)

if not USE_MOCK:
    try:
        from ml.emotion import analyze_text as _ml_analyze_text
        from ml.audio import analyze_audio as _ml_analyze_audio
        from ml.csi import compute_csi as _ml_compute_csi
        from ml.risk_model import compute_risk as _ml_compute_risk
    except ImportError as e:
        raise RuntimeError(
            f"USE_MOCK=False but ML modules are not available: {e}"
        )

_MOCK_EMOTION = EmotionResult(
    scores=EmotionScores(
        anger=0.05,
        sadness=0.50,
        fear=0.20,
        joy=0.05,
        disgust=0.05,
        surprise=0.05,
        neutral=0.10,
    ),
    top_signals=["sadness", "fear"],
    confidence=0.85,
)

_MOCK_FEATURES = MLFeatures(
    negativity=0.65,
    uncertainty=0.55,
    typing_irregularity=0.40,
)

_MOCK_OUTPUT = MLPipelineOutput(
    emotion=_MOCK_EMOTION,
    features=_MOCK_FEATURES,
    csi=0.62,
    zscore=1.75,
    risk=0.58,
    state="elevated",
)


def run_text_analysis(payload: MLPipelineInput) -> MLPipelineOutput:
    """
    Main entry point for text-based mental state analysis.
    Routes to mock or real ML depending on USE_MOCK flag.

    Args:
        payload: MLPipelineInput containing text, typing_metrics, history

    Returns:
        MLPipelineOutput with emotion, features, csi, zscore, risk, state
    """
    if USE_MOCK:
        return _mock_text_analysis(payload)
    return _real_text_analysis(payload)


def run_audio_analysis(audio_base64: str) -> MLPipelineOutput:
    """
    Entry point for audio-based analysis (Whisper + Wav2Vec2).
    Falls back to mock if USE_MOCK is True.

    Args:
        audio_base64: Base64-encoded audio string from frontend

    Returns:
        MLPipelineOutput
    """
    if USE_MOCK:
        return _MOCK_OUTPUT
    return _real_audio_analysis(audio_base64)


def _mock_text_analysis(payload: MLPipelineInput) -> MLPipelineOutput:
    """
    Returns hardcoded realistic output.
    Slightly varies csi/risk based on history length
    so the dashboard doesn't look completely flat.
    """
    history_len = len(payload.history)

    # Simulate slight drift as history grows
    csi   = min(0.95, 0.62 + history_len * 0.03)
    risk  = min(0.95, 0.58 + history_len * 0.02)
    state = (
        "high"     if csi > 0.75 else
        "elevated" if csi > 0.50 else
        "normal"
    )

    return MLPipelineOutput(
        emotion=_MOCK_EMOTION,
        features=_MOCK_FEATURES,
        csi=round(csi, 4),
        zscore=round(1.75 + history_len * 0.1, 4),
        risk=round(risk, 4),
        state=state,
    )



def _real_text_analysis(payload: MLPipelineInput) -> MLPipelineOutput:
    """
    Calls the actual ML modules once USE_MOCK = False.
    Expects ML layer to expose:
        analyze_text(text)            -> dict
        compute_csi(features, history) -> float
        compute_risk(history)          -> float
    """
    # Step 1 — Emotion + linguistic features
    raw_emotion = _ml_analyze_text(payload.text)

    # Step 2 — Fuse typing metrics into features
    features = MLFeatures(
        negativity=raw_emotion.get("negativity", 0.0),
        uncertainty=raw_emotion.get("uncertainty", 0.0),
        typing_irregularity=_compute_typing_irregularity(payload.typing_metrics),
    )

    # Step 3 — CSI
    csi = _ml_compute_csi(
        features=features.model_dump(),
        history=[h.model_dump() for h in payload.history],
    )

    # Step 4 — Risk
    risk = _ml_compute_risk(
        history=[h.model_dump() for h in payload.history]
    )

    # Step 5 — Z-score (computed inside csi module, returned separately)
    zscore = raw_emotion.get("zscore", 0.0)

    state = (
        "high"     if csi > 0.75 else
        "elevated" if csi > 0.50 else
        "normal"
    )

    return MLPipelineOutput(
        emotion=EmotionResult(
            scores=EmotionScores(**raw_emotion["scores"]),
            top_signals=raw_emotion.get("top_signals", []),
            confidence=raw_emotion.get("confidence", 0.0),
        ),
        features=features,
        csi=round(csi, 4),
        zscore=round(zscore, 4),
        risk=round(risk, 4),
        state=state,
    )


def _real_audio_analysis(audio_base64: str) -> MLPipelineOutput:
    """
    Passes audio to the ML audio pipeline.
    Expects ML layer to expose:
        analyze_audio(file) -> dict
    """
    raw = _ml_analyze_audio(audio_base64)

    features = MLFeatures(
        negativity=raw.get("negativity", 0.0),
        uncertainty=raw.get("uncertainty", 0.0),
        typing_irregularity=0.0,    # not applicable for audio
    )

    csi   = raw.get("csi", 0.0)
    risk  = raw.get("risk", 0.0)
    state = (
        "high"     if csi > 0.75 else
        "elevated" if csi > 0.50 else
        "normal"
    )

    return MLPipelineOutput(
        emotion=EmotionResult(
            scores=EmotionScores(**raw["scores"]),
            top_signals=raw.get("top_signals", []),
            confidence=raw.get("confidence", 0.0),
        ),
        features=features,
        csi=round(csi, 4),
        zscore=round(raw.get("zscore", 0.0), 4),
        risk=round(risk, 4),
        state=state,
    )


def _compute_typing_irregularity(typing_metrics) -> float:
    """
    Derives a normalized irregularity score from typing metrics.
    High backspaces + high pause variance + low speed = high irregularity.
    """
    speed         = typing_metrics.speed or 1.0
    backspaces    = typing_metrics.backspaces
    pause_var     = typing_metrics.pause_variance

    raw = (backspaces * 0.4) + (pause_var * 0.4) + (1 / speed * 0.2)
    return round(min(raw, 1.0), 4)