"""
Main FastAPI application.
Configures and runs the AI Chatbot API server.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, documents, sessions
from app.config.database import engine, Base
from app.config.settings import settings

# Create FastAPI app
app = FastAPI(
    title="AI Chatbot API",
    description="Backend API for AI Chatbot with RAG capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(sessions.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    # This will be handled by init_db.py script
    pass


@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {
        "message": "AI Chatbot API is running",
        "version": "1.0.0",
        "llm_provider": settings.LLM_PROVIDER
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True
    )
