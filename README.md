# AI Chatbot Backend with RAG

An intelligent chatbot backend that lets you have conversations powered by AI, with the ability to upload documents for better context. Built with FastAPI, LangChain, and PostgreSQL.

![Architecture](architecture.svg)

## What Can It Do?

- 💬 **Smart Conversations**: Chat with OpenAI or Gemini models
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
│  │ (OpenAI/Gemini) │               │
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
# Choose your provider (openai or gemini)
LLM_PROVIDER=gemini

# Add your provider API key
GOOGLE_API_KEY=your-gemini-key-here
# OPENAI_API_KEY=sk-your-key-here
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
  "llm_provider": "gemini"
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

There are **two ways** to test your chatbot. Pick whichever you prefer! 👇

---

## 🌐 Method 1: Interactive API Documentation (Easiest!)

This is the most beginner-friendly way. No command line needed!

**Step 1: Open the Interactive Docs**
- Just visit: **http://localhost:8000/docs** in your browser
- You'll see a beautiful interface with all API endpoints listed

**Step 2: Create a Chat Session**

1. Scroll down and find **POST /api/sessions/**
2. Click on it to expand it
3. Click the blue **"Try it out"** button
4. Click the big **"Execute"** button (no parameters needed)
5. Scroll down to see the response with your `session_id`

Example response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-24T10:30:00.000Z"
}
```

**💾 Copy your session_id - you'll need it for everything else!**

**Step 3: Send a Chat Message**

1. Find **POST /api/chat/**
2. Click **"Try it out"**
3. In the request body box, paste this (use YOUR session_id):
   ```json
   {
     "session_id": "550e8400-e29b-41d4-a716-446655440000",
     "message": "Hi! Can you explain what machine learning is?"
   }
   ```
4. Click **"Execute"**
5. See the AI's response below!

**Step 4: Upload a Document (Optional)**

1. Find **POST /api/documents/upload**
2. Click **"Try it out"**
3. In the `session_id` field, paste your session ID
4. In the `file` field, click "Choose Files" and pick a PDF or text file
5. Click **"Execute"**

Now your chatbot has context from your document!

**Step 5: Chat About Your Document**

1. Go back to **POST /api/chat/**
2. Click **"Try it out"**
3. Paste this (with YOUR session_id):
   ```json
   {
     "session_id": "550e8400-e29b-41d4-a716-446655440000",
     "message": "What is the main topic in the document I just uploaded?"
   }
   ```
4. Click **"Execute"**

The AI will answer based on your document!

**Step 6: View Your Chat History**

1. Find **GET /api/sessions/{session_id}/history**
2. Click **"Try it out"**
3. Paste your session_id in the field
4. Click **"Execute"**

You'll see all your messages from this session!

---

## 💻 Method 2: Command Line Testing

Prefer the terminal? Here's how to do everything with `curl` commands.

### On Linux/macOS:

**Create a Session:**
```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Send a Message:**
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your-session-id-here",
    "message": "Hello! What can you do?"
  }'
```

**Upload a Document:**
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "session_id=your-session-id-here" \
  -F "file=@sample_document.txt"
```

**Get Chat History:**
```bash
curl http://localhost:8000/api/sessions/your-session-id-here/history
```

**List All Sessions:**
```bash
curl http://localhost:8000/api/sessions/
```

**Delete a Session:**
```bash
curl -X DELETE http://localhost:8000/api/sessions/your-session-id-here
```

### On Windows PowerShell:

**Create a Session:**
```powershell
$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/sessions/" -ContentType "application/json"
$sessionId = $response.session_id
Write-Host "Session ID: $sessionId"
```

**Send a Message:**
```powershell
$body = @{
    session_id = "your-session-id-here"
    message = "Hello! What can you do?"
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/chat/" -ContentType "application/json" -Body $body
Write-Host $response.assistant_message
```

**Upload a Document:**
```powershell
$filePath = "C:\path\to\your\document.txt"
$sessionId = "your-session-id-here"

$form = @{
    session_id = $sessionId
    file = Get-Item -Path $filePath
}

$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/documents/upload" -Form $form
Write-Host $response | ConvertTo-Json
```

**Get Chat History:**
```powershell
$sessionId = "your-session-id-here"
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/sessions/$sessionId/history"
$response.messages | ForEach-Object { Write-Host "[$($_.role)] $($_.content)" }
```

### On Windows Command Prompt (cmd):

**Create a Session:**
```cmd
curl -X POST http://localhost:8000/api/sessions/ -H "Content-Type: application/json" -d "{}"
```

**Send a Message:**
```cmd
curl -X POST http://localhost:8000/api/chat/ -H "Content-Type: application/json" -d "{ \"session_id\": \"your-session-id-here\", \"message\": \"Hello!\" }"
```

---

## 🐍 Method 3: Python Script

Write a Python script to automate testing:

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Create a session
print("📝 Creating a chat session...")
session_resp = requests.post(f"{BASE_URL}/api/sessions/")
session_id = session_resp.json()["session_id"]
print(f"✓ Session created: {session_id}\n")

# 2. Upload a document
print("📄 Uploading a document...")
with open("sample_document.txt", "rb") as f:
    files = {"file": f}
    data = {"session_id": session_id}
    doc_resp = requests.post(f"{BASE_URL}/api/documents/upload", files=files, data=data)
    if doc_resp.status_code == 200:
        print("✓ Document uploaded successfully\n")
    else:
        print(f"✗ Upload failed: {doc_resp.text}\n")

# 3. Send a message
print("💬 Sending a message...")
chat_resp = requests.post(
    f"{BASE_URL}/api/chat/",
    json={
        "session_id": session_id,
        "message": "What is the document about?"
    }
)
response = chat_resp.json()
print(f"You: {response['user_message']}")
print(f"AI: {response['assistant_message']}\n")

# 4. Get conversation history
print("📜 Conversation history:")
history_resp = requests.get(f"{BASE_URL}/api/sessions/{session_id}/history")
messages = history_resp.json()["messages"]
for msg in messages:
    print(f"[{msg['role'].upper()}] {msg['content'][:80]}...")

# 5. Clean up
print("\n🗑️  Deleting session...")
requests.delete(f"{BASE_URL}/api/sessions/{session_id}")
print("✓ Session deleted")
```

Save this as `test_chatbot.py` and run it:
```bash
python test_chatbot.py
```

---

## 📊 Complete API Endpoints Reference

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/api/sessions/` | Create a new chat session |
| `GET` | `/api/sessions/` | List all sessions |
| `GET` | `/api/sessions/{session_id}` | Get details of a specific session |
| `DELETE` | `/api/sessions/{session_id}` | Delete a session |
| `GET` | `/api/sessions/{session_id}/history` | Get all messages in a session |
| `POST` | `/api/chat/` | Send a message and get AI response |
| `POST` | `/api/documents/upload` | Upload a document to a session |
| `GET` | `/api/documents/list/{session_id}` | List all documents in a session |

---

## 🎯 Quick Testing Workflow

### Using Interactive Docs (Recommended for beginners):
1. Open http://localhost:8000/docs
2. POST /api/sessions/ → Execute → Copy session_id
3. POST /api/chat/ → Enter session_id & message → Execute
4. See the response!

### Using Command Line:
```bash
# Create session and save the ID
curl -X POST http://localhost:8000/api/sessions/ -H "Content-Type: application/json" -d '{}' | grep -o '"session_id":"[^"]*' | cut -d'"' -f4

# Use that ID in your next command
curl -X POST http://localhost:8000/api/chat/ -H "Content-Type: application/json" -d '{"session_id": "YOUR_ID_HERE", "message": "Hello!"}'
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
| `LLM_PROVIDER` | Which LLM provider to use (`openai` or `gemini`) | Yes | `gemini` |
| `OPENAI_API_KEY` | Your OpenAI API key | Only if `LLM_PROVIDER=openai` | - |
| `GOOGLE_API_KEY` | Your Gemini API key | Only if `LLM_PROVIDER=gemini` | - |
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
