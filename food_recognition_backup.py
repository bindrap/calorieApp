#!/usr/bin/env python3
"""
Food Recognition Module
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

from ollama import Client

# Configuration from CLAUDE.md
OLLAMA_MODEL = "gpt-oss:120b"
API_KEY = "fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg"

class FoodRecognizer:
    """Handles food recognition from images using Ollama Cloud"""

    def __init__(self, model: str = OLLAMA_MODEL, api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY", API_KEY)

        # Initialize Ollama client
        self.client = Client(
            host="https://ollama.com",
            headers={'Authorization': f'Bearer {self.api_key}'}
        )

    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze food image and return recognition results

        Args:
            image_path: Path to the food image

        Returns:
            Dict containing recognition results with keys:
            - primary_food: Main food item identified
            - all_foods: List of all food items detected
            - confidence: Confidence score (0.0-1.0)
            - estimated_weight: Estimated weight in grams
            - description: Detailed description
        """
        try:
            # Load and process image
            image_data = self._prepare_image(image_path)

            # Create prompt for food recognition
            messages = self._create_food_recognition_prompt(image_data)

            # Get response from Ollama
            response = self._call_ollama_vision(messages)

            # Parse and structure the response
            result = self._parse_recognition_response(response)

            return result

        except Exception as e:
            logging.error(f"Food recognition failed for {image_path}: {e}")
            raise Exception(f"Failed to analyze image: {str(e)}")

    def _prepare_image(self, image_path: str) -> str:
        """
        Prepare image for API call by resizing and encoding to base64
        """
        try:
            with Image.open(image_path) as img:
                # Resize image if too large (to save API costs)
                max_size = (1024, 1024)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                image_bytes = buffer.getvalue()

                return base64.b64encode(image_bytes).decode('utf-8')

        except Exception as e:
            raise Exception(f"Image processing failed: {str(e)}")

    def _create_food_recognition_prompt(self, image_data: str) -> List[Dict]:
        """Create the prompt messages for food recognition"""

        system_prompt = """You are a professional nutritionist and food identification expert.
        Analyze the food image and provide detailed information about the food items present.

        Your response must be in JSON format with these exact fields:
        {
            "primary_food": "main food item name",
            "all_foods": ["list", "of", "all", "food", "items"],
            "confidence": 0.95,
            "estimated_weight_grams": 150,
            "estimated_portion_size": "1 medium apple",
            "description": "Detailed description of what you see"
        }

        Rules:
        1. Be accurate and specific with food names
        2. Estimate portion size/weight as best as possible
        3. Confidence should be 0.0-1.0 (be honest about uncertainty)
        4. Include all visible food items, even small ones
        5. Use common food names that people would recognize
        6. If unsure about exact food, use broader categories (e.g., "mixed vegetables")
        7. Always provide valid JSON format
        """

        user_prompt = """Please analyze this food image and identify:
        1. What food items are present
        2. Estimated portion sizes/weights
        3. Your confidence in the identification
        4. Any other relevant details

        Provide your response in the exact JSON format specified."""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt,
                "images": [image_data]  # Base64 encoded image
            }
        ]

        return messages

    def _call_ollama_vision(self, messages: List[Dict]) -> str:
        """Call Ollama Cloud API with vision capabilities"""
        try:
            response_text = ""

            # Stream the response
            for part in self.client.chat(
                self.model,
                messages=messages,
                stream=True
            ):
                if 'message' in part and 'content' in part['message']:
                    response_text += part['message']['content']

            return response_text.strip()

        except Exception as e:
            logging.error(f"Ollama API call failed: {e}")
            raise Exception(f"API call failed: {str(e)}")

    def _parse_recognition_response(self, response: str) -> Dict:
        """Parse the JSON response from Ollama"""
        try:
            # Try to extract JSON from response (in case there's extra text)
            start = response.find('{')
            end = response.rfind('}') + 1

            if start != -1 and end > start:
                json_str = response[start:end]
                result = json.loads(json_str)

                # Validate required fields and add defaults if missing
                return {
                    'primary_food': result.get('primary_food', 'Unknown food'),
                    'all_foods': result.get('all_foods', [result.get('primary_food', 'Unknown food')]),
                    'confidence': float(result.get('confidence', 0.5)),
                    'estimated_weight': result.get('estimated_weight_grams', 100),
                    'portion_size': result.get('estimated_portion_size', 'Unknown portion'),
                    'description': result.get('description', 'Food item detected')
                }
            else:
                raise ValueError("No valid JSON found in response")

        except (json.JSONDecodeError, ValueError) as e:
            logging.warning(f"Could not parse JSON response: {e}")
            logging.warning(f"Raw response: {response}")

            # Fallback: create basic result from text analysis
            return self._create_fallback_result(response)

    def _create_fallback_result(self, response: str) -> Dict:
        """Create a basic result when JSON parsing fails"""
        # Simple text analysis to extract food names
        response_lower = response.lower()

        # Common food keywords to look for
        food_keywords = [
            'apple', 'banana', 'orange', 'bread', 'rice', 'chicken', 'beef',
            'pasta', 'pizza', 'salad', 'sandwich', 'burger', 'egg', 'fish',
            'vegetable', 'fruit', 'meat', 'cheese', 'milk', 'yogurt'
        ]

        detected_foods = []
        for keyword in food_keywords:
            if keyword in response_lower:
                detected_foods.append(keyword.title())

        primary_food = detected_foods[0] if detected_foods else "Unknown food"

        return {
            'primary_food': primary_food,
            'all_foods': detected_foods or [primary_food],
            'confidence': 0.3,  # Low confidence for fallback
            'estimated_weight': 100,  # Default weight
            'portion_size': '1 serving',
            'description': f"Detected from text analysis: {response[:200]}..."
        }

    def get_food_suggestions(self, partial_name: str) -> List[str]:
        """
        Get food name suggestions based on partial input
        (Can be enhanced with a proper food database later)
        """
        common_foods = [
            'Apple', 'Banana', 'Orange', 'Grapes', 'Strawberry',
            'Chicken Breast', 'Beef', 'Pork', 'Fish', 'Salmon',
            'Rice', 'Pasta', 'Bread', 'Quinoa', 'Oatmeal',
            'Broccoli', 'Carrots', 'Spinach', 'Tomato', 'Onion',
            'Milk', 'Cheese', 'Yogurt', 'Butter', 'Eggs',
            'Pizza', 'Burger', 'Sandwich', 'Salad', 'Soup'
        ]

        partial_lower = partial_name.lower()
        suggestions = [
            food for food in common_foods
            if partial_lower in food.lower()
        ]

        return suggestions[:10]  # Return top 10 matches