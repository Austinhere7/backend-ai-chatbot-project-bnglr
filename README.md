# AI Chatbot Backend with RAG

A production-ready backend API for an AI chatbot with Retrieval Augmented Generation (RAG) capabilities. The chatbot allows users to upload documents for additional context and maintains conversation history across sessions.

![Architecture](architecture.svg)

## Features

- 🤖 **AI-Powered Chat**: Intelligent conversations using state-of-the-art language modelss
- 📄 **Document Upload**: Support for PDF and TXT files to provide additional context
- 🔍 **RAG (Retrieval Augmented Generation)**: Uses uploaded documents to enhance responses
- 💬 **Conversation History**: Maintains full chat history for contextual responses
- 🎯 **Session Management**: Segregate conversations and documents by session
- 🔌 **Multiple LLM Providers**: Support for OpenAI, Google Gemini, and Anthropic Claude
- 🐳 **Docker Support**: One-command deployment with docker-compose
- 🗄️ **PostgreSQL with pgvector**: Efficient vector storage and similarity search

## Architecture

The application follows a clean, modular architecture:

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         FastAPI Backend             │
├─────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────┐    │
│  │   Chat   │  │   Document   │    │
│  │ Endpoint │  │   Upload     │    │
│  └────┬─────┘  └──────┬───────┘    │
│       │                │            │
│       ▼                ▼            │
│  ┌─────────────────────────────┐   │
│  │      RAG Service            │   │
│  │  - Context Retrieval        │   │
│  │  - History Management       │   │
│  │  - Response Generation      │   │
│  └─────────┬───────────────────┘   │
│            │                        │
│            ▼                        │
│  ┌─────────────────┐               │
│  │   LLM Service   │               │
│  │ (OpenAI/Gemini/ │               │
│  │   Anthropic)    │               │
│  └─────────────────┘               │
└─────────┬───────────────────────────┘
          │
          ▼
┌────────────────────────────┐
│   PostgreSQL + pgvector    │
│  - Sessions               │
│  - Messages               │
│  - Documents              │
│  - Vector Embeddings      │
└───────────────────────────┘
```

## System Requirements

- **Docker & Docker Compose** (recommended)
  - Docker Engine 20.10+
  - Docker Compose 2.0+

OR for local setup:

- **Python 3.11+**
- **PostgreSQL 14+** with **pgvector** extension
- **pip** (Python package manager)

## Quick Start with Docker (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/Austinhere7/backend-ai-chatbot-project-bnglr.git
cd backend-ai-chatbot-project-bnglr
```

### 2. Configure Environment Variables

Copy the example environment file and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` file with your preferred text editor:

```bash
nano .env  # or vim .env, or any editor
```

**Required Configuration:**

```env
# Choose your LLM provider: openai, gemini, or anthropic
LLM_PROVIDER=openai

# Add the API key for your chosen provider
OPENAI_API_KEY=sk-your-openai-api-key-here
# OR
GOOGLE_API_KEY=your-google-api-key-here
# OR
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### 3. Start the Application

```bash
docker-compose up
```

This single command will:
- Start PostgreSQL database with pgvector extension
- Initialize the database schema
- Start the backend API server

The API will be available at: **http://localhost:8000**

### 4. Verify Installation

Open your browser or use curl:

```bash
curl http://localhost:8000
```

You should see:
```json
{
  "message": "AI Chatbot API is running",
  "version": "1.0.0",
  "llm_provider": "openai"
}
```

## Local Setup (Without Docker)

### 1. Install PostgreSQL with pgvector

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

**Install pgvector extension:**
```bash
cd /tmp
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

**On macOS (with Homebrew):**
```bash
brew install postgresql
brew install pgvector
```

### 2. Create Database

```bash
# Start PostgreSQL
sudo service postgresql start  # Ubuntu/Debian
# OR
brew services start postgresql  # macOS

# Create database and user
sudo -u postgres psql
```

In PostgreSQL prompt:
```sql
CREATE DATABASE chatbot_db;
CREATE USER chatbot_user WITH PASSWORD 'chatbot_password';
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;
\q
```

### 3. Clone and Setup

```bash
git clone https://github.com/Austinhere7/backend-ai-chatbot-project-bnglr.git
cd backend-ai-chatbot-project-bnglr

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

### 5. Initialize Database

```bash
python init_db.py
```

### 6. Run the Application

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: **http://localhost:8000**

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Create Session

Create a new chat session:

```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-24T10:30:00.000Z",
  "message_count": 0,
  "document_count": 0
}
```

### 2. Upload Document

