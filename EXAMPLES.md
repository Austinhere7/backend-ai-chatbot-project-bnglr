# API Usage Examples

This document provides practical examples of using the AI Chatbot API.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Basic Usage](#basic-usage)
- [Advanced Examples](#advanced-examples)
- [Python Client](#python-client)
- [cURL Examples](#curl-examples)
- [Common Patterns](#common-patterns)

## Prerequisites

Make sure the server is running:
```bash
docker-compose up
# OR
python -m uvicorn app.main:app --reload
```

## Basic Usage

### 1. Create a Session

**cURL:**
```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Python:**
```python
import requests

response = requests.post("http://localhost:8000/api/sessions/", json={})
session_id = response.json()["session_id"]
print(f"Session ID: {session_id}")
```

### 2. Send a Chat Message

**cURL:**
```bash
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "Hello! How are you?"
  }'
```

**Python:**
```python
response = requests.post(
    "http://localhost:8000/api/chat/",
    json={
        "session_id": session_id,
        "message": "Hello! How are you?"
    }
)
print(response.json()["assistant_message"])
```

### 3. Upload a Document

**cURL:**
```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "session_id=YOUR_SESSION_ID" \
  -F "file=@/path/to/document.pdf"
```

**Python:**
```python
with open("document.pdf", "rb") as f:
    files = {"file": f}
    data = {"session_id": session_id}
    response = requests.post(
        "http://localhost:8000/api/documents/upload",
        data=data,
        files=files
    )
print(response.json())
```

### 4. Get Conversation History

**cURL:**
```bash
curl http://localhost:8000/api/sessions/YOUR_SESSION_ID/history
```

**Python:**
```python
response = requests.get(f"http://localhost:8000/api/sessions/{session_id}/history")
history = response.json()
for msg in history["messages"]:
    print(f"{msg['role']}: {msg['content']}")
```

## Advanced Examples

### Complete Workflow Example

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Create a session
session_response = requests.post(f"{BASE_URL}/api/sessions/", json={})
session_id = session_response.json()["session_id"]
print(f"Created session: {session_id}")

# 2. Upload a document
with open("research_paper.pdf", "rb") as f:
    upload_response = requests.post(
        f"{BASE_URL}/api/documents/upload",
        data={"session_id": session_id},
        files={"file": f}
    )
print(f"Uploaded document: {upload_response.json()['chunks_created']} chunks")

# 3. Ask questions about the document
questions = [
    "What is the main topic of this document?",
    "Can you summarize the key findings?",
    "What methodology was used?"
]

for question in questions:
    response = requests.post(
        f"{BASE_URL}/api/chat/",
        json={"session_id": session_id, "message": question}
    )
    answer = response.json()["assistant_message"]
    print(f"\nQ: {question}")
    print(f"A: {answer}")
    time.sleep(1)  # Rate limiting

# 4. Get full conversation history
history = requests.get(f"{BASE_URL}/api/sessions/{session_id}/history")
print(f"\nTotal messages in conversation: {len(history.json()['messages'])}")
```

### Multiple Document Upload

```python
import os

documents = ["doc1.pdf", "doc2.txt", "doc3.pdf"]

for doc in documents:
    with open(doc, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/documents/upload",
            data={"session_id": session_id},
            files={"file": f}
        )
        print(f"Uploaded {doc}: {response.json()['chunks_created']} chunks")
```

### Session Management

```python
# Create multiple sessions for different topics
sessions = {}

topics = ["python_help", "research_questions", "general_chat"]

for topic in topics:
    response = requests.post(f"{BASE_URL}/api/sessions/", json={})
    sessions[topic] = response.json()["session_id"]
    print(f"Created session for {topic}: {sessions[topic]}")

# Use different sessions
for topic, sid in sessions.items():
    response = requests.post(
        f"{BASE_URL}/api/chat/",
        json={
            "session_id": sid,
            "message": f"Let's discuss {topic}"
        }
    )
    print(f"{topic}: {response.json()['assistant_message']}")
```

## Python Client

Complete Python client class:

```python
import requests
from typing import Optional, Dict, List

class ChatbotClient:
    """Client for interacting with the AI Chatbot API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id: Optional[str] = None
    
    def create_session(self) -> str:
        """Create a new session."""
        response = requests.post(f"{self.base_url}/api/sessions/", json={})
        response.raise_for_status()
        self.session_id = response.json()["session_id"]
        return self.session_id
    
    def chat(self, message: str, session_id: Optional[str] = None) -> str:
        """Send a chat message."""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID. Create a session first.")
        
        response = requests.post(
            f"{self.base_url}/api/chat/",
            json={"session_id": sid, "message": message}
        )
        response.raise_for_status()
        return response.json()["assistant_message"]
    
    def upload_document(self, file_path: str, session_id: Optional[str] = None) -> Dict:
        """Upload a document."""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID. Create a session first.")
        
        with open(file_path, "rb") as f:
            response = requests.post(
                f"{self.base_url}/api/documents/upload",
                data={"session_id": sid},
                files={"file": f}
            )
        response.raise_for_status()
        return response.json()
    
    def get_history(self, session_id: Optional[str] = None) -> List[Dict]:
        """Get conversation history."""
        sid = session_id or self.session_id
        if not sid:
            raise ValueError("No session ID. Create a session first.")
        
        response = requests.get(f"{self.base_url}/api/sessions/{sid}/history")
        response.raise_for_status()
        return response.json()["messages"]
    
    def health_check(self) -> bool:
        """Check if the API is healthy."""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False

# Usage example
if __name__ == "__main__":
    client = ChatbotClient()
    
    # Check health
    if not client.health_check():
        print("API is not available!")
        exit(1)
    
    # Create session
    session_id = client.create_session()
    print(f"Session: {session_id}")
    
    # Upload document
    result = client.upload_document("sample_document.txt")
    print(f"Uploaded: {result['filename']}")
    
    # Chat
    response = client.chat("What are the key features mentioned?")
    print(f"Bot: {response}")
    
    # Get history
    history = client.get_history()
    print(f"Total messages: {len(history)}")
```

## cURL Examples

### Quick Test Script

Save this as `test.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "1. Health Check"
curl -s $BASE_URL/health | jq

echo -e "\n2. Create Session"
SESSION_ID=$(curl -s -X POST $BASE_URL/api/sessions/ -H "Content-Type: application/json" -d '{}' | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

echo -e "\n3. Upload Document"
curl -s -X POST $BASE_URL/api/documents/upload \
  -F "session_id=$SESSION_ID" \
  -F "file=@sample_document.txt" | jq

echo -e "\n4. Chat"
curl -s -X POST $BASE_URL/api/chat/ \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"What is this document about?\"}" | jq

echo -e "\n5. Get History"
curl -s $BASE_URL/api/sessions/$SESSION_ID/history | jq
```

Make it executable:
```bash
chmod +x test.sh
./test.sh
```

## Common Patterns

### Error Handling

```python
def safe_chat(client, message):
    """Chat with error handling."""
    try:
        response = client.chat(message)
        return response
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"Error: {e}")
    return None
```

### Streaming Conversations

```python
def interactive_chat(client):
    """Interactive chat session."""
    print("Chatbot ready! Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
        
        response = client.chat(user_input)
        print(f"Bot: {response}")
```

### Batch Processing

```python
def process_documents_batch(client, file_list):
    """Process multiple documents."""
    results = []
    for file_path in file_list:
        try:
            result = client.upload_document(file_path)
            results.append({"file": file_path, "success": True, "result": result})
        except Exception as e:
            results.append({"file": file_path, "success": False, "error": str(e)})
    return results
```

## Tips and Best Practices

1. **Always create a session first** before uploading documents or chatting
2. **Use the same session ID** for related conversations and documents
3. **Handle errors gracefully** - check response status codes
4. **Upload documents before asking questions** about them
5. **Respect rate limits** - add delays between requests if making many calls
6. **Keep session IDs** - they're needed for retrieving history

## Need Help?

- Check the [README.md](README.md) for setup instructions
- View API docs at http://localhost:8000/docs
- Report issues on GitHub
