"""
LLM service for managing language model interactions.
Powered by OpenAI's GPT models.
"""
from langchain_openai import ChatOpenAI
from app.config.settings import settings


class LLMService:
    """
    Service for managing language model interactions using OpenAI's API.
    
    Uses OpenAI's GPT-3.5-turbo model for conversational AI.
    Requires OPENAI_API_KEY to be set in environment variables.
    
    Example usage:
        from app.services.llm_service import llm_service
        llm = llm_service.get_llm()
        response = llm.invoke([("human", "Hello!")])
    """
    
    def __init__(self):
        """Initialize the LLM service with OpenAI."""
        self.llm = None
    
    def _initialize_llm(self):
        """
        Initialize OpenAI language model.
        
        Returns:
            ChatOpenAI instance
            
        Raises:
            ValueError: If OPENAI_API_KEY is not set
        """
        if not settings.OPENAI_API_KEY:
            return None
        
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )
    
    def get_llm(self):
        """
        Get the initialized LLM instance.
        
        Returns:
            LLM instance
        """
        if self.llm is None:
            self.llm = self._initialize_llm()
        if self.llm is None:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file.")
        return self.llm


# Global LLM service instance
llm_service = LLMService()
