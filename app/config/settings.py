"""
Configuration module for the AI Chatbot application.
Loads environment variables and provides application settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database configuration
    DATABASE_URL: str = "postgresql://chatbot_user:chatbot_password@localhost:5432/chatbot_db"
    
    # OpenAI API Key
    OPENAI_API_KEY: Optional[str] = None
    
    # Application configuration
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    # Vector store configuration
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
