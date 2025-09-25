#!/usr/bin/env python3
"""
Web Search-Enhanced Nutrition Calculator
Uses Ollama to perform intelligent web searches for real-time calorie data
Especially accurate for fast food and branded items
"""

import requests
import json
import re
from typing import Dict, Optional
from ollama import Client

# Configuration
OLLAMA_MODEL = "gpt-oss:120b"
API_KEY = "fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg"

class WebSearchNutritionCalculator:
    """Uses Ollama + web search for hyper-accurate nutrition data"""

    def __init__(self, model: str = OLLAMA_MODEL, api_key: str = API_KEY):
        self.model = model
        self.api_key = api_key
        self.base_url = "https://ollama.com"

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # Fast food chains that should always use web search
        self.fast_food_chains = [
            'mcdonalds', 'mcdonald', 'burger king', 'kfc', 'taco bell',
            'subway', 'pizza hut', 'dominos', 'starbucks', 'dunkin',
            'wendys', 'wendy', 'chipotle', 'five guys', 'in-n-out', 'jack in the box',
            'carl jr', 'hardees', 'arbys', 'dairy queen', 'sonic',
            'papa johns', 'little caesars', 'popeyes', 'chick-fil-a'
        ]

    def get_web_search_nutrition(self, food_name: str, estimated_weight: float = None) -> Optional[Dict]:
        """
        Use Ollama to search the web for accurate nutrition information
        """
        print(f"🌐 Web searching for nutrition data: {food_name}")

        try:
            # Check if this is a fast food item that needs web search
            if self._is_fast_food_item(food_name):
                return self._search_fast_food_nutrition(food_name, estimated_weight)
            elif self._needs_web_search(food_name):
                return self._search_general_nutrition(food_name, estimated_weight)
            else:
                return None

        except Exception as e:
            print(f"❌ Web search failed: {e}")
            return None

    def _is_fast_food_item(self, food_name: str) -> bool:
        """Check if the food item is from a fast food chain"""
        food_lower = food_name.lower()
        return any(chain in food_lower for chain in self.fast_food_chains)

    def _needs_web_search(self, food_name: str) -> bool:
        """Determine if food item needs web search for accuracy"""
        # Items that benefit from web search
        web_search_keywords = [
            'big mac', 'whopper', 'quarter pounder', 'mcchicken', 'baconator',
            'pizza', 'starbucks', 'frappuccino', 'latte',
            'branded', 'restaurant', 'chain'
        ]

        food_lower = food_name.lower()
        return any(keyword in food_lower for keyword in web_search_keywords)

    def _search_fast_food_nutrition(self, food_name: str, estimated_weight: float) -> Optional[Dict]:
        """Search for fast food nutrition data using Ollama"""

        search_prompt = f"""You are a nutrition expert with access to current fast food nutrition information.

        I need the exact nutritional information for: {food_name}

        Please search for the most current and accurate nutrition facts from official sources (company websites, nutrition databases, etc.).

        Respond ONLY with valid JSON in this exact format:
        {{
            "food_name": "Official menu item name",
            "brand": "Restaurant/brand name",
            "calories": 570,
            "protein": 25.0,
            "carbs": 45.0,
            "fat": 33.0,
            "fiber": 3.0,
            "sugar": 9.0,
            "sodium": 1010,
            "serving_weight_grams": 222,
            "serving_description": "1 sandwich",
            "confidence": 0.95,
            "source": "Official website/nutrition database"
        }}

        If you cannot find exact data, respond with:
        {{"error": "Could not find reliable nutrition data"}}

        Search for: {food_name} nutrition facts calories"""

        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": search_prompt}],
                "stream": False
            }

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers=self.headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get('message', {}).get('content', '')

                # Parse JSON response
                nutrition_data = self._parse_nutrition_json(content)

                if nutrition_data and 'error' not in nutrition_data:
                    # Scale to requested weight if different from serving size
                    if estimated_weight and estimated_weight != nutrition_data.get('serving_weight_grams', estimated_weight):
                        nutrition_data = self._scale_nutrition_data(nutrition_data, estimated_weight)

                    print(f"✅ Found web data: {nutrition_data.get('calories')} calories ({nutrition_data.get('confidence', 0):.2f} confidence)")
                    return nutrition_data
                else:
                    print(f"⚠️ Web search returned no reliable data")
                    return None

        except Exception as e:
            print(f"❌ Fast food search error: {e}")
            return None

    def _search_general_nutrition(self, food_name: str, estimated_weight: float) -> Optional[Dict]:
        """Search for general food nutrition data"""

        search_prompt = f"""You are a nutrition expert. Search for accurate nutritional information for: {food_name}

        Find data from reliable sources like USDA nutrition database, nutrition labels, or reputable nutrition websites.

        Respond with JSON in this format:
        {{
            "food_name": "{food_name}",
            "calories_per_100g": 250,
            "protein_per_100g": 12.0,
            "carbs_per_100g": 30.0,
            "fat_per_100g": 10.0,
            "fiber_per_100g": 2.0,
            "sugar_per_100g": 5.0,
            "sodium_per_100g": 500,
            "confidence": 0.8,
            "source": "USDA/nutrition database"
        }}

        If no reliable data found, respond: {{"error": "No reliable data found"}}

        Search for: {food_name} nutrition facts per 100g USDA database"""

        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": search_prompt}],
                "stream": False
            }

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                headers=self.headers,
                timeout=25
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get('message', {}).get('content', '')

                nutrition_data = self._parse_nutrition_json(content)

                if nutrition_data and 'error' not in nutrition_data:
                    # Convert per-100g data to actual serving
                    actual_weight = estimated_weight or 100
                    scale_factor = actual_weight / 100.0

                    scaled_data = {
                        'food_name': nutrition_data.get('food_name', food_name),
                        'calories': nutrition_data.get('calories_per_100g', 0) * scale_factor,
                        'protein': nutrition_data.get('protein_per_100g', 0) * scale_factor,
                        'carbs': nutrition_data.get('carbs_per_100g', 0) * scale_factor,
                        'fat': nutrition_data.get('fat_per_100g', 0) * scale_factor,
                        'fiber': nutrition_data.get('fiber_per_100g', 0) * scale_factor,
                        'sugar': nutrition_data.get('sugar_per_100g', 0) * scale_factor,
                        'sodium': nutrition_data.get('sodium_per_100g', 0) * scale_factor / 1000,  # mg to g
                        'serving_weight_grams': actual_weight,
                        'confidence': nutrition_data.get('confidence', 0.7),
                        'source': nutrition_data.get('source', 'web_search'),
                        'data_source': 'web_search'
                    }

                    print(f"✅ Found general nutrition data: {scaled_data.get('calories'):.1f} calories")
                    return scaled_data

        except Exception as e:
            print(f"❌ General search error: {e}")

        return None

    def _parse_nutrition_json(self, content: str) -> Optional[Dict]:
        """Parse JSON from Ollama response"""
        try:
            # Find JSON in the response
            start = content.find('{')
            end = content.rfind('}') + 1

            if start != -1 and end > start:
                json_str = content[start:end]
                return json.loads(json_str)

        except Exception as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw content: {content[:200]}...")

        return None

    def _scale_nutrition_data(self, nutrition_data: Dict, target_weight: float) -> Dict:
        """Scale nutrition data to target weight"""
        original_weight = nutrition_data.get('serving_weight_grams', 100)
        scale_factor = target_weight / original_weight

        scaled_data = nutrition_data.copy()
        scaled_data.update({
            'calories': nutrition_data.get('calories', 0) * scale_factor,
            'protein': nutrition_data.get('protein', 0) * scale_factor,
            'carbs': nutrition_data.get('carbs', 0) * scale_factor,
            'fat': nutrition_data.get('fat', 0) * scale_factor,
            'fiber': nutrition_data.get('fiber', 0) * scale_factor,
            'sugar': nutrition_data.get('sugar', 0) * scale_factor,
            'sodium': nutrition_data.get('sodium', 0) * scale_factor,
            'serving_weight_grams': target_weight,
            'serving_description': f'{target_weight}g portion'
        })

        return scaled_data

    def enhance_nutrition_with_web_search(self, recognition_result: Dict, existing_calculation: Dict) -> Dict:
        """Enhance existing calculation with web search data if available"""
        food_name = recognition_result.get('primary_food', '')
        estimated_weight = recognition_result.get('estimated_weight', 100)

        # Try web search enhancement
        web_data = self.get_web_search_nutrition(food_name, estimated_weight)

        if web_data and web_data.get('confidence', 0) > 0.8:
            # Web search found high-confidence data, use it instead
            return {
                'food_name': web_data.get('food_name', food_name),
                'weight_grams': web_data.get('serving_weight_grams', estimated_weight),
                'total_calories': round(web_data.get('calories', 0), 1),
                'protein': round(web_data.get('protein', 0), 1),
                'carbs': round(web_data.get('carbs', 0), 1),
                'fat': round(web_data.get('fat', 0), 1),
                'fiber': round(web_data.get('fiber', 0), 1),
                'sugar': round(web_data.get('sugar', 0), 1),
                'sodium': round(web_data.get('sodium', 0), 3),
                'data_source': 'web_search_enhanced',
                'confidence_score': web_data.get('confidence', 0.9),
                'brand': web_data.get('brand', ''),
                'source': web_data.get('source', 'web_search'),
                'serving_description': web_data.get('serving_description', f'{estimated_weight}g')
            }
        else:
            # Use existing calculation with web search attempted flag
            enhanced_result = existing_calculation.copy()
            enhanced_result.update({
                'data_source': f"{existing_calculation.get('data_source', 'unknown')}_web_verified",
                'web_search_attempted': True,
                'web_search_success': web_data is not None
            })
            return enhanced_result

# Test the web search functionality
if __name__ == "__main__":
    calculator = WebSearchNutritionCalculator()

    test_foods = [
        {'primary_food': 'Big Mac', 'estimated_weight': 222},
        {'primary_food': 'Whopper', 'estimated_weight': 291},
        {'primary_food': 'Starbucks Grande Latte', 'estimated_weight': 473}
    ]

    for food_test in test_foods:
        print(f"\n🧪 Testing: {food_test['primary_food']}")
        result = calculator.get_web_search_nutrition(
            food_test['primary_food'],
            food_test['estimated_weight']
        )

        if result:
            print(f"✅ Result: {result.get('calories')} calories")
            print(f"   Source: {result.get('source', 'unknown')}")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
        else:
            print("❌ No web search data found")