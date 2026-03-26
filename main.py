# backend/main.py
#type:ignore

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from state_manager import StateManager
from backend.routes import analyze, session, dashboard, escalation

# ─────────────────────────────────────────────
# SINGLETON STATE MANAGER
# Shared across all routes via app.state
# ─────────────────────────────────────────────

state_manager = StateManager()


# ─────────────────────────────────────────────
# LIFESPAN (startup / shutdown)
# ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[BOOT] Mental State Analytics API starting...")
    app.state.state_manager = state_manager
    # TODO: init DB connection here (storage.py Phase 2)
    # TODO: init MongoDB checkpointer here if using LangGraph
    yield
    # Shutdown
    print("[SHUTDOWN] Cleaning up...")


# ─────────────────────────────────────────────
# APP INIT
# ─────────────────────────────────────────────

app = FastAPI(
    title="Mental State Analytics API",
    description="Multimodal mental state tracking with real-time CSI, intervention, and escalation.",
    version="1.0.0",
    lifespan=lifespan,
)


# ─────────────────────────────────────────────
# CORS
# Update origins before production deployment
# ─────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(analyze.router)      # POST /analyze/text, /analyze/audio
app.include_router(session.router)      # POST /session/start, /session/end
app.include_router(dashboard.router)    # GET  /dashboard/{user_id}
app.include_router(escalation.router)   # POST /escalate/check


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Mental State Analytics API", "docs": "/docs"}


# ─────────────────────────────────────────────
# RUN (dev only)
# Use: uvicorn main:app --reload --port 8000
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)