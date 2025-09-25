#!/usr/bin/env python3
"""
Test script for Ollama Cloud API connection
"""

import os
import base64
from pathlib import Path
from ollama import Client

# Configuration
OLLAMA_MODEL = "gpt-oss:120b"
API_KEY = "fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg"

def test_basic_connection():
    """Test basic text-only connection to Ollama Cloud"""
    print("🔄 Testing basic Ollama Cloud connection...")

    try:
        client = Client(
            host="https://ollama.com",
            headers={'Authorization': f'Bearer {API_KEY}'}
        )

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Respond with a simple greeting."
            },
            {
                "role": "user",
                "content": "Hello, are you working?"
            }
        ]

        print(f"📡 Using model: {OLLAMA_MODEL}")
        print(f"🔑 API Key: {API_KEY[:20]}...")

        response_text = ""
        for part in client.chat(OLLAMA_MODEL, messages=messages, stream=True):
            if 'message' in part and 'content' in part['message']:
                response_text += part['message']['content']

        print(f"✅ Success! Response: {response_text}")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_vision_capabilities():
    """Test vision capabilities with a simple image"""
    print("\n🔄 Testing vision capabilities...")

    try:
        # Create a simple test image (1x1 red pixel)
        from PIL import Image
        import io

        # Create a small test image
        img = Image.new('RGB', (100, 100), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        client = Client(
            host="https://ollama.com",
            headers={'Authorization': f'Bearer {API_KEY}'}
        )

        messages = [
            {
                "role": "system",
                "content": "You are a vision AI. Describe what you see in the image."
            },
            {
                "role": "user",
                "content": "What color is this image?",
                "images": [image_base64]
            }
        ]

        response_text = ""
        for part in client.chat(OLLAMA_MODEL, messages=messages, stream=True):
            if 'message' in part and 'content' in part['message']:
                response_text += part['message']['content']

        print(f"✅ Vision test success! Response: {response_text}")
        return True

    except Exception as e:
        print(f"❌ Vision test error: {e}")
        return False

def test_alternative_models():
    """Test if other models are available"""
    print("\n🔄 Testing alternative models...")

    alternative_models = [
        "llama3.2-vision:11b",
        "llava:latest",
        "bakllava:latest",
        "llama3.2:latest"
    ]

    client = Client(
        host="https://ollama.com",
        headers={'Authorization': f'Bearer {API_KEY}'}
    )

    for model in alternative_models:
        try:
            print(f"Testing {model}...")
            messages = [{"role": "user", "content": "Hello"}]

            response_text = ""
            for part in client.chat(model, messages=messages, stream=True):
                if 'message' in part and 'content' in part['message']:
                    response_text += part['message']['content']

            print(f"✅ {model} works! Response: {response_text[:50]}...")
            return model

        except Exception as e:
            print(f"❌ {model} failed: {e}")
            continue

    return None

def test_api_endpoints():
    """Test different API endpoints"""
    print("\n🔄 Testing API endpoints...")

    import requests

    endpoints_to_test = [
        "https://ollama.com/api/chat",
        "https://api.ollama.com/api/chat",
        "https://ollama.cloud/api/chat"
    ]

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    test_payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": "test"}],
        "stream": False
    }

    for endpoint in endpoints_to_test:
        try:
            print(f"Testing endpoint: {endpoint}")
            response = requests.post(endpoint, json=test_payload, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Endpoint {endpoint} works!")
                return endpoint
            else:
                print(f"❌ Response: {response.text[:200]}")
        except Exception as e:
            print(f"❌ Endpoint {endpoint} failed: {e}")

    return None

if __name__ == "__main__":
    print("🧪 Ollama Cloud API Troubleshooting")
    print("=" * 50)

    # Test basic connection
    basic_works = test_basic_connection()

    # Test vision if basic works
    if basic_works:
        vision_works = test_vision_capabilities()
    else:
        # Try alternative models
        working_model = test_alternative_models()
        if working_model:
            print(f"\n💡 Suggestion: Use model '{working_model}' instead of '{OLLAMA_MODEL}'")
        else:
            # Try different endpoints
            working_endpoint = test_api_endpoints()
            if working_endpoint:
                print(f"\n💡 Suggestion: Use endpoint '{working_endpoint}'")

    print("\n📋 Troubleshooting Summary:")
    print("1. Check if API key is valid and has sufficient credits")
    print("2. Verify the model name is correct")
    print("3. Check if vision capabilities are included in your plan")
    print("4. Review API documentation for any recent changes")
    print("5. Consider using a fallback model or local Ollama installation")