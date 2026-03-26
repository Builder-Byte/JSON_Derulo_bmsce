# backend/services/baseline_manager.py

import math
from datetime import datetime, timezone
from typing import Optional


# ─────────────────────────────────────────────
# GLOBAL PRIORS (cold start defaults)
# Used when user history < MIN_SESSIONS
# Based on population-level estimates
# ─────────────────────────────────────────────

GLOBAL_PRIOR_CSI_MEAN  = 0.40
GLOBAL_PRIOR_CSI_STD   = 0.15
GLOBAL_PRIOR_RISK_MEAN = 0.35
GLOBAL_PRIOR_RISK_STD  = 0.12

MIN_SESSIONS           = 5     # minimum history needed for personal baseline
WINDOW_SIZE            = 10    # rolling window for mean/std computation
EMA_ALPHA              = 0.3   # exponential moving average smoothing factor


# ─────────────────────────────────────────────
# BASELINE STORE
# user_id → { csi_window, risk_window, ema_csi, ema_risk, session_count }
# ─────────────────────────────────────────────

_baseline_store: dict[str, dict] = {}


def _init_user(user_id: str):
    if user_id not in _baseline_store:
        _baseline_store[user_id] = {
            "csi_window":    [],       # rolling list of CSI values
            "risk_window":   [],       # rolling list of risk values
            "ema_csi":       None,     # exponential moving average for CSI
            "ema_risk":      None,     # exponential moving average for risk
            "session_count": 0,
            "last_updated":  None,
        }


# ─────────────────────────────────────────────
# INTERNAL MATH HELPERS
# ─────────────────────────────────────────────

def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 1.0                  # avoid division by zero
    m = _mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance) or 1.0


def _ema(prev: Optional[float], new_val: float, alpha: float) -> float:
    """Exponential moving average — smooths noisy typing/CSI signals."""
    if prev is None:
        return new_val
    return alpha * new_val + (1 - alpha) * prev


def _zscore(value: float, mean: float, std: float) -> float:
    """Signed z-score — how many std deviations from baseline."""
    return round((value - mean) / (std or 1.0), 4)


# ─────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────

def update(user_id: str, csi: float, risk: float):
    """
    Ingests a new CSI + risk value into the user's rolling baseline.
    Call this after every store_ml_output().

    Args:
        user_id:  User identifier
        csi:      Latest CSI value from ML pipeline
        risk:     Latest risk score from ML pipeline
    """
    _init_user(user_id)
    b = _baseline_store[user_id]

    # Rolling window — drop oldest if at capacity
    b["csi_window"].append(csi)
    b["risk_window"].append(risk)

    if len(b["csi_window"]) > WINDOW_SIZE:
        b["csi_window"].pop(0)
    if len(b["risk_window"]) > WINDOW_SIZE:
        b["risk_window"].pop(0)

    # EMA update
    b["ema_csi"]  = _ema(b["ema_csi"],  csi,  EMA_ALPHA)
    b["ema_risk"] = _ema(b["ema_risk"], risk, EMA_ALPHA)

    b["session_count"] += 1
    b["last_updated"]   = datetime.now(timezone.utc).isoformat()


def get_baseline(user_id: str) -> dict:
    """
    Returns the current baseline stats for a user.
    Falls back to global priors during cold start (< MIN_SESSIONS).

    Returns:
        {
            csi_mean, csi_std,
            risk_mean, risk_std,
            ema_csi, ema_risk,
            session_count,
            is_cold_start
        }
    """
    _init_user(user_id)
    b = _baseline_store[user_id]
    is_cold_start = b["session_count"] < MIN_SESSIONS

    if is_cold_start:
        return {
            "csi_mean":      GLOBAL_PRIOR_CSI_MEAN,
            "csi_std":       GLOBAL_PRIOR_CSI_STD,
            "risk_mean":     GLOBAL_PRIOR_RISK_MEAN,
            "risk_std":      GLOBAL_PRIOR_RISK_STD,
            "ema_csi":       b["ema_csi"]  or GLOBAL_PRIOR_CSI_MEAN,
            "ema_risk":      b["ema_risk"] or GLOBAL_PRIOR_RISK_MEAN,
            "session_count": b["session_count"],
            "is_cold_start": True,
        }

    return {
        "csi_mean":      round(_mean(b["csi_window"]),  4),
        "csi_std":       round(_std(b["csi_window"]),   4),
        "risk_mean":     round(_mean(b["risk_window"]), 4),
        "risk_std":      round(_std(b["risk_window"]),  4),
        "ema_csi":       round(b["ema_csi"],            4),
        "ema_risk":      round(b["ema_risk"],           4),
        "session_count": b["session_count"],
        "is_cold_start": False,
    }


def compute_zscore(user_id: str, csi: float, risk: float) -> dict:
    """
    Computes z-scores for CSI and risk against user's personal baseline.
    Uses global priors during cold start.

    Args:
        user_id:  User identifier
        csi:      Current CSI value
        risk:     Current risk score

    Returns:
        { csi_zscore, risk_zscore, baseline_delta, is_cold_start }
    """
    baseline = get_baseline(user_id)

    csi_zscore  = _zscore(csi,  baseline["csi_mean"],  baseline["csi_std"])
    risk_zscore = _zscore(risk, baseline["risk_mean"], baseline["risk_std"])

    # Baseline delta — how far current EMA has drifted from rolling mean
    baseline_delta = round(
        abs(baseline["ema_csi"] - baseline["csi_mean"]), 4
    )

    return {
        "csi_zscore":      csi_zscore,
        "risk_zscore":     risk_zscore,
        "baseline_delta":  baseline_delta,
        "is_cold_start":   baseline["is_cold_start"],
    }


def is_anomaly(user_id: str, csi: float, zscore_threshold: float = 2.0) -> bool:
    """
    Returns True if the current CSI is a statistically significant
    deviation from the user's personal baseline.

    Args:
        user_id:           User identifier
        csi:               Current CSI value
        zscore_threshold:  Standard deviations to flag as anomaly (default 2σ)
    """
    baseline   = get_baseline(user_id)
    csi_zscore = _zscore(csi, baseline["csi_mean"], baseline["csi_std"])
    return abs(csi_zscore) >= zscore_threshold


def get_trend(user_id: str) -> str:
    """
    Computes CSI trend direction from the rolling window.

    Returns:
        'increasing' | 'decreasing' | 'stable'
    """
    _init_user(user_id)
    window = _baseline_store[user_id]["csi_window"]

    if len(window) < 3:
        return "stable"

    # Compare first half mean vs second half mean
    mid   = len(window) // 2
    first = _mean(window[:mid])
    last  = _mean(window[mid:])
    delta = last - first

    if delta > 0.05:
        return "increasing"
    elif delta < -0.05:
        return "decreasing"
    return "stable"


def reset(user_id: str):
    """Clears baseline for a user. Call on session wipe or account reset."""
    if user_id in _baseline_store:
        del _baseline_store[user_id]
