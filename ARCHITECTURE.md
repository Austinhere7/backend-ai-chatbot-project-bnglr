# AI Chatbot Backend - Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT / API CONSUMER                         │
│                     (e.g., Frontend Application)                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND SERVER                            │
│                      (Port 8000)                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      API ROUTERS                             │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │   Chat Router   │  │Document Router│  │Session Router│    │   │
│  │  ├─────────────────┤  ├──────────────┤  ├──────────────┤    │   │
│  │  │ POST /chat      │  │POST /upload  │  │POST /        │    │   │
│  │  │ (Chat endpoint) │  │ (File upload)│  │(Create sess) │    │   │
│  │  │                 │  │              │  │              │    │   │
│  │  │                 │  │GET /list     │  │GET /         │    │   │
│  │  │                 │  │(List docs)   │  │(List sess)   │    │   │
│  │  │                 │  │              │  │              │    │   │
│  │  │                 │  │              │  │GET /{id}     │    │   │
│  │  │                 │  │              │  │(Get details) │    │   │
│  │  │                 │  │              │  │              │    │   │
│  │  │                 │  │              │  │GET /{id}/... │    │   │
│  │  │                 │  │              │  │(Get history) │    │   │
│  │  │                 │  │              │  │              │    │   │
│  │  │                 │  │              │  │DELETE /{id}  │    │   │
│  │  │                 │  │              │  │(Delete sess) │    │   │
│  │  └────────┬────────┘  └──────┬───────┘  └──────┬───────┘    │   │
│  │           │                  │                  │             │   │
│  └───────────┼──────────────────┼──────────────────┼─────────────┘   │
│              │                  │                  │                  │
│  ┌───────────▼──────────────────▼──────────────────▼─────────────┐   │
│  │                    SERVICE LAYER                              │   │
│  ├────────────────────────────────────────────────────────────────┤   │
│  │                                                                 │   │
│  │  ┌──────────────────┐  ┌──────────────────┐                  │   │
│  │  │  RAG Service     │  │ Document Service │                  │   │
│  │  ├──────────────────┤  ├──────────────────┤                  │   │
│  │  │ • Retrieve       │  │ • Process PDF    │                  │   │
│  │  │   relevant       │  │ • Process Text   │                  │   │
│  │  │   chunks         │  │ • Chunk text     │                  │   │
│  │  │ • Get history    │  │ • Validate files │                  │   │
│  │  │ • Generate       │  │                  │                  │   │
│  │  │   responses      │  │                  │                  │   │
│  │  └────────┬─────────┘  └────────┬─────────┘                  │   │
│  │           │                     │                            │   │
│  │  ┌────────▼──────────────┬──────▼──────────────┐            │   │
│  │  │  LLM Service          │ Embedding Service   │            │   │
│  │  ├───────────────────────┼─────────────────────┤            │   │
│  │  │ • Initialize LLM      │ • Generate          │            │   │
│  │  │ • OpenAI              │   embeddings        │            │   │
│  │  │ • Gemini              │ • Sentence          │            │   │
│  │  │ • Anthropic           │   Transformers      │            │   │
│  │  │ • Generate text       │ • 384-dim vectors   │            │   │
│  │  └────────┬──────────────┴──────┬──────────────┘            │   │
│  │           │                     │                            │   │
│  └───────────┼─────────────────────┼────────────────────────────┘   │
│              │                     │                                 │
│              │        ┌────────────┴───────────┐                     │
│              │        │                        │                     │
└──────────────┼────────┼────────────────────────┼─────────────────────┘
               │        │                        │
               ▼        ▼                        ▼
        ┌──────────────────────────────────────────────────┐
        │    POSTGRESQL DATABASE + pgvector               │
        │    (Port 5432)                                   │
        ├──────────────────────────────────────────────────┤
        │                                                   │
        │  ┌────────────────┐  ┌─────────────────────┐    │
        │  │  sessions      │  │  messages           │    │
        │  ├────────────────┤  ├─────────────────────┤    │
        │  │ • id (PK)      │  │ • id (PK)           │    │
        │  │ • session_id   │  │ • session_id (FK)   │    │
        │  │ • created_at   │  │ • role (user/asst)  │    │
        │  │ • updated_at   │  │ • content           │    │
        │  └────────────────┘  │ • created_at        │    │
        │                      └─────────────────────┘    │
        │                                                   │
        │  ┌────────────────┐  ┌─────────────────────┐    │
        │  │  documents     │  │  document_chunks    │    │
        │  ├────────────────┤  ├─────────────────────┤    │
        │  │ • id (PK)      │  │ • id (PK)           │    │
        │  │ • session_id   │  │ • document_id (FK)  │    │
        │  │ • filename     │  │ • chunk_text        │    │
        │  │ • file_type    │  │ • chunk_index       │    │
        │  │ • content      │  │ • embedding         │    │
        │  │ • created_at   │  │   (384-dim vector)  │    │
        │  └────────────────┘  │ • pgvector index    │    │
        │                      └─────────────────────┘    │
        │                                                   │
        └──────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Chat Request Flow

