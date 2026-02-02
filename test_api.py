"""
Comprehensive API testing script for the AI Chatbot Backend.

This script tests all API endpoints and validates the functionality:
- Health checks
- Session management (create, list, retrieve, delete)
- Document upload and listing
- Chat interactions
- Conversation history retrieval

Usage:
    python test_api.py

Requirements:
    - Backend server running (python -m uvicorn app.main:app)
    - Database initialized and running
    - Valid .env configuration with LLM API keys

Output:
    Detailed test results with pass/fail status for each endpoint
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional

BASE_URL = "http://localhost:8000"
TIMEOUT = 10  # seconds


class TestResult:
    """Container for test results."""
    
    def __init__(self):
        self.results = []
    
    def add(self, test_name: str, passed: bool, message: str = ""):
        """Add a test result."""
        self.results.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
    
    def print_summary(self):
        """Print test results summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        for result in self.results:
            status = "✓ PASS" if result["passed"] else "✗ FAIL"
            print(f"{status:8} {result['name']:40} {result['message']}")
        
        print("-"*70)
        print(f"Results: {passed}/{total} tests passed")
        print("="*70)
        
        return passed == total


def check_server_running():
    """Verify server is running."""
    print("Checking if server is running at " + BASE_URL + "...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        print("✓ Server is running\n")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to server: {str(e)}")
        print(f"  Please start the server first:\n")
        print(f"  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload\n")
        return False


def test_health_check():
    """Test the health check endpoint."""
    print("1. Testing health check...")
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
        data = response.json()
        print("✓ Root endpoint passed")
        print(f"  Message: {data.get('message')}")
        print(f"  LLM Provider: {data.get('llm_provider')}")
        return True
    else:
        print(f"✗ Root endpoint failed: {response.status_code}")
        return False


def test_create_session():
    """Test session creation."""
    print("\n3. Testing session creation...")
    response = requests.post(
        f"{BASE_URL}/api/sessions/",
        json={},
        timeout=TIMEOUT
    )
    if response.status_code == 200:
        data = response.json()
        print("✓ Session creation passed")
        print(f"  Session ID: {data['session_id']}")
        print(f"  Created at: {data['created_at']}")
        return data['session_id']
    else:
        print(f"✗ Session creation failed: {response.status_code}")
        return None


def test_list_sessions():
    """Test listing sessions."""
    print("\n4. Testing list sessions...")
    response = requests.get(
        f"{BASE_URL}/api/sessions/",
        timeout=TIMEOUT
    )
    if response.status_code == 200:
        data = response.json()
        print("✓ List sessions passed")
        print(f"  Total sessions: {len(data)}")
        return True
    else:
        print(f"✗ List sessions failed: {response.status_code}")
        return False


def test_get_session(session_id):
    """Test getting session details."""
    print("\n5. Testing get session details...")
    response = requests.get(
        f"{BASE_URL}/api/sessions/{session_id}",
        timeout=TIMEOUT
    )
    if response.status_code == 200:
        data = response.json()
        print("✓ Get session passed")
        print(f"  Messages: {data.get('message_count', 0)}")
        print(f"  Documents: {data.get('document_count', 0)}")
        return True
    else:
        print(f"✗ Get session failed: {response.status_code}")
        return False


