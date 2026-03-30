# main.py
# FastAPI application — exposes LangChain as REST API endpoints
# Concept: FastAPI decorators, Pydantic validation, REST endpoints

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import (
    ChatRequest, ChatResponse,
    HealthResponse,
    ClearMemoryRequest, ClearMemoryResponse
)
from chains.memory import get_memory, clear_memory, get_active_sessions
from chains.chat_chain import create_chat_chain, get_response

# ── Load env ──────────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# ── FastAPI app ───────────────────────────────────────────────
app = FastAPI(
    title="AI Chat API",
    description="LangChain-powered chat API built with FastAPI",
    version="1.0.0"
)

# ── CORS — allow all origins ──────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ────────────────────────────────────────────────────

@app.get("/", response_model=HealthResponse)
def root():
    """Root endpoint — check if API is running."""
    return HealthResponse(
        status="ok",
        message="AI Chat API is running. Visit /docs for API documentation."
    )


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", message="Healthy")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Accepts a message and session_id, returns AI response.

    - POST /chat
    - Body: {"message": "Hello", "session_id": "user123"}
    - Returns: {"response": "Hi there!", "session_id": "user123"}
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    try:
        # Get or create session memory
        memory = get_memory(request.session_id)

        # Create chain with session memory
        chain = create_chat_chain(API_KEY, memory, request.temperature)

        # Get response
        response = get_response(chain, request.message)

        return ChatResponse(
            response=response,
            session_id=request.session_id,
            status="ok"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clear-memory", response_model=ClearMemoryResponse)
def clear_session_memory(request: ClearMemoryRequest):
    """
    Clears conversation memory for a session.

    - POST /clear-memory
    - Body: {"session_id": "user123"}
    """
    cleared = clear_memory(request.session_id)
    if cleared:
        return ClearMemoryResponse(
            status="ok",
            message=f"Memory cleared for session: {request.session_id}"
        )
    return ClearMemoryResponse(
        status="not_found",
        message=f"Session not found: {request.session_id}"
    )


@app.get("/sessions")
def list_sessions():
    """Lists all active sessions."""
    sessions = get_active_sessions()
    return {"active_sessions": sessions, "count": len(sessions)}