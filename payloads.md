Here’s your complete specification formatted cleanly as a `.md` file:

---

````markdown
# PAYLOAD SPECIFICATION — MENTAL STATE ANALYTICS SYSTEM

## 1. FRONTEND → BACKEND (PRIMARY INPUT)

```json
{
  "schema_version": "v1",
  "user_id": "string",
  "timestamp": "ISO-8601",
  "text": "string",
  "audio_base64": "optional_string",
  "typing_metrics": {
    "speed": "float",
    "backspaces": "int",
    "latency": "float",
    "pause_variance": "float"
  },
  "session_metadata": {
    "session_id": "string",
    "device": "web|mobile",
    "local_time": "HH:MM",
    "input_mode": "text|voice"
  }
}
````

---

## 2. BACKEND → ML PIPELINE (INTERNAL CONTRACT)

```json
{
  "text": "string",
  "typing_metrics": {
    "speed": "float",
    "backspaces": "int",
    "latency": "float",
    "pause_variance": "float"
  },
  "history": [
    {
      "csi": "float",
      "timestamp": "ISO-8601"
    }
  ]
}
```

---

## 3. ML PIPELINE OUTPUT (RAW RESPONSE)

```json
{
  "emotion": {
    "scores": {
      "anger": "float",
      "sadness": "float",
      "fear": "float",
      "joy": "float",
      "disgust": "float",
      "surprise": "float",
      "neutral": "float"
    },
    "confidence": "float"
  },
  "features": {
    "negativity": "float",
    "uncertainty": "float",
    "typing_irregularity": "float"
  },
  "csi": "float",
  "zscore": "float",
  "risk": "float",
  "state": "normal|elevated|high"
}
```

---

## 4. BACKEND → FRONTEND (FINAL RESPONSE)

```json
{
  "schema_version": "v1",
  "user_id": "string",
  "timestamp": "ISO-8601",
  "analysis": {
    "emotion": {
      "top_signals": ["sadness", "fear"],
      "confidence": "float"
    },
    "csi": "float",
    "zscore": "float",
    "risk": "float",
    "state": "normal|elevated|high"
  },
  "intervention": {
    "type": "breathing|reflection|none",
    "payload": {
      "duration_sec": "int",
      "prompt": "string"
    }
  },
  "escalation": {
    "triggered": "boolean",
    "level": "low|medium|high|critical",
    "reason": "keyword|risk|behavioral"
  }
}
```

---

## 5. BACKEND → DATABASE (LOG FORMAT)

```json
{
  "user_id": "string",
  "timestamp": "ISO-8601",
  "csi": "float",
  "risk": "float",
  "state": "string",
  "features": {
    "negativity": "float",
    "uncertainty": "float",
    "typing_irregularity": "float"
  }
}
```

---

## 6. DASHBOARD RESPONSE PAYLOAD

```json
{
  "user_id": "string",
  "history": [
    {
      "timestamp": "ISO-8601",
      "csi": "float",
      "risk": "float",
      "state": "string"
    }
  ],
  "aggregates": {
    "avg_csi": "float",
    "max_risk": "float",
    "trend": "increasing|stable|decreasing"
  }
}
```

---

## 7. ESCALATION EVENT PAYLOAD (CRITICAL PATH)

```json
{
  "user_id": "string",
  "timestamp": "ISO-8601",
  "trigger": {
    "type": "keyword|risk|combined",
    "details": "string"
  },
  "signals": {
    "csi": "float",
    "risk": "float",
    "zscore": "float"
  },
  "action": {
    "level": "critical",
    "next_step": "contact_support|alert_contact|show_resources"
  }
}
```

---

## 8. ERROR RESPONSE PAYLOAD

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "string",
    "details": {}
  }
}
```

---

# CRITICAL ANALYSIS

## Assumption

Defining payloads = system readiness

## Counterpoint

Payloads without:

* validation
* schema enforcement
* version control

→ will break under integration

## Hidden Gaps

* No strict typing (e.g., Pydantic not enforced)
* No structured error propagation across services
* No backward compatibility strategy
* No schema evolution policy

---

# FINAL RULE

Payloads are contracts, not suggestions.
Any deviation across frontend, backend, or ML will collapse the system.

```

---

If you want, I can next:
- Turn this into **Pydantic models (production-ready)**
- Add **OpenAPI/Swagger spec**
- Or design **event-driven architecture (Kafka schema contracts)**
```
