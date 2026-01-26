# AI Chatbot Backend with RAG

An intelligent chatbot backend that lets you have conversations powered by AI, with the ability to upload documents for better context. Built with FastAPI, LangChain, and PostgreSQL.

![Architecture](architecture.svg)

## What Can It Do?

- 💬 **Smart Conversations**: Chat with AI models from OpenAI, Google, or Anthropic
- 📄 **Document Understanding**: Upload PDFs or text files and ask questions about them
- 🧠 **Context-Aware**: The bot remembers your conversation and uses it for better responses
- 🔄 **Session Management**: Keep different conversations separate with unique sessions
- 🚀 **Easy Setup**: Get everything running with just one Docker command
- 🔍 **Vector Search**: Uses embeddings and pgvector for smart document retrieval

## How It's Built

Here's the basic flow of the application:

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

## What You'll Need

**Easiest way (Docker):**
- Docker Desktop or Docker Engine 20.10+
- Docker Compose 2.0+

**Or if you prefer local setup:**
- Python 3.11 or higher
- PostgreSQL 14+ with the pgvector extension
- pip for installing Python packages

## Getting Started (The Easy Way - Docker)

### Step 1: Grab the Code

```bash
git clone https://github.com/Austinhere7/backend-ai-chatbot-project-bnglr.git
cd backend-ai-chatbot-project-bnglr
```

### Step 2: Set Up Your API Keys

First, create your environment file:

```bash
cp .env.example .env
```

Then open the `.env` file in any text editor and add your API key:

```bash
nano .env  # or use notepad, vim, whatever you like
```

**Here's what you need to configure:**

```env
# Pick which AI service you want to use
LLM_PROVIDER=openai  # can be: openai, gemini, or anthropic

# Then add your API key (only need one based on what you picked above)
OPENAI_API_KEY=sk-your-key-here
# GOOGLE_API_KEY=your-key-here  
# ANTHROPIC_API_KEY=your-key-here
```

### Step 3: Fire It Up!

This is where the magic happens. One command does it all:

```bash
docker-compose up
```

Wait for it to finish (first time takes a while as it downloads everything). You'll know it's ready when you see:
```
chatbot_backend  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

Your chatbot is now live at **http://localhost:8000**! 🎉

### Step 4: Make Sure It's Working

Quick test in your browser or terminal:

```bash
curl http://localhost:8000
```

You should get back something like:
```json
{
  "message": "AI Chatbot API is running",
  "version": "1.0.0",
  "llm_provider": "openai"
}
```

## Setting Up Locally (Without Docker)

If you prefer running things directly on your machine, here's how.

### 1. Install PostgreSQL with pgvector

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Install pgvector extension
cd /tmp
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

**macOS (using Homebrew):**
```bash
brew install postgresql
brew install pgvector
```

### 2. Set Up the Database

```bash
# Start PostgreSQL
sudo service postgresql start  # Linux
# or
brew services start postgresql  # Mac

# Create your database
sudo -u postgres psql
```

In the PostgreSQL prompt, run:
```sql
CREATE DATABASE chatbot_db;
CREATE USER chatbot_user WITH PASSWORD 'chatbot_password';
GRANT ALL PRIVILEGES ON DATABASE chatbot_db TO chatbot_user;
\q
```

### 3. Install the Application

```bash
git clone https://github.com/Austinhere7/backend-ai-chatbot-project-bnglr.git
cd backend-ai-chatbot-project-bnglr

# Set up a virtual environment (keeps things clean)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install everything you need
pip install -r requirements.txt
```

### 4. Configure Your Settings

```bash
cp .env.example .env
# Edit .env with your API keys and database settings
```

### 5. Initialize the Database

```bash
python init_db.py
```

### 6. Start the Server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Your API is now running at **http://localhost:8000**

## Time to Play! Testing Your Chatbot

### The Easiest Way: Use the Built-in Interface

Once your server is running, just open **http://localhost:8000/docs** in your browser. You'll see a nice interactive interface where you can test everything.

#### Let's Create a Chat Session

1. Look for **POST /api/sessions/** in the docs page
2. Click it, then click **"Try it out"**
3. Hit **"Execute"**
4. Copy the `session_id` you get back - you'll need it!

Example response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-24T10:30:00.000Z"
}
```

#### Now Chat With the AI!

