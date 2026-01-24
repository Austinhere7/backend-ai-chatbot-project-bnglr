"""
Session management API endpoints.
Handles creation and retrieval of chat sessions.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from app.config.database import get_db
from app.models.models import Session
from app.models.schemas import SessionCreate, SessionResponse, ConversationHistory, MessageHistory
from typing import List
import uuid

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])


@router.post("/", response_model=SessionResponse)
async def create_session(
    request: SessionCreate,
    db: DBSession = Depends(get_db)
):
    """
    Create a new chat session.
    
    Args:
        request: SessionCreate with optional custom session_id
        db: Database session
        
    Returns:
        SessionResponse with session details
    """
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Check if session already exists
    existing = db.query(Session).filter(
        Session.session_id == session_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Session with ID {session_id} already exists"
        )
    
    # Create new session
    session = Session(session_id=session_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return SessionResponse(
        session_id=session.session_id,
        created_at=session.created_at,
        message_count=0,
        document_count=0
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    db: DBSession = Depends(get_db)
):
    """
    Get session details.
    
    Args:
        session_id: Session ID to retrieve
        db: Database session
        
    Returns:
        SessionResponse with session details
        
    Raises:
        HTTPException: If session not found
    """
    session = db.query(Session).filter(
        Session.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse(
        session_id=session.session_id,
        created_at=session.created_at,
        message_count=len(session.messages),
        document_count=len(session.documents)
    )


@router.get("/{session_id}/history", response_model=ConversationHistory)
async def get_conversation_history(
    session_id: str,
    db: DBSession = Depends(get_db)
):
    """
    Get conversation history for a session.
    
    Args:
        session_id: Session ID
        db: Database session
        
    Returns:
        ConversationHistory with all messages
        
    Raises:
        HTTPException: If session not found
    """
    session = db.query(Session).filter(
        Session.session_id == session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = [
        MessageHistory(
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at
        )
        for msg in session.messages
    ]
    
    return ConversationHistory(
        session_id=session_id,
        messages=messages
    )
