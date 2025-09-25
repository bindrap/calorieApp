#!/usr/bin/env python3
"""
Debug Ollama API issues
"""

import requests
from ollama import Client
import json

# Configuration
OLLAMA_MODEL = "gpt-oss:120b"
API_KEY = "fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg"

def test_different_approaches():
    print("🔍 Debugging Ollama API Connection")
    print("=" * 50)

    # Test 1: Direct requests to different endpoints
    endpoints = [
        "https://ollama.com/api/chat",
        "https://api.ollama.com/api/chat",
        "https://ollama.com/api/generate",
        "https://api.ollama.com/api/generate"
    ]

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    test_payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": False
    }

    for endpoint in endpoints:
        try:
            print(f"\n🔄 Testing endpoint: {endpoint}")
            response = requests.post(endpoint, json=test_payload, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")

            if response.status_code == 200:
                print("✅ Success!")
                break
        except Exception as e:
            print(f"❌ Failed: {e}")

    # Test 2: Ollama client with different configurations
    print(f"\n🔄 Testing Ollama Client approaches...")

    hosts_to_try = [
        "https://ollama.com",
        "https://api.ollama.com",
        "http://ollama.com",
    ]

    for host in hosts_to_try:
        try:
            print(f"\nTrying host: {host}")
            client = Client(host=host)

            # Try without auth first
            try:
                response = ""
                for part in client.chat(OLLAMA_MODEL, messages=[{"role": "user", "content": "test"}], stream=True):
                    response += part.get('message', {}).get('content', '')
                    break
                print(f"✅ No auth worked: {response[:50]}")
                break
            except:
                pass

            # Try with auth in headers
            client = Client(
                host=host,
                headers={'Authorization': f'Bearer {API_KEY}'}
            )

            response = ""
            for part in client.chat(OLLAMA_MODEL, messages=[{"role": "user", "content": "test"}], stream=True):
                response += part.get('message', {}).get('content', '')
                break
            print(f"✅ Auth headers worked: {response[:50]}")
            break

        except Exception as e:
            print(f"❌ Failed with {host}: {e}")

    # Test 3: Check available models
    print(f"\n🔄 Checking available models...")
    try:
        response = requests.get("https://ollama.com/api/tags", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"Available models: {[m.get('name', 'unknown') for m in models[:5]]}")
        else:
            print(f"Model list failed: {response.status_code}")
    except Exception as e:
        print(f"Model check failed: {e}")

if __name__ == "__main__":
    test_different_approaches()