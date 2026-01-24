"""
Document upload API endpoints.
Handles file uploads for RAG context.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session as DBSession
from app.config.database import get_db
from app.models.models import Session, Document, DocumentChunk
from app.models.schemas import DocumentUploadResponse
from app.services.document_service import document_processor
from app.services.embedding_service import embedding_service
from app.config.settings import settings

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    session_id: str = Form(...),
    file: UploadFile = File(...),
    db: DBSession = Depends(get_db)
):
    """
    Upload a document for RAG context.
    Supports PDF and TXT file formats.
    
    Args:
        session_id: Session ID to associate the document with
        file: Uploaded file (PDF or TXT)
        db: Database session
        
    Returns:
        DocumentUploadResponse with upload details
        
    Raises:
        HTTPException: If file type not supported or error occurs
    """
    # Validate file type
    allowed_types = ["application/pdf", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed types: PDF, TXT"
        )
    
    # Get or create session
    session = db.query(Session).filter(
        Session.session_id == session_id
    ).first()
    
    if not session:
        session = Session(session_id=session_id)
        db.add(session)
        db.commit()
        db.refresh(session)
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Process document based on type
        if file.content_type == "application/pdf":
            text_content = document_processor.process_pdf(file_content)
            file_type = "pdf"
        else:  # text/plain
            text_content = document_processor.process_text(file_content)
            file_type = "txt"
        
        # Create document record
        document = Document(
            session_id=session.id,
            filename=file.filename,
            file_type=file_type,
            content=text_content
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Chunk the text
        chunks = document_processor.chunk_text(
            text_content,
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        # Generate embeddings for chunks
        embeddings = embedding_service.generate_embeddings(chunks)
        
        # Store chunks with embeddings
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            doc_chunk = DocumentChunk(
                document_id=document.id,
                chunk_text=chunk,
                chunk_index=idx,
                embedding=embedding
            )
            db.add(doc_chunk)
        
        db.commit()
        
        return DocumentUploadResponse(
            session_id=session_id,
            filename=file.filename,
            file_type=file_type,
            chunks_created=len(chunks),
            message="Document uploaded and processed successfully"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
