"""
Embedding service for generating vector embeddings from text.
Uses sentence transformers for creating embeddings.
"""
from sentence_transformers import SentenceTransformer
from app.config.settings import settings
from typing import List
import numpy as np


class EmbeddingService:
    """
    Service for generating text embeddings.
    
    Uses Sentence Transformers to convert text into dense vector embeddings.
    These embeddings are used for:
    - Vector similarity search in the document chunks
    - Finding relevant documents for user queries
    - Semantic understanding of text
    
    Default model: all-MiniLM-L6-v2 (384-dimensional embeddings)
    This is a lightweight, efficient model suitable for RAG applications.
    
    To use a different model, set EMBEDDING_MODEL in .env file.
    Ensure the model dimension matches the Vector column definition in models.
    """
    
    def __init__(self):
        """Initialize the embedding model."""
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model.
        
        Returns:
            Integer dimension of embedding vectors
        """
        return self.embedding_dimension


# Global embedding service instance
embedding_service = EmbeddingService()
