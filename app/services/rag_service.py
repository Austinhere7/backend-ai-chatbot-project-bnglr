"""
RAG (Retrieval Augmented Generation) service.
Implements the core chatbot logic with context retrieval and generation.
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Tuple
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from app.models.models import Message, DocumentChunk
from app.services.llm_service import llm_service
from app.services.embedding_service import embedding_service


class RAGService:
    """
    Service for Retrieval Augmented Generation (RAG).
    
    This service implements the core chatbot logic by:
    1. Retrieving relevant document chunks using vector similarity search
    2. Building context from relevant documents
    3. Retrieving conversation history for context awareness
    4. Generating responses using the LLM with the retrieved context
    
    The RAG approach enhances the LLM's responses by grounding them in
    user-provided documents, ensuring more accurate and contextually
    relevant answers.
    """
    
    def __init__(self):
        """Initialize RAG service."""
        self.llm = None
        self.embedding_service = embedding_service
    
    def retrieve_relevant_chunks(
        self, 
        db: Session, 
        session_id: int, 
        query: str, 
        top_k: int = 3
    ) -> List[str]:
        """
        Retrieve relevant document chunks using vector similarity search.
        
        Note: For optimal performance with large datasets, ensure database indexes
        are created on session_id and document_id columns. Use EXPLAIN ANALYZE
        to monitor query performance.
        
        Args:
            db: Database session
            session_id: Session ID to filter documents
            query: User query for similarity search
            top_k: Number of top results to return
            
        Returns:
            List of relevant text chunks
        """
        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query)
        
        # Convert embedding to PostgreSQL array format
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        # Query for similar chunks using pgvector
        # Join with documents table to filter by session
        sql_query = text("""
            SELECT dc.chunk_text, dc.embedding <=> :embedding::vector AS distance
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            JOIN sessions s ON d.session_id = s.id
            WHERE s.id = :session_id
            ORDER BY distance
            LIMIT :top_k
        """)
        
        result = db.execute(
            sql_query,
            {"embedding": embedding_str, "session_id": session_id, "top_k": top_k}
        )
        
        chunks = [row[0] for row in result.fetchall()]
        return chunks
    
    def get_conversation_history(self, db: Session, session_id: int, limit: int = 10) -> List[Tuple[str, str]]:
        """
        Retrieve recent conversation history.
        
        Args:
            db: Database session
            session_id: Session ID
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of (role, content) tuples
        """
        messages = db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.created_at.desc()).limit(limit).all()
        
        # Reverse to get chronological order
        messages = list(reversed(messages))
        
        return [(msg.role, msg.content) for msg in messages]
    
    def generate_response(
        self, 
        db: Session, 
        session_id: int, 
        user_message: str
    ) -> str:
        """
        Generate chatbot response using RAG.
        
        Args:
            db: Database session
            session_id: Session ID
            user_message: User's message
            
        Returns:
            Generated response
        """
        # Retrieve relevant document chunks
        try:
            relevant_chunks = self.retrieve_relevant_chunks(db, session_id, user_message)
        except Exception:
            relevant_chunks = []
        
        # Get conversation history
        history = self.get_conversation_history(db, session_id)
        
        # Build context from relevant chunks
        context = ""
        if relevant_chunks:
            context = "\n\n".join(relevant_chunks)
        
        # Create the prompt template
        if context:
            system_message = f"""You are a helpful AI assistant. Use the following context from uploaded documents to answer the user's question. If the context doesn't contain relevant information, you can use your general knowledge.

Context from documents:
{context}

Provide a helpful and accurate response based on the context and conversation history."""
        else:
            system_message = "You are a helpful AI assistant. Provide accurate and helpful responses to user questions."
        
        # Build message history for LangChain
        messages = [("system", system_message)]
        
        # Add conversation history
        for role, content in history:
            if role == "user":
                messages.append(("human", content))
            else:
                messages.append(("assistant", content))
        
        # Add current user message
        messages.append(("human", user_message))
        
        # Generate response using LLM (with graceful fallback if unavailable)
        try:
            llm = llm_service.get_llm()
            response = llm.invoke(messages)
            return response.content
        except Exception:
            if context:
                trimmed_context = context[:1000]
                return (
                    "Based on the uploaded documents, here is the most relevant information:\n\n"
                    f"{trimmed_context}"
                )
            return (
                "The language model is not configured right now. "
                "Please set OPENAI_API_KEY in the .env file to enable full responses."
            )


# Global RAG service instance
rag_service = RAGService()
