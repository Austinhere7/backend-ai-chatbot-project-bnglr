"""
Chat API endpoints.
Handles chat interactions with the AI assistant.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from app.config.database import get_db
from app.models.models import Session, Message
from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import rag_service
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: DBSession = Depends(get_db)
):
    """
    Chat endpoint for sending messages to the AI assistant.
    
    Args:
        request: ChatRequest containing session_id and message
        db: Database session
        
    Returns:
        ChatResponse with user message, assistant response, and metadata
        
    Raises:
        HTTPException: If session not found or error occurs
    """
    # Get or create session
    session = db.query(Session).filter(
        Session.session_id == request.session_id
    ).first()
    
    if not session:
        # Create new session if it doesn't exist
        session = Session(session_id=request.session_id)
        db.add(session)
        db.commit()
        db.refresh(session)
    
    try:
        # Generate response using RAG
        assistant_response = rag_service.generate_response(
            db, 
            session.id, 
            request.message
        )
        
        # Save user message
        user_msg = Message(
            session_id=session.id,
            role="user",
            content=request.message
        )
        db.add(user_msg)
        
        # Save assistant response
        assistant_msg = Message(
            session_id=session.id,
            role="assistant",
            content=assistant_response
        )
        db.add(assistant_msg)
        
        # Update session timestamp
        session.updated_at = datetime.now()
        
        db.commit()
        db.refresh(assistant_msg)
        
        return ChatResponse(
            session_id=request.session_id,
            user_message=request.message,
            assistant_message=assistant_response,
            created_at=assistant_msg.created_at
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
