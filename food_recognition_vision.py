#!/usr/bin/env python3
"""
Fixed Food Recognition Module
Uses Ollama Cloud API to analyze food images and identify food items
"""

import os
import base64
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
import io
import requests

# Configuration from CLAUDE.md
OLLAMA_MODEL = "gpt-oss:120b"
API_KEY = "fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg"

class FoodRecognizer:
    """Handles food recognition from images using Ollama Cloud"""

    def __init__(self, model: str = OLLAMA_MODEL, api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY", API_KEY)

        # Base URL for Ollama Cloud
        self.base_url = "https://ollama.com"

        # Headers for authentication
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze food image and return recognition results
        """
        try:
            print(f"🔄 Analyzing image: {image_path}")

            # Load and process image
            image_data = self._prepare_image(image_path)
            print("✅ Image processed successfully")

            # Try direct API approach first
            result = self._analyze_with_direct_api(image_data)

            if result:
                print("✅ Food recognition successful")
                return result
            else:
                print("⚠️ Falling back to text-only analysis")
                return self._fallback_text_analysis(image_path)

        except Exception as e:
            print(f"❌ Food recognition failed: {e}")
            logging.error(f"Food recognition failed for {image_path}: {e}")
            return self._create_fallback_result(f"Error: {str(e)}")

    def _prepare_image(self, image_path: str) -> str:
        """Prepare image for API call"""
        try:
            with Image.open(image_path) as img:
                # Resize image if too large
                max_size = (512, 512)  # Smaller for API efficiency
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Convert to RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=75)
                image_bytes = buffer.getvalue()

                return base64.b64encode(image_bytes).decode('utf-8')

        except Exception as e:
            raise Exception(f"Image processing failed: {str(e)}")

    def _analyze_with_direct_api(self, image_data: str) -> Optional[Dict]:
        """Try direct API call with image"""
        try:
            # Method 1: Try with requests directly
            url = f"{self.base_url}/api/chat"

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a food recognition expert. Analyze the image and return ONLY a JSON response with this exact structure:
{
    "primary_food": "main food name",
    "all_foods": ["food1", "food2"],
    "confidence": 0.85,
    "estimated_weight_grams": 150,
    "description": "what you see"
}

Be precise with food names. Estimate weight based on visual cues."""
                    },
                    {
                        "role": "user",
                        "content": "Analyze this food image and identify what food items you see.",
                        "images": [image_data]
                    }
                ],
                "stream": False
            }

            response = requests.post(url, json=payload, headers=self.headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                content = data.get('message', {}).get('content', '')
                return self._parse_recognition_response(content)
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"❌ Direct API failed: {e}")
            return None

    def _fallback_text_analysis(self, image_path: str) -> Dict:
        """Fallback to text-only analysis using filename and basic recognition"""
        try:
            # Use the ollama client for text-only analysis
            from ollama import Client

            client = Client(
                host=self.base_url,
                headers={'Authorization': f'Bearer {self.api_key}'}
            )

            # Extract potential food info from filename
            filename = Path(image_path).stem.lower()

            messages = [
                {
                    "role": "system",
                    "content": """You are a food identification expert. Based on the filename or description provided, suggest what food this might be and provide nutritional estimates. Respond in JSON format:
{
    "primary_food": "food name",
    "all_foods": ["food1"],
    "confidence": 0.3,
    "estimated_weight_grams": 100,
    "description": "estimated based on filename"
}"""
                },
                {
                    "role": "user",
                    "content": f"A food image was uploaded with filename: {filename}. What food might this be?"
                }
            ]

            response_text = ""
            for part in client.chat(self.model, messages=messages, stream=True):
                if 'message' in part and 'content' in part['message']:
                    response_text += part['message']['content']

            return self._parse_recognition_response(response_text)

        except Exception as e:
            print(f"❌ Fallback analysis failed: {e}")
            return self._create_fallback_result("Fallback analysis failed")

    def _parse_recognition_response(self, response: str) -> Dict:
        """Parse the JSON response"""
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1

            if start != -1 and end > start:
                json_str = response[start:end]
                result = json.loads(json_str)

                # Validate and clean result
                return {
                    'primary_food': result.get('primary_food', 'Unknown food'),
                    'all_foods': result.get('all_foods', [result.get('primary_food', 'Unknown food')]),
                    'confidence': min(max(float(result.get('confidence', 0.5)), 0.0), 1.0),
                    'estimated_weight': max(int(result.get('estimated_weight_grams', 100)), 1),
                    'portion_size': result.get('portion_size', '1 serving'),
                    'description': result.get('description', 'Food item detected')
                }
            else:
                raise ValueError("No valid JSON found in response")

        except Exception as e:
            print(f"⚠️ JSON parsing failed: {e}")
            print(f"Raw response: {response[:200]}...")
            return self._create_fallback_result(response)

    def _create_fallback_result(self, response: str) -> Dict:
        """Create a basic result when other methods fail"""
        # Try to extract food names from text
        response_lower = response.lower()

        common_foods = [
            'pizza', 'burger', 'sandwich', 'salad', 'pasta', 'rice', 'chicken', 'beef',
            'fish', 'vegetables', 'fruit', 'apple', 'banana', 'bread', 'cheese',
            'eggs', 'soup', 'noodles', 'potato', 'fries'
        ]

        detected_foods = []
        for food in common_foods:
            if food in response_lower:
                detected_foods.append(food.title())

        primary_food = detected_foods[0] if detected_foods else "Unknown Food"

        return {
            'primary_food': primary_food,
            'all_foods': detected_foods or [primary_food],
            'confidence': 0.2,  # Low confidence for fallback
            'estimated_weight': 100,
            'portion_size': '1 serving',
            'description': f"Basic detection: {response[:100]}..." if response else "Unable to analyze image"
        }

    def test_connection(self) -> bool:
        """Test if the API connection is working"""
        try:
            from ollama import Client

            client = Client(
                host=self.base_url,
                headers={'Authorization': f'Bearer {self.api_key}'}
            )

            messages = [{"role": "user", "content": "Hello, test connection"}]

            response = ""
            for part in client.chat(self.model, messages=messages, stream=True):
                if 'message' in part and 'content' in part['message']:
                    response += part['message']['content']
                    break  # Just test first response

            return len(response) > 0

        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False