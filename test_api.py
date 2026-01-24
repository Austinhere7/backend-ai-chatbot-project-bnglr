"""
Test script to verify basic functionality of the chatbot API.
Run this after starting the server to test all endpoints.
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint."""
    print("\n1. Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✓ Health check passed")
        print(f"  Response: {response.json()}")
        return True
    else:
        print(f"✗ Health check failed: {response.status_code}")
        return False


def test_root():
    """Test the root endpoint."""
    print("\n2. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("✓ Root endpoint passed")
        print(f"  Response: {response.json()}")
        return True
    else:
        print(f"✗ Root endpoint failed: {response.status_code}")
        return False


def test_create_session():
    """Test session creation."""
    print("\n3. Testing session creation...")
    response = requests.post(
        f"{BASE_URL}/api/sessions/",
        json={}
    )
    if response.status_code == 200:
        data = response.json()
        print("✓ Session creation passed")
        print(f"  Session ID: {data['session_id']}")
        return data['session_id']
    else:
        print(f"✗ Session creation failed: {response.status_code}")
        return None


def test_chat(session_id):
    """Test chat endpoint."""
    print("\n4. Testing chat endpoint...")
    response = requests.post(
        f"{BASE_URL}/api/chat/",
        json={
            "session_id": session_id,
            "message": "Hello! Can you introduce yourself?"
        }
    )
    if response.status_code == 200:
        data = response.json()
        print("✓ Chat endpoint passed")
        print(f"  User: {data['user_message']}")
        print(f"  Assistant: {data['assistant_message'][:100]}...")
        return True
    else:
        print(f"✗ Chat endpoint failed: {response.status_code}")
        print(f"  Error: {response.text}")
        return False


def test_get_session(session_id):
    """Test getting session details."""
    print("\n5. Testing get session...")
    response = requests.get(f"{BASE_URL}/api/sessions/{session_id}")
    if response.status_code == 200:
        data = response.json()
        print("✓ Get session passed")
        print(f"  Messages: {data['message_count']}")
        print(f"  Documents: {data['document_count']}")
        return True
    else:
        print(f"✗ Get session failed: {response.status_code}")
        return False


def test_conversation_history(session_id):
    """Test getting conversation history."""
    print("\n6. Testing conversation history...")
    response = requests.get(f"{BASE_URL}/api/sessions/{session_id}/history")
    if response.status_code == 200:
        data = response.json()
        print("✓ Conversation history passed")
        print(f"  Total messages: {len(data['messages'])}")
        for msg in data['messages']:
            print(f"    {msg['role']}: {msg['content'][:50]}...")
        return True
    else:
        print(f"✗ Conversation history failed: {response.status_code}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("AI Chatbot API Test Suite")
    print("=" * 60)
    
    # Test basic endpoints
    if not test_health_check():
        print("\n✗ Server is not running or not healthy!")
        print("  Please start the server with: docker-compose up")
        sys.exit(1)
    
    if not test_root():
        sys.exit(1)
    
    # Test session management
    session_id = test_create_session()
    if not session_id:
        sys.exit(1)
    
    # Test chat
    if not test_chat(session_id):
        print("\n⚠ Chat test failed. Please check:")
        print("  1. LLM_PROVIDER is set correctly in .env")
        print("  2. API key is valid for your provider")
        print("  3. Network connectivity is available")
    
    # Test session retrieval
    test_get_session(session_id)
    test_conversation_history(session_id)
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
