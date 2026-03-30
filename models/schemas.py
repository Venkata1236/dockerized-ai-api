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
    message: str                          # User's message
    session_id: str = "default"          # Session ID for memory
    temperature: Optional[float] = 0.7   # Response creativity


class ChatResponse(BaseModel):
    """
    Response model for the /chat endpoint.
    """
    response: str        # Bot's reply
    session_id: str      # Echo back the session ID
    status: str = "ok"  # Status of the request


class HealthResponse(BaseModel):
    """Response model for the /health endpoint."""
    status: str
    message: str


class ClearMemoryRequest(BaseModel):
    """Request model for clearing session memory."""
    session_id: str


class ClearMemoryResponse(BaseModel):
    """Response model for clearing session memory."""
    status: str
    message: str