1. Find **POST /api/chat/**
2. Click **"Try it out"**
3. Paste this in the request body (use your own session_id):
   ```json
   {
     "session_id": "your-session-id-here",
     "message": "Hi! Can you explain what machine learning is?"
   }
   ```
4. Click **"Execute"**
5. Watch the AI respond!

#### Want to Upload a Document?

1. Go to **POST /api/documents/upload**
2. Click **"Try it out"**
3. Enter your `session_id`
4. Choose a PDF or text file
5. Click **"Execute"**

Now you can ask questions about your document, and the bot will use it for context!

#### Check Your Conversation History

1. Find **GET /api/sessions/{session_id}/messages**
2. Click **"Try it out"**
3. Paste your `session_id`
4. Click **"Execute"**

You'll see your entire conversation!

### Using Command Line? Here's How

If you're more comfortable with the terminal, here are the commands:

#### Create a Session
```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Upload a Document
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "session_id=YOUR_SESSION_ID" \
  -F "file=@/path/to/your/document.pdf"
```

#### Send a Message
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "What does the document say about AI?"
  }'
```

#### Get Chat History
```bash
curl http://localhost:8000/api/sessions/YOUR_SESSION_ID/messages
```

### Using PowerShell (Windows)

```powershell
# Create a session
$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/sessions/" -ContentType "application/json"
$sessionId = $response.session_id

# Send a message
$body = @{
    session_id = $sessionId
    message = "Tell me about quantum computing"
} | ConvertTo-Json

$chatResponse = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/chat/" -ContentType "application/json" -Body $body
Write-Host $chatResponse.assistant_message
```

### Testing with Python

Want to write a quick script? Here's a starter:

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a session
session = requests.post(f"{BASE_URL}/api/sessions/").json()
session_id = session["session_id"]

# Chat with the bot
response = requests.post(
    f"{BASE_URL}/api/chat/",
    json={"session_id": session_id, "message": "What is AI?"}
)
print(response.json()["assistant_message"])
```

## How Does It Actually Work?

When you send a message, here's what happens behind the scenes:

1. **You create a session** - This keeps your conversations organized
2. **You upload documents** (optional) - They get split into chunks and converted to embeddings
3. **You send a message** - The system searches for relevant document chunks
4. **Context building** - Your chat history + relevant document chunks are combined
5. **AI generates response** - The LLM uses all this context to give you a smart answer
6. **Everything gets saved** - Your messages are stored for future context

It's called RAG (Retrieval Augmented Generation) - fancy term for "AI with better memory and context"!

## Running Into Issues?

### "Connection refused"
- Make sure Docker is running: `docker-compose ps`
- Check if something else is using port 8000

### "Database won't connect"
- Give PostgreSQL a few seconds to start up
- Check logs: `docker-compose logs chatbot_db`

### "API key not working"
- Double-check your `.env` file
- Make sure you're using the right key for the provider you selected
- Verify you have API credits left

### "Document upload failed"
- Currently supports PDF and TXT files only
- Keep files under 10MB for best results
- Make sure you're using a valid session_id

### Want to see what's happening?
```bash
# Watch logs in real-time
docker-compose logs -f

# Just the backend
docker-compose logs chatbot_backend

# Just the database
docker-compose logs chatbot_db
```

## Configuration Options

You can customize these in your `.env` file:

| Setting | What It Does | Required? | Default |
|---------|-------------|-----------|---------|
| `DATABASE_URL` | Where to find your PostgreSQL database | Yes | `postgresql://chatbot_user:chatbot_password@localhost:5432/chatbot_db` |
| `LLM_PROVIDER` | Which AI service to use (openai, gemini, or anthropic) | Yes | `openai` |
| `OPENAI_API_KEY` | Your OpenAI API key | Only if using OpenAI | - |
| `GOOGLE_API_KEY` | Your Google API key for Gemini | Only if using Gemini | - |
| `ANTHROPIC_API_KEY` | Your Anthropic API key for Claude | Only if using Anthropic | - |
| `APP_HOST` | What address to run the server on | No | `0.0.0.0` |
| `APP_PORT` | What port to use | No | `8000` |
| `EMBEDDING_MODEL` | Which model to use for embeddings | No | `all-MiniLM-L6-v2` |
| `CHUNK_SIZE` | How many characters per document chunk | No | `1000` |
| `CHUNK_OVERLAP` | How much chunks should overlap | No | `200` |


## What's Inside? Project Structure

```
backend-ai-chatbot-project-bnglr/
├── app/
│   ├── api/                    # All the API endpoints
│   │   ├── chat.py            # Handles chat messages
│   │   ├── documents.py       # Handles file uploads
│   │   └── sessions.py        # Manages sessions
│   ├── config/                # Configuration stuff
│   │   ├── database.py        # Database connection
│   │   └── settings.py        # App settings
│   ├── models/                # Data models
│   │   ├── models.py          # Database tables
│   │   └── schemas.py         # API request/response formats
│   ├── services/              # The business logic
│   │   ├── llm_service.py     # Talks to AI services
│   │   ├── embedding_service.py # Creates embeddings
│   │   ├── document_service.py  # Processes documents
│   │   └── rag_service.py     # RAG magic happens here
│   └── main.py                # The main app
├── init_db.py                 # Sets up the database
├── requirements.txt           # Python packages needed
├── Dockerfile                 # How to build the Docker image
├── docker-compose.yml         # Orchestrates everything
├── .env.example              # Example environment file
└── README.md                 # You're reading it!
```

## The Database Tables

**sessions** - Keeps track of different conversations
- Each session gets a unique ID
- Timestamps for when it was created/updated

**messages** - All the chat messages
- Links to a session
- Stores who said it (user or AI)
- The actual message content

**documents** - Files you've uploaded
- Associated with a session
- Original filename and type
- The full text content

**document_chunks** - Document pieces with embeddings
- Each chunk from a document
- The text chunk itself
- Vector embedding for similarity search

## License

MIT License - feel free to use this however you'd like!
