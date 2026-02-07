"""
LLM service for managing language model interactions.
Supports multiple providers based on environment settings.
"""
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import settings


class LLMService:
    """
    Service for managing language model interactions.

    Provider selection is controlled by LLM_PROVIDER in the environment.
    Supported providers: openai, gemini.
    """
    
    def __init__(self):
        """Initialize the LLM service."""
        self.llm = None
    
    def _initialize_llm(self):
        """
        Initialize a provider-specific language model.

        Returns:
            A Chat model instance

        Raises:
            ValueError: If required API key is missing or provider is unsupported
        """
        provider = (settings.LLM_PROVIDER or "openai").lower()

        if provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider.")
            return ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY,
            )

        if provider == "gemini":
            if not settings.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY is required for Gemini provider.")
            return ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                temperature=0.7,
                google_api_key=settings.GOOGLE_API_KEY,
            )

        raise ValueError(f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}")
    
    def get_llm(self):
        """
        Get the initialized LLM instance.
        
        Returns:
            LLM instance
        """
        if self.llm is None:
            self.llm = self._initialize_llm()
        return self.llm


# Global LLM service instance
llm_service = LLMService()
