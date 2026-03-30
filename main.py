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

# ── Load environment variables from .env file ──────────────────
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")  # Must be set in .env

# ── Initialize FastAPI app with metadata ──────────────────────
app = FastAPI(
    title="AI Chat API",
    description="LangChain-powered chat API built with FastAPI",
    version="1.0.0"
)

# ── CORS — allow all origins (update in production) ──────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict this in production
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
    """Health check endpoint — used by Docker and monitoring tools."""
    return HealthResponse(status="ok", message="Healthy")

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint.
    - Each session_id maintains its own conversation history
    - Temperature controls creativity (0.0 = focused, 1.0 = creative)
    """
    # Validate API key before processing
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    try:
        # Step 1: Get or create memory for this session
        memory = get_memory(request.session_id)

        # Step 2: Build the LangChain chain with memory attached
        chain = create_chat_chain(API_KEY, memory, request.temperature)

        # Step 3: Get AI response
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

    # Return appropriate message based on whether session existed
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
    """Lists all active sessions and their count."""
    sessions = get_active_sessions()
    return {"active_sessions": sessions, "count": len(sessions)}