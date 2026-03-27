# 🧠 Multimodal Behavioral Observability Engine

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Lightweight_Gateway-lightgrey.svg)
![Frontend](https://img.shields.io/badge/Frontend-Vanilla_JS_%7C_HTML5-orange.svg)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-F9AB00.svg)
![Status](https://img.shields.io/badge/Status-Hackathon_Ready-success.svg)

> **Built for the IMPACT AI Hackathon**
> 
> *Moving beyond standard "AI chatbots" to create a clinical-grade, time-series behavioral triage system.*

## 📖 The Problem
Current mental health AI relies entirely on semantic text analysis. If a user types, *"I'm doing absolutely great!"*, standard LLM wrappers will classify them as "Happy." But what if it took them 45 seconds, 20 backspaces, highly erratic keystrokes, and a shaking voice to deliver that single sentence? Standard AI misses the "Fake Smile."

## 🚀 Our Solution
We built a **Multimodal Temporal Observability Engine**. It does not try to be an "AI Therapist." Instead, it is a frictionless background triage system that ingests natural language, sub-conscious physical typing telemetry, and raw acoustic voice data to infer cognitive strain over time. 

It calculates a personalized **Cognitive Strain Index (CSI)**, tracks deviations using Exponential Moving Averages, and triggers UI interventions before a crisis occurs.

---

## ✨ Core Architecture & Pitchable Features

### 1. 🎭 "Cognitive Masking" Detection (The Heuristic Engine)
Standard sentiment analysis is brittle. We map Hugging Face text-classification (`j-hartmann/emotion-english-distilroberta-base`) against live keystroke telemetry and acoustic DSP. If semantic positivity is high but physical typing/vocal tremors are highly erratic, the system instantly flags hidden distress (`is_masking: True`).

### 2. 📊 Dynamic Baseline Calibration
Stress looks different for everyone. Instead of hardcoded risk thresholds, our engine calculates a rolling mean of a user's CSI. The system only escalates risk when a user deviates significantly from *their own* historical norm.

### 3. 📉 Temporal Risk Observability
Mental state is a time-series sequence. We use **Exponential Moving Averages (EMA)** to smooth telemetry noise. This prevents UI whiplash from a single typo while successfully catching slow, steady declines in mental stability over 14-day longitudinal windows.

### 4. 🚑 Automated Micro-Intervention Engine
The ML pipeline outputs direct UI action triggers based on current risk levels:
* **Masking Detected:** Triggers contextual grounding UI (e.g., 5-4-3-2-1 technique).
* **Severe Spikes (Crisis Lexicon):** Bypasses standard UI smoothing and triggers an un-dismissible **SOS 988 Crisis Handoff**.

### 5. 🔍 Transparent Explainability (XAI)
To bridge the gap between AI and clinical trust, every inference returns a human-readable `explanations` array detailing exactly *why* the AI made its decision (e.g., *"Acoustic anomaly: High vocal tremor detected contradicting semantic input."*).

---

## ⚙️ System Workflow

To achieve zero-latency processing suitable for edge-node clinical environments, we bypassed heavy Virtual DOM frameworks (like React) and ASGI bloat in favor of a decoupled, high-throughput micro-architecture.

1. **Telemetry Intercept (Vanilla JS / HTML5):** User interacts with the UI. Native browser event listeners and WebRTC silently harvest `speed`, `backspaces`, `latency`, and 4-second `audio_blobs`.
2. **The API Bridge (Flask):** A lightweight routing tier that receives the multipart/form-data payload and bridges it to the ML core.
3. **The ML Engine (Python):** * Runs NLP extraction (DistilRoBERTa).
   * Runs Acoustic Digital Signal Processing (`librosa`) with a 20dB noise-floor trim to calculate spectral centroids.
   * Fuses text + physical + voice data into a raw CSI.
   * Calculates EMA risk trend.
4. **Clinician Sandbox (Vanilla JS + Chart.js):** The Single Page Application (SPA) instantly parses the JSON response, rendering real-time telemetry, metric dashboards, and anomaly alerts natively in the browser.

---

## 🛠️ Installation & Local Setup

### Prerequisites
* Python 3.9+
* pip

### 1. Clone the repository
```bash
git clone [https://github.com/Builder-Byte/JSON_Derulo_bmsce.git](https://github.com/Builder-Byte/JSON_Derulo_bmsce.git)
cd JSON_Derulo_bmsce