```
1. User sends chat message
   │
   ├─▶ POST /api/chat
   │   {
   │     "session_id": "abc123",
   │     "message": "What is RAG?"
   │   }
   │
   ▼
2. Get/Create Session
   │
   ├─▶ Query sessions table
   ├─▶ Create if not exists
   │
   ▼
3. Retrieve Context (RAG)
   │
   ├─▶ Generate embedding for user message
   │   (Sentence Transformers: all-MiniLM-L6-v2)
   │
   ├─▶ Vector similarity search in pgvector
   │   SELECT TOP 3 chunks similar to message
   │   ORDER BY embedding distance ASC
   │
   ├─▶ Get conversation history (last 10 messages)
   │
   ▼
4. Generate Response
   │
   ├─▶ Build system prompt with context
   ├─▶ Include relevant document chunks
   ├─▶ Include conversation history
   ├─▶ Add user message
   │
   ├─▶ Call LLM (OpenAI/Gemini/Anthropic)
   │   with conversation context
   │
   ▼
5. Store Conversation
   │
   ├─▶ Save user message to messages table
   ├─▶ Save AI response to messages table
   ├─▶ Update session.updated_at
   │
   ▼
6. Return Response
   │
   └─▶ ChatResponse {
         "session_id": "abc123",
         "user_message": "What is RAG?",
         "assistant_message": "RAG stands for...",
         "created_at": "2024-01-24T10:30:00Z"
       }
```

### Document Upload Flow

```
1. User uploads document
   │
   ├─▶ POST /api/documents/upload
   │   FormData {
   │     "session_id": "abc123",
   │     "file": <PDF or TXT file>
   │   }
   │
   ▼
2. Validate File
   │
   ├─▶ Check content-type (PDF/TXT)
   ├─▶ Get/Create session
   │
   ▼
3. Extract Text
   │
   ├─▶ If PDF: Use PyPDF to extract text from all pages
   ├─▶ If TXT: Decode UTF-8 text
   │
   ▼
4. Chunk Text
   │
   ├─▶ Split into chunks (1000 chars default)
   ├─▶ Maintain overlap (200 chars default)
   │   This preserves context at chunk boundaries
   │
   ▼
5. Generate Embeddings
   │
   ├─▶ For each chunk:
   │   └─▶ Generate 384-dimensional embedding
   │       using all-MiniLM-L6-v2 model
   │
   ▼
6. Store in Database
   │
   ├─▶ Create document record (documents table)
   ├─▶ Create chunk records with embeddings
   │   (document_chunks table with pgvector)
   │
   ├─▶ Create indexes for efficient similarity search
   │
   ▼
7. Return Response
   │
   └─▶ DocumentUploadResponse {
         "session_id": "abc123",
         "filename": "document.pdf",
         "file_type": "pdf",
         "chunks_created": 25,
         "message": "Document uploaded and processed successfully"
       }
```

## Technology Stack

### Backend Framework
- **FastAPI**: Modern Python web framework for building APIs
  - Automatic request/response validation
  - Interactive API documentation (Swagger UI, ReDoc)
  - ASGI support for async operations

### Language Models & Embeddings
- **LangChain**: Framework for building LLM applications
  - Supports multiple LLM providers
  - Message history management
  - Prompt templating

- **LangChain Integrations**:
  - `langchain-openai`: OpenAI API integration (GPT-3.5-turbo)
  - `langchain-google-genai`: Google Gemini integration
  - `langchain-anthropic`: Anthropic Claude integration