def test_upload_document(session_id):
    """Test document upload."""
    print("\n6. Testing document upload...")
    
    # Create sample document content
    sample_content = b"""
    Artificial Intelligence and Machine Learning
    =============================================
    
    Artificial Intelligence (AI) refers to the capability of machines to perform tasks
    that typically require human intelligence.
    
    Machine Learning is a subset of AI that enables computers to learn from data
    without being explicitly programmed.
    
    Key Applications:
    - Natural Language Processing
    - Computer Vision
    - Recommendation Systems
    - Predictive Analytics
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/documents/upload",
            data={'session_id': session_id},
            files={'file': ('sample.txt', sample_content, 'text/plain')},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Document upload passed")
            print(f"  Filename: {data.get('filename')}")
            print(f"  Chunks created: {data.get('chunks_created', 0)}")
            return True
        else:
            print(f"✗ Document upload failed: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"✗ Document upload error: {str(e)}")
        return False


def test_list_documents(session_id):
    """Test listing documents."""
    print("\n7. Testing list documents...")
    response = requests.get(
        f"{BASE_URL}/api/documents/list/{session_id}",
        timeout=TIMEOUT
    )
    if response.status_code == 200:
        data = response.json()
        print("✓ List documents passed")
        docs = data.get('documents', [])
        print(f"  Documents: {len(docs)}")
        for doc in docs[:3]:
            print(f"    - {doc.get('filename')} ({doc.get('chunks_count')} chunks)")
        return True
    else:
        print(f"✗ List documents failed: {response.status_code}")
        return False


def test_chat(session_id):
    """Test chat endpoint."""
    print("\n8. Testing chat endpoint...")
    response = requests.post(
        f"{BASE_URL}/api/chat/",
        json={
            "session_id": session_id,
            "message": "What is artificial intelligence based on the documents?"
        },
        timeout=TIMEOUT
    )
    if response.status_code == 200:
        data = response.json()
        print("✓ Chat endpoint passed")
        print(f"  User: {data['user_message']}")
        print(f"  Assistant: {data['assistant_message'][:150]}...")
        return True
    else:
        print(f"✗ Chat endpoint failed: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        return False


def test_conversation_history(session_id):
    """Test getting conversation history."""
    print("\n9. Testing conversation history...")
    response = requests.get(
        f"{BASE_URL}/api/sessions/{session_id}/history",
        timeout=TIMEOUT
    )
    if response.status_code == 200:
        data = response.json()
        messages = data.get('messages', [])
        print("✓ Conversation history passed")
        print(f"  Total messages: {len(messages)}")
        for msg in messages[-3:]:  # Show last 3 messages
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '')[:80]
            print(f"    [{role}] {content}...")
        return True
    else:
        print(f"✗ Conversation history failed: {response.status_code}")
        return False


def test_delete_session(session_id):
    """Test deleting a session."""
    print("\n10. Testing delete session...")
    response = requests.delete(
        f"{BASE_URL}/api/sessions/{session_id}",
        timeout=TIMEOUT
    )
    if response.status_code == 200:
        print("✓ Delete session passed")
        return True
    else:
        print(f"✗ Delete session failed: {response.status_code}")
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🤖  AI CHATBOT BACKEND - API TEST SUITE")
    print("="*70 + "\n")
    
    # Check if server is running
    if not check_server_running():
        sys.exit(1)
    
    # Run tests
    tests_passed = 0
    tests_total = 0
    
    # Basic tests
    if test_health_check():
        tests_passed += 1
    tests_total += 1
    
    if test_root():
        tests_passed += 1
    tests_total += 1
    
    # Session and chat tests
    session_id = test_create_session()
    if session_id:
        tests_passed += 1
    tests_total += 1
    
    if test_list_sessions():
        tests_passed += 1
    tests_total += 1
    
    if session_id and test_get_session(session_id):
        tests_passed += 1
    tests_total += 1
    
    # Document tests
    if session_id and test_upload_document(session_id):
        tests_passed += 1
    tests_total += 1
    
    if session_id and test_list_documents(session_id):
        tests_passed += 1
    tests_total += 1
    
    # Chat tests
    if session_id and test_chat(session_id):
        tests_passed += 1
    tests_total += 1
    
    if session_id and test_conversation_history(session_id):
        tests_passed += 1
    tests_total += 1
    
    # Cleanup
    if session_id and test_delete_session(session_id):
        tests_passed += 1
    tests_total += 1
    
    # Print summary
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    print("="*70 + "\n")
    
    if tests_passed == tests_total:
        print("🎉 All tests passed! The API is working correctly.")
        sys.exit(0)
    else:
        print(f"⚠️  {tests_total - tests_passed} test(s) failed.")
        sys.exit(1)
