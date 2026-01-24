"""
Pydantic schemas for request/response validation.
Defines the data structures for API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Schema for chat request."""
    session_id: str = Field(..., description="Session ID for the conversation")
    message: str = Field(..., description="User message to the chatbot")


class ChatResponse(BaseModel):
    """Schema for chat response."""
    session_id: str
    user_message: str
    assistant_message: str
    created_at: datetime


class SessionCreate(BaseModel):
    """Schema for creating a new session."""
    session_id: Optional[str] = Field(None, description="Optional custom session ID")


class SessionResponse(BaseModel):
    """Schema for session response."""
    session_id: str
    created_at: datetime
    message_count: int = 0
    document_count: int = 0


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response."""
    session_id: str
    filename: str
    file_type: str
    chunks_created: int
    message: str


class MessageHistory(BaseModel):
    """Schema for message in conversation history."""
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationHistory(BaseModel):
    """Schema for full conversation history."""
    session_id: str
    messages: List[MessageHistory]