- **Sentence Transformers**: Generate text embeddings
  - Model: all-MiniLM-L6-v2 (384-dimensional)
  - Lightweight and efficient for RAG

### Database & Vector Store
- **PostgreSQL 14+**: Relational database for structured data
  - Sessions, messages, documents metadata

- **pgvector**: PostgreSQL extension for vector similarity search
  - Store and query 384-dimensional embeddings
  - Efficient similarity search using distance metrics

### Document Processing
- **PyPDF**: PDF text extraction
- **python-docx**: DOCX file support (planned)
- **Unstructured**: Advanced document processing

### ORM & Data Validation
- **SQLAlchemy 2.0**: Database ORM
- **Pydantic 2.9**: Request/response data validation
- **Pydantic Settings**: Configuration management

## Key Features

### 1. Session Management
- Each conversation is isolated in a session
- Sessions store all related messages and documents
- Support for custom session IDs
- Cascade delete: Deleting a session removes all related data

### 2. Retrieval Augmented Generation (RAG)
- Document upload and text extraction
- Intelligent chunking with overlap for context preservation
- Vector similarity search in pgvector
- Context injection into LLM prompts
- Conversation history awareness

### 3. Multi-Provider LLM Support
- **OpenAI**: gpt-3.5-turbo model
- **Google Gemini**: gemini-pro model
- **Anthropic**: claude-3-sonnet model
- Configurable via environment variables
- Requires corresponding API key

### 4. Conversation History
- All messages stored in database
- Chronological ordering for context retrieval
- Last 10 messages included in prompt (configurable)
- Full history accessible via API

## API Endpoints Summary

### Chat Endpoints
- `POST /api/chat` - Send message to chatbot
- `GET /` - Health check

### Document Endpoints
- `POST /api/documents/upload` - Upload PDF/TXT for RAG context
- `GET /api/documents/list/{session_id}` - List documents in session

### Session Endpoints
- `POST /api/sessions/` - Create new session
- `GET /api/sessions/` - List all sessions
- `GET /api/sessions/{session_id}` - Get session details
- `GET /api/sessions/{session_id}/history` - Get conversation history
- `DELETE /api/sessions/{session_id}` - Delete session

## Database Schema Design

### Sessions Table
Stores chat session metadata
- Primary session identifier
- Timestamp tracking for session lifecycle

### Messages Table
Stores conversation history
- Links to sessions for segregation
- Tracks role (user/assistant) for context
- Timestamp for message ordering

### Documents Table
Stores uploaded file metadata
- Document filename and type
- Full text content (optional compression)
- Links to session for organization

### Document Chunks Table
Stores processed document segments with embeddings
- Uses pgvector for efficient similarity search
- Includes chunk index for ordering
- 384-dimensional embeddings for semantic search

## Performance Considerations

1. **Vector Similarity Search**
   - Indexed on document_id for fast filtering
   - pgvector optimizes for cosine/L2/inner product distances
   - Top-K retrieval (default: 3 chunks) balances speed and quality

2. **Chunking Strategy**
   - 1000 character chunks with 200 character overlap
   - Overlap preserves context at boundaries
   - Configurable via environment variables

3. **Batch Processing**
   - Embeddings generated in batches for efficiency
   - Sentence Transformers uses GPU acceleration if available

4. **Database Indexing**
   - Session_id indexed for fast lookups
   - Message created_at indexed for sorting
   - Document_id indexed for chunk queries

## Error Handling

- Comprehensive exception handling in all endpoints
- Specific HTTP status codes for different error types
- Detailed error logging for debugging
- User-friendly error messages in responses

## Security Considerations

- CORS enabled for development (configure for production)
- API key validation before LLM initialization
- File type validation for document uploads
- Database connection using credentials from environment
- SQL injection prevention through SQLAlchemy ORM

## Deployment

### Docker
- Multi-container setup with docker-compose
- PostgreSQL with pgvector pre-configured
- Environment variable configuration
- Health checks for service availability

### Environment Configuration
- `.env` file for local development
- Support for different LLM providers
- Database connection pooling
- Configurable chunk sizes and overlap

## Future Enhancements

1. User authentication and authorization
2. Rate limiting
3. Advanced logging and monitoring
4. Caching mechanisms for embeddings
5. More document format support (DOCX, PPT, etc.)
6. Streaming responses for long generations
7. Admin dashboard for session management
8. Analytics and usage tracking
