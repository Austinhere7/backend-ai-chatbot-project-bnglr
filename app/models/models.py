"""
Database models for the AI Chatbot application.
Defines the schema for sessions, messages, and documents.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.config.database import Base


class Session(Base):
    """
    Session model to manage chat sessions.
    Each session represents a separate conversation context.
    """
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    """
    Message model to store conversation history.
    Stores both user messages and AI responses.
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    session = relationship("Session", back_populates="messages")


class Document(Base):
    """
    Document model to store uploaded files.
    Stores file metadata and references to chunked embeddings.
    """
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    content = Column(Text)  # Full text content of the document
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    session = relationship("Session", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    """
    DocumentChunk model to store document chunks with embeddings.
    Uses pgvector for storing and querying vector embeddings.
    """
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    # Vector embedding (dimension=384 for all-MiniLM-L6-v2 model)
    embedding = Column(Vector(384))
    
    # Relationship
    document = relationship("Document", back_populates="chunks")
