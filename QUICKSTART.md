# Quick Start Guide

Get the AI Chatbot running in 5 minutes!

## Prerequisites
- Docker and Docker Compose installed
- An API key from one of:
  - OpenAI (https://platform.openai.com/api-keys)
  - Google AI (https://makersuite.google.com/app/apikey)
  - Anthropic (https://console.anthropic.com/)

## Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Austinhere7/backend-ai-chatbot-project-bnglr.git
cd backend-ai-chatbot-project-bnglr
```

### 2. Configure API Key
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
nano .env
```

**For OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

**For Google Gemini:**
```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your-key-here
```

**For Anthropic:**
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-key-here
```

### 3. Start the Application
```bash
docker-compose up
```

Wait for the messages:
```
chatbot_backend  | INFO:     Application startup complete.
chatbot_backend  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Test the API

**Open a new terminal and run:**

```bash
# Test health
curl http://localhost:8000/health

# Create a session
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" -d '{}'

# You'll get a session_id like: "550e8400-e29b-41d4-a716-446655440000"
# Save it for the next commands!

# Upload a document
curl -X POST http://localhost:8000/api/documents/upload \
  -F "session_id=YOUR_SESSION_ID" \
  -F "file=@sample_document.txt"

# Chat with the bot
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "What are the key features mentioned in the document?"
  }'
```

### 5. View Interactive API Docs

Open your browser:
```
http://localhost:8000/docs
```

## Python Quick Test

Save this as `quick_test.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Create session
session = requests.post(f"{BASE_URL}/api/sessions/", json={}).json()
session_id = session["session_id"]
print(f"Created session: {session_id}")

# 2. Upload document
with open("sample_document.txt", "rb") as f:
    upload = requests.post(
        f"{BASE_URL}/api/documents/upload",
        data={"session_id": session_id},
        files={"file": f}
    ).json()
print(f"Uploaded: {upload['chunks_created']} chunks")

# 3. Chat
chat = requests.post(
    f"{BASE_URL}/api/chat/",
    json={
        "session_id": session_id,
        "message": "What are the key features?"
    }
).json()
print(f"\nBot: {chat['assistant_message']}")
```

Run it:
```bash
python quick_test.py
```

## Troubleshooting

**"Connection refused"**
- Wait a few more seconds for the server to start
- Check logs: `docker-compose logs backend`

**"API key error"**
- Verify your API key is correct in `.env`
- Make sure you selected the right LLM_PROVIDER

**Need to restart?**
```bash
docker-compose down
docker-compose up
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [EXAMPLES.md](EXAMPLES.md) for more usage examples
- Explore the API at http://localhost:8000/docs

## Support

Having issues? Check:
1. Docker is running: `docker --version`
2. Ports 5432 and 8000 are free
3. .env file exists and has valid API key
4. Internet connection is working

Enjoy your AI chatbot! 🤖
