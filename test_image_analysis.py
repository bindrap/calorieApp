#!/usr/bin/env python3
"""
Test image analysis with Ollama API
"""

import requests
import base64
from PIL import Image
import io
import tempfile
import json

# Configuration
OLLAMA_MODEL = "gpt-oss:120b"
API_KEY = "fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg"

def create_simple_food_image():
    """Create a simple colored image"""
    # Create a simple image with text
    img = Image.new('RGB', (200, 200), color='orange')

    # Add some simple shapes to make it look like food
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)

    # Draw a simple plate-like circle
    draw.ellipse([20, 20, 180, 180], fill='white', outline='gray', width=3)

    # Draw some food-like elements (pizza slice shapes)
    draw.polygon([(100, 100), (140, 60), (160, 120)], fill='red')  # Tomato
    draw.polygon([(100, 100), (60, 60), (80, 120)], fill='yellow')  # Cheese
    draw.ellipse([90, 90, 110, 110], fill='brown')  # Center

    return img

def test_image_with_ollama():
    print("🧪 Testing Image Analysis with Ollama")
    print("=" * 45)

    # Create test image
    img = create_simple_food_image()

    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    print(f"✅ Created test image ({len(image_base64)} chars base64)")

    # Test different API approaches
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Method 1: Direct API with image
    print("\n🔄 Method 1: Direct API with images field")
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": "What do you see in this image? Describe it briefly.",
                    "images": [image_base64]
                }
            ],
            "stream": False
        }

        response = requests.post(
            "https://ollama.com/api/chat",
            json=payload,
            headers=headers,
            timeout=30
        )

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            content = data.get('message', {}).get('content', 'No content')
            print(f"✅ Response: {content}")
        else:
            print(f"❌ Error: {response.text}")

    except Exception as e:
        print(f"❌ Method 1 failed: {e}")

    # Method 2: Try with different model that might support vision
    print("\n🔄 Method 2: Try with different model")
    vision_models = ["qwen3-coder:480b", "deepseek-v3.1:671b"]

    for model in vision_models:
        try:
            print(f"Testing with {model}...")
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Describe what you see in this image.",
                        "images": [image_base64]
                    }
                ],
                "stream": False
            }

            response = requests.post(
                "https://ollama.com/api/chat",
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get('message', {}).get('content', 'No content')
                print(f"✅ {model} response: {content[:100]}...")
                break
            else:
                print(f"❌ {model} failed: {response.text[:100]}")

        except Exception as e:
            print(f"❌ {model} error: {e}")

    # Method 3: Text-only fallback test
    print("\n🔄 Method 3: Text-only fallback test")
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a food identification expert."
                },
                {
                    "role": "user",
                    "content": "I have an image of food that looks orange and round with some red and yellow elements, possibly pizza. What food might this be? Respond in JSON: {\"primary_food\": \"food name\", \"confidence\": 0.8}"
                }
            ],
            "stream": False
        }

        response = requests.post(
            "https://ollama.com/api/chat",
            json=payload,
            headers=headers,
            timeout=20
        )

        if response.status_code == 200:
            data = response.json()
            content = data.get('message', {}).get('content', 'No content')
            print(f"✅ Text fallback works: {content}")
        else:
            print(f"❌ Text fallback failed: {response.text}")

    except Exception as e:
        print(f"❌ Text fallback error: {e}")

if __name__ == "__main__":
    test_image_with_ollama()