"""
LLM service for managing language model interactions.
Supports multiple LLM providers: OpenAI, Gemini, and Anthropic.
"""
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from app.config.settings import settings


class LLMService:
    """
    Service for managing language model interactions.
    
    Supports multiple LLM providers:
    - OpenAI: Uses gpt-3.5-turbo model
    - Google Gemini: Uses gemini-pro model
    - Anthropic Claude: Uses claude-3-sonnet model
    
    The provider is configured via the LLM_PROVIDER environment variable.
    Each provider requires its specific API key set in environment variables.
    
    Example usage:
        from app.services.llm_service import llm_service
        llm = llm_service.get_llm()
        response = llm.invoke([("human", "Hello!")])
    """
    
    def __init__(self):
        """Initialize the LLM service with configured provider."""
        self.provider = settings.LLM_PROVIDER.lower()
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """
        Initialize the language model based on configured provider.
        
        Returns:
            Initialized LLM instance
            
        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        if self.provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
        
        elif self.provider == "gemini":
            if not settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY is required for Gemini provider")
            return ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=0.7,
                google_api_key=settings.GOOGLE_API_KEY
            )
        
        elif self.provider == "anthropic":
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider")
            return ChatAnthropic(
                model="claude-3-sonnet-20240229",
                temperature=0.7,
                anthropic_api_key=settings.ANTHROPIC_API_KEY
            )
        
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def get_llm(self):
        """
        Get the initialized LLM instance.
        
        Returns:
            LLM instance
        """
        return self.llm


# Global LLM service instance
llm_service = LLMService()
