#!/usr/bin/env python3
"""Test script to verify Ollama Cloud API configuration"""

import os
from ollama import Client

# Your API key
API_KEY = "1728cbe73f944db7afa1a3c8f52d2f41.GzEVZ8ADdcDHwIxdbvKnqbXy"

print("Testing Ollama Cloud API configurations...\n")

# Test 1: Default ollama.chat() with environment variable
print("Test 1: Using environment variable")
os.environ['OLLAMA_API_KEY'] = API_KEY
try:
    import ollama
    response = ollama.chat(
        model='gpt-oss:120b-cloud',
        messages=[{'role': 'user', 'content': 'Say hi'}]
    )
    print(f"✅ Success with env var: {response['message']['content'][:50]}")
except Exception as e:
    print(f"❌ Failed with env var: {e}")

# Test 2: Client with cloud endpoint
print("\nTest 2: Using Client with ollama.com")
try:
    client = Client(
        host='https://ollama.com',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    response = client.chat(
        model='gpt-oss:120b-cloud',
        messages=[{'role': 'user', 'content': 'Say hi'}]
    )
    print(f"✅ Success with ollama.com: {response['message']['content'][:50]}")
except Exception as e:
    print(f"❌ Failed with ollama.com: {e}")

# Test 3: Client with api.ollama.com
print("\nTest 3: Using Client with api.ollama.com")
try:
    client = Client(
        host='https://api.ollama.com',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    response = client.chat(
        model='gpt-oss:120b-cloud',
        messages=[{'role': 'user', 'content': 'Say hi'}]
    )
    print(f"✅ Success with api.ollama.com: {response['message']['content'][:50]}")
except Exception as e:
    print(f"❌ Failed with api.ollama.com: {e}")

# Test 4: Client with cloud.ollama.com
print("\nTest 4: Using Client with cloud.ollama.com")
try:
    client = Client(
        host='https://cloud.ollama.com',
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    response = client.chat(
        model='gpt-oss:120b-cloud',
        messages=[{'role': 'user', 'content': 'Say hi'}]
    )
    print(f"✅ Success with cloud.ollama.com: {response['message']['content'][:50]}")
except Exception as e:
    print(f"❌ Failed with cloud.ollama.com: {e}")

print("\n✅ Testing complete!")
