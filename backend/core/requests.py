from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Request model for the chat endpoint."""
    message: str = Field(..., description="The message sent by the user")
    chat_id: Optional[str] = Field(None, description="Unique identifier for the chat session. If None, a new chat will be created.")

class ChatResponse(BaseModel):
    """Standard response model for non-streaming responses."""
    chat_id: str = Field(..., description="Unique identifier for the chat session")
    response: str = Field(..., description="The response from the model")

class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(..., description="Error message")
    