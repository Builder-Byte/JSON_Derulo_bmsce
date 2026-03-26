2. BACKEND OWNER
Responsibilities:

FastAPI server

Endpoint orchestration

DB integration:

SQLite → structured logs

ChromaDB → embeddings (optional phase 2)

Escalation engine (deterministic layer)

Session + user state handling

Deliverables:

/backend/
  main.py
  routes/
    analyze.py
    session.py
  services/
    ml_service.py    
    escalation.py   
    storage.py
  models/
    schemas.py
CORE ENDPOINTS:

POST /analyze/text
POST /analyze/audio
GET  /dashboard/{user_id}
POST /session/start
POST /escalate/check