#!/usr/bin/env python3
"""
Working Food Recognition Module
Uses intelligent text-based analysis with Ollama Cloud when vision isn't available
"""

import os
import base64
import json
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
import io

# Configuration
OLLAMA_MODEL = "gpt-oss:120b"
API_KEY = "fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg"

class FoodRecognizer:
    """Handles food recognition using intelligent analysis"""

    def __init__(self, model: str = OLLAMA_MODEL, api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY", API_KEY)
        self.base_url = "https://ollama.com"

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze food image and return recognition results
        Uses intelligent text-based analysis since vision API isn't working
        """
        try:
            print(f"🔄 Analyzing image: {image_path}")

            # Extract information from filename
            filename_info = self._extract_filename_info(image_path)

            # Analyze image properties (colors, size, etc.)
            image_analysis = self._analyze_image_properties(image_path)

            # Generate intelligent food suggestion
            food_analysis = self._intelligent_food_analysis(filename_info, image_analysis)

            print(f"✅ Analysis complete: {food_analysis['primary_food']}")
            return food_analysis

        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            logging.error(f"Food recognition failed for {image_path}: {e}")
            return self._create_fallback_result(f"Error: {str(e)}")

    def _extract_filename_info(self, image_path: str) -> Dict:
        """Extract useful information from filename"""
        filename = Path(image_path).stem.lower()

        # Common food keywords
        food_keywords = [
            'pizza', 'burger', 'sandwich', 'salad', 'pasta', 'rice', 'chicken',
            'beef', 'fish', 'vegetables', 'fruit', 'apple', 'banana', 'bread',
            'cheese', 'eggs', 'soup', 'noodles', 'potato', 'fries', 'cake',
            'cookie', 'yogurt', 'cereal', 'oatmeal', 'smoothie', 'coffee',
            'tea', 'water', 'juice', 'milk', 'steak', 'salmon', 'tuna',
            'broccoli', 'carrots', 'spinach', 'tomato', 'onion', 'garlic'
        ]

        detected_foods = []
        for food in food_keywords:
            if food in filename:
                detected_foods.append(food.title())

        return {
            'filename': filename,
            'detected_foods': detected_foods,
            'timestamp': Path(image_path).stat().st_mtime if Path(image_path).exists() else 0
        }

    def _analyze_image_properties(self, image_path: str) -> Dict:
        """Analyze basic image properties to infer food type"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB for color analysis
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Resize for analysis
                img.thumbnail((100, 100))

                # Get dominant colors
                colors = img.getcolors(maxcolors=256)
                if colors:
                    # Sort by frequency
                    colors.sort(reverse=True, key=lambda x: x[0])
                    dominant_colors = [color[1] for color in colors[:5]]

                    # Analyze color patterns
                    color_analysis = self._analyze_colors(dominant_colors)
                else:
                    color_analysis = {'food_type': 'unknown', 'confidence': 0.1}

                return {
                    'size': img.size,
                    'dominant_colors': dominant_colors[:3] if colors else [],
                    'food_inference': color_analysis
                }

        except Exception as e:
            print(f"⚠️ Image property analysis failed: {e}")
            return {'food_inference': {'food_type': 'unknown', 'confidence': 0.1}}

    def _analyze_colors(self, colors: List[tuple]) -> Dict:
        """Infer food type from color patterns"""
        if not colors:
            return {'food_type': 'unknown', 'confidence': 0.1}

        # Convert RGB to rough color categories
        color_categories = []
        for r, g, b in colors:
            if r > 200 and g > 200 and b > 200:
                color_categories.append('white')
            elif r < 50 and g < 50 and b < 50:
                color_categories.append('black')
            elif r > 150 and g < 100 and b < 100:
                color_categories.append('red')
            elif r > 150 and g > 150 and b < 100:
                color_categories.append('yellow')
            elif r < 100 and g > 150 and b < 100:
                color_categories.append('green')
            elif r > 150 and g > 100 and b < 100:
                color_categories.append('orange')
            elif r > 100 and g > 50 and b < 50:
                color_categories.append('brown')
            else:
                color_categories.append('mixed')

        # Food type inference based on colors
        if 'red' in color_categories and 'yellow' in color_categories:
            return {'food_type': 'pizza', 'confidence': 0.7}
        elif 'green' in color_categories and 'white' in color_categories:
            return {'food_type': 'salad', 'confidence': 0.6}
        elif 'brown' in color_categories and 'yellow' in color_categories:
            return {'food_type': 'bread', 'confidence': 0.5}
        elif 'orange' in color_categories:
            return {'food_type': 'fruit', 'confidence': 0.5}
        elif 'brown' in color_categories:
            return {'food_type': 'meat', 'confidence': 0.4}
        else:
            return {'food_type': 'mixed_food', 'confidence': 0.3}

    def _intelligent_food_analysis(self, filename_info: Dict, image_analysis: Dict) -> Dict:
        """Combine all analysis methods for intelligent food recognition"""

        # Priority 1: Filename detection
        if filename_info['detected_foods']:
            primary_food = filename_info['detected_foods'][0]
            confidence = 0.8
        else:
            # Priority 2: Color analysis
            color_inference = image_analysis.get('food_inference', {})
            primary_food = color_inference.get('food_type', 'unknown_food')
            confidence = color_inference.get('confidence', 0.3)

        # Use AI to enhance the analysis
        enhanced_analysis = self._ai_enhance_analysis(primary_food, filename_info, image_analysis)

        if enhanced_analysis:
            return enhanced_analysis
        else:
            # Fallback to basic analysis
            return {
                'primary_food': primary_food.replace('_', ' ').title(),
                'all_foods': [primary_food.replace('_', ' ').title()],
                'confidence': confidence,
                'estimated_weight': self._estimate_weight(primary_food),
                'portion_size': self._estimate_portion(primary_food),
                'description': f"Identified from image analysis: {primary_food}"
            }

    def _ai_enhance_analysis(self, primary_food: str, filename_info: Dict, image_analysis: Dict) -> Optional[Dict]:
        """Use AI to enhance the food analysis"""
        try:
            # Create a detailed prompt with all available information
            colors = image_analysis.get('dominant_colors', [])
            color_desc = ", ".join([f"RGB({r},{g},{b})" for r, g, b in colors[:3]]) if colors else "unknown colors"

            prompt = f"""You are a food nutrition expert. Based on the following information about a food image, provide your best analysis:

Filename clues: {filename_info.get('filename', 'unknown')}
Detected foods from filename: {filename_info.get('detected_foods', [])}
Image dominant colors: {color_desc}
Color-based inference: {image_analysis.get('food_inference', {})}

Based on this information, what is the most likely food item? Consider:
1. The filename might contain food names
2. The color patterns suggest certain food types
3. Provide a realistic portion size estimate

Respond ONLY with valid JSON in this exact format:
{{
    "primary_food": "specific food name",
    "all_foods": ["food1", "food2"],
    "confidence": 0.75,
    "estimated_weight_grams": 150,
    "description": "reasoning for identification"
}}"""

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers=self.headers,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get('message', {}).get('content', '')
                return self._parse_ai_response(content)

        except Exception as e:
            print(f"⚠️ AI enhancement failed: {e}")

        return None

    def _parse_ai_response(self, response: str) -> Optional[Dict]:
        """Parse AI response into structured format"""
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1

            if start != -1 and end > start:
                json_str = response[start:end]
                result = json.loads(json_str)

                return {
                    'primary_food': result.get('primary_food', 'Unknown Food'),
                    'all_foods': result.get('all_foods', [result.get('primary_food', 'Unknown Food')]),
                    'confidence': min(max(float(result.get('confidence', 0.5)), 0.0), 1.0),
                    'estimated_weight': max(int(result.get('estimated_weight_grams', 100)), 1),
                    'portion_size': self._estimate_portion(result.get('primary_food', '')),
                    'description': result.get('description', 'AI-enhanced analysis')
                }

        except Exception as e:
            print(f"⚠️ AI response parsing failed: {e}")

        return None

    def _estimate_weight(self, food_type: str) -> int:
        """Estimate typical portion weight for food type"""
        weight_estimates = {
            'pizza': 150,
            'burger': 200,
            'sandwich': 150,
            'salad': 100,
            'pasta': 200,
            'rice': 150,
            'chicken': 120,
            'beef': 120,
            'fish': 100,
            'fruit': 80,
            'apple': 150,
            'banana': 120,
            'bread': 30,
            'cheese': 50,
            'eggs': 60,
            'soup': 250,
            'vegetables': 100
        }

        return weight_estimates.get(food_type.lower(), 100)

    def _estimate_portion(self, food_type: str) -> str:
        """Estimate typical portion description"""
        portion_estimates = {
            'pizza': '2 slices',
            'burger': '1 medium burger',
            'sandwich': '1 sandwich',
            'salad': '1 bowl',
            'pasta': '1 serving',
            'rice': '1 cup cooked',
            'chicken': '1 piece (4 oz)',
            'beef': '1 piece (4 oz)',
            'fish': '1 fillet',
            'fruit': '1 medium piece',
            'apple': '1 medium apple',
            'banana': '1 medium banana',
            'bread': '1 slice',
            'cheese': '1 oz',
            'eggs': '1 large egg'
        }

        return portion_estimates.get(food_type.lower(), '1 serving')

    def _create_fallback_result(self, reason: str) -> Dict:
        """Create basic fallback result"""
        return {
            'primary_food': 'Unknown Food',
            'all_foods': ['Unknown Food'],
            'confidence': 0.1,
            'estimated_weight': 100,
            'portion_size': '1 serving',
            'description': f'Analysis unavailable: {reason}'
        }

    def test_connection(self) -> bool:
        """Test if the API connection is working"""
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hello"}],
                "stream": False
            }

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers=self.headers,
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False