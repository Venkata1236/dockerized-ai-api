# models/schemas.py
# Pydantic models for request and response validation
# Concept: Pydantic — FastAPI uses these to validate incoming data automatically

from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    """
    Request model for the /chat endpoint.
    FastAPI automatically validates this structure.
    """
    message: str                    # User's message (required)
    session_id: str = "default"     # Defaults to "default" if not provided
    temperature: Optional[float] = 0.7  # 0.0 = deterministic, 1.0 = creative

class ChatResponse(BaseModel):
    """Response model for the /chat endpoint."""
    response: str       # AI's reply text
    session_id: str     # Echo back the session ID for client tracking
    status: str = "ok"  # "ok" or "error"

class HealthResponse(BaseModel):
    """Response model for the /health endpoint."""
    status: str     # "ok" or "error"
    message: str    # Human-readable status message

class ClearMemoryRequest(BaseModel):
    """Request model for clearing session memory."""
    session_id: str  # The session to clear

class ClearMemoryResponse(BaseModel):
    """Response model for clearing session memory."""
    status: str   # "ok" or "not_found"
    message: str  # Confirmation or error message