Upload a document for context (PDF or TXT):

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "session_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "file=@/path/to/document.pdf"
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "document.pdf",
  "file_type": "pdf",
  "chunks_created": 15,
  "message": "Document uploaded and processed successfully"
}
```

### 3. Chat

Send a message to the chatbot:

```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "What is mentioned in the document about AI?"
  }'
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_message": "What is mentioned in the document about AI?",
  "assistant_message": "Based on the document you uploaded...",
  "created_at": "2024-01-24T10:35:00.000Z"
}
```

### 4. Get Conversation History

Retrieve chat history for a session:

```bash
curl http://localhost:8000/api/sessions/550e8400-e29b-41d4-a716-446655440000/history
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql://chatbot_user:chatbot_password@localhost:5432/chatbot_db` |
| `LLM_PROVIDER` | LLM provider (openai/gemini/anthropic) | Yes | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | If using OpenAI | - |
| `GOOGLE_API_KEY` | Google API key for Gemini | If using Gemini | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | If using Anthropic | - |
| `APP_HOST` | Server host | No | `0.0.0.0` |
| `APP_PORT` | Server port | No | `8000` |
| `EMBEDDING_MODEL` | Sentence transformer model | No | `all-MiniLM-L6-v2` |
| `CHUNK_SIZE` | Document chunk size | No | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap size | No | `200` |

### Supported LLM Providers

#### OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```
- Get API key: https://platform.openai.com/api-keys

#### Google Gemini
```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=...
```
- Get API key: https://makersuite.google.com/app/apikey

#### Anthropic Claude
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=...
```
- Get API key: https://console.anthropic.com/

## Project Structure

```
backend-ai-chatbot-project-bnglr/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── chat.py            # Chat endpoint
│   │   ├── documents.py       # Document upload endpoint
│   │   └── sessions.py        # Session management endpoints
│   ├── config/                # Configuration
│   │   ├── database.py        # Database setup
│   │   └── settings.py        # App settings
│   ├── models/                # Data models
│   │   ├── models.py          # SQLAlchemy models
│   │   └── schemas.py         # Pydantic schemas
│   ├── services/              # Business logic
│   │   ├── llm_service.py     # LLM integration
│   │   ├── embedding_service.py # Embeddings
│   │   ├── document_service.py  # Document processing
│   │   └── rag_service.py     # RAG implementation
│   └── main.py                # FastAPI application
├── init_db.py                 # Database initialization
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker orchestration
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Database Schema

### Sessions Table
- `id`: Primary key
- `session_id`: Unique session identifier
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Messages Table
- `id`: Primary key
- `session_id`: Foreign key to sessions
- `role`: 'user' or 'assistant'
- `content`: Message text
- `created_at`: Timestamp

### Documents Table
- `id`: Primary key
- `session_id`: Foreign key to sessions
- `filename`: Original filename
- `file_type`: File type (pdf/txt)
- `content`: Full document text
- `created_at`: Timestamp

### Document_Chunks Table
- `id`: Primary key
- `document_id`: Foreign key to documents
- `chunk_text`: Text chunk
- `chunk_index`: Chunk position
- `embedding`: Vector embedding (384 dimensions)

## Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Full Workflow Test

```bash
# 1. Create session
SESSION_ID=$(curl -s -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" -d '{}' | jq -r '.session_id')

echo "Session ID: $SESSION_ID"

# 2. Upload a document
curl -X POST http://localhost:8000/api/documents/upload \
  -F "session_id=$SESSION_ID" \
  -F "file=@sample.txt"

# 3. Chat with the bot
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"What is in the document?\"
  }"

# 4. Get conversation history
curl http://localhost:8000/api/sessions/$SESSION_ID/history
```

## Troubleshooting

### Docker Issues

**Database connection errors:**
```bash
# Check if database is running
docker-compose ps

# View database logs
docker-compose logs db

# Restart services
docker-compose down
docker-compose up
```

**Port already in use:**
```bash
# Change port in docker-compose.yml or stop conflicting service
sudo lsof -i :8000  # Find process using port 8000
```

### Local Setup Issues

**pgvector not found:**
```bash
# Ensure pgvector is properly installed
sudo -u postgres psql -d chatbot_db -c "CREATE EXTENSION vector;"
```

**Module import errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Database connection errors:**
- Verify PostgreSQL is running: `sudo service postgresql status`
- Check credentials in `.env` file
- Ensure database exists: `sudo -u postgres psql -l`

## Development

### Adding New Features

1. **New API Endpoint**: Add to `app/api/`
2. **New Model**: Update `app/models/models.py`
3. **New Service**: Add to `app/services/`

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all functions
- Keep functions focused and modular

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/Austinhere7/backend-ai-chatbot-project-bnglr/issues

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [LangChain](https://www.langchain.com/)
- Vector storage by [pgvector](https://github.com/pgvector/pgvector)
- Embeddings by [Sentence Transformers](https://www.sbert.net/)