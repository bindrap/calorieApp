#!/usr/bin/env python3
"""
Multi-Item Meal Recognition System
Detect and analyze multiple foods on a single plate using advanced vision AI
"""

import os
import json
import base64
import requests
from typing import Dict, List, Optional
from pathlib import Path


class MultiItemFoodRecognizer:
    """
    Enhanced food recognition that can detect multiple items in a single image
    Uses advanced vision models to segment and identify each food item separately
    """

    def __init__(self):
        self.api_url = os.environ.get('OLLAMA_API_URL', 'https://api.ollamacloud.ai/v1/chat/completions')
        self.api_key = os.environ.get('OLLAMA_API_KEY', '')
        self.model = os.environ.get('OLLAMA_MODEL', 'gpt-oss:120b')

    def analyze_multi_item_meal(
        self,
        image_path: str,
        user_description: Optional[str] = None,
        reference_objects: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze an image and detect multiple food items

        Args:
            image_path: Path to the meal image
            user_description: Optional user-provided description
            reference_objects: Optional calibrated reference objects (hand, plate, etc.)

        Returns:
            Dict containing:
                - items: List of detected food items
                - total_calories: Sum of all items
                - total_macros: Aggregated protein/carbs/fat
                - confidence: Overall confidence score
        """
        print(f"🔍 Analyzing multi-item meal: {image_path}")

        # Encode image
        image_base64 = self._encode_image(image_path)

        # Build enhanced prompt for multi-item detection
        prompt = self._build_multi_item_prompt(user_description, reference_objects)

        # Call vision AI
        response = self._call_vision_api(prompt, image_base64)

        # Parse response
        result = self._parse_multi_item_response(response)

        return result

    def _build_multi_item_prompt(
        self,
        user_description: Optional[str] = None,
        reference_objects: Optional[Dict] = None
    ) -> str:
        """Build enhanced prompt for detecting multiple items"""

        prompt = """🔍 MULTI-ITEM MEAL ANALYSIS

Your task is to identify EVERY individual food item visible in this image and provide detailed nutrition information for each.

CRITICAL INSTRUCTIONS:
1. **Identify ALL items** - List every distinct food item on the plate/table
2. **Separate analysis** - Provide individual nutrition data for EACH item
3. **Portion estimation** - Estimate weight/volume for each item separately
4. **Aggregation** - Sum up totals at the end

"""

        # Add user description if provided
        if user_description and user_description.strip():
            prompt += f"""
🎯 USER DESCRIPTION (HIGHEST PRIORITY):
"{user_description}"

Trust the user's description above all. They may mention specific items, brands, or portion sizes.

"""

        # Add reference object context if available
        if reference_objects:
            prompt += """
📏 REFERENCE OBJECTS FOR SCALE:
"""
            if 'hand_palm' in reference_objects:
                hand_data = reference_objects['hand_palm']
                prompt += f"- User's palm: {hand_data.get('length_cm')}cm × {hand_data.get('width_cm')}cm\n"
            if 'plate' in reference_objects:
                plate_data = reference_objects['plate']
                prompt += f"- Plate diameter: {plate_data.get('width_cm')}cm\n"
            if 'fist' in reference_objects:
                fist_data = reference_objects['fist']
                prompt += f"- User's fist: ~{fist_data.get('volume_ml')}ml volume\n"

            prompt += "\nUse these references to estimate portion sizes more accurately.\n\n"

        prompt += """
OUTPUT FORMAT (respond with valid JSON):
```json
{
    "items": [
        {
            "item_number": 1,
            "food_name": "Grilled Chicken Breast",
            "category": "protein",
            "estimated_weight_grams": 200,
            "estimation_method": "visual comparison with hand",
            "confidence": 0.85,
            "calories": 330,
            "protein": 62,
            "carbs": 0,
            "fat": 7,
            "notes": "Appears to be grilled, no visible oil"
        },
        {
            "item_number": 2,
            "food_name": "White Rice",
            "category": "carbs",
            "estimated_weight_grams": 150,
            "estimation_method": "visual volume estimation",
            "confidence": 0.78,
            "calories": 195,
            "protein": 4,
            "carbs": 43,
            "fat": 0.3,
            "notes": "Cooked white rice, about 3/4 cup"
        }
    ],
    "totals": {
        "total_calories": 525,
        "total_protein": 66,
        "total_carbs": 43,
        "total_fat": 7.3,
        "total_items": 2
    },
    "overall_confidence": 0.82,
    "meal_type": "lunch",
    "cooking_methods": ["grilled", "steamed"],
    "additional_notes": "Balanced meal with good protein content"
}
```

IMPORTANT GUIDELINES:
✅ DO:
- Identify EVERY distinct food item (even garnishes if significant)
- Estimate portion sizes carefully using visual cues
- Consider cooking methods (affects calories)
- Note any visible oils, butter, sauces
- Use standard serving sizes as benchmarks
- Provide realistic confidence scores (0.0-1.0)

❌ DON'T:
- Lump multiple items together
- Skip small but calorie-dense items (dressings, oils)
- Guess wildly - mark low confidence if unsure
- Forget to sum up totals

Begin your analysis now:
"""

        return prompt

    def _call_vision_api(self, prompt: str, image_base64: str) -> str:
        """Call the vision AI API"""

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/jpeg;base64,{image_base64}'
                            }
                        }
                    ]
                }
            ],
            'max_tokens': 3000,
            'temperature': 0.3  # Lower temperature for more consistent output
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            return content

        except Exception as e:
            print(f"❌ Vision API error: {e}")
            return self._get_fallback_response()

    def _parse_multi_item_response(self, response: str) -> Dict:
        """Parse the AI's JSON response into structured data"""

        try:
            # Extract JSON from markdown code blocks if present
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                json_str = response[json_start:json_end].strip()
            elif '```' in response:
                json_start = response.find('```') + 3
                json_end = response.find('```', json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response

            # Parse JSON
            data = json.loads(json_str)

            # Validate and structure result
            result = {
                'items': data.get('items', []),
                'totals': data.get('totals', {}),
                'overall_confidence': data.get('overall_confidence', 0.5),
                'meal_type': data.get('meal_type', 'unknown'),
                'cooking_methods': data.get('cooking_methods', []),
                'additional_notes': data.get('additional_notes', ''),
                'multi_item': len(data.get('items', [])) > 1,
                'raw_response': response
            }

            print(f"✅ Detected {len(result['items'])} items")
            for item in result['items']:
                print(f"   {item.get('item_number')}. {item.get('food_name')} - {item.get('calories')} cal")

            return result

        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print(f"Raw response: {response[:500]}")
            return self._get_fallback_result()
        except Exception as e:
            print(f"❌ Error parsing response: {e}")
            return self._get_fallback_result()

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def _get_fallback_response(self) -> str:
        """Fallback response if API fails"""
        return json.dumps({
            'items': [{
                'item_number': 1,
                'food_name': 'Unknown Food',
                'category': 'unknown',
                'estimated_weight_grams': 200,
                'estimation_method': 'fallback',
                'confidence': 0.1,
                'calories': 300,
                'protein': 10,
                'carbs': 30,
                'fat': 10,
                'notes': 'API error - using fallback values'
            }],
            'totals': {
                'total_calories': 300,
                'total_protein': 10,
                'total_carbs': 30,
                'total_fat': 10,
                'total_items': 1
            },
            'overall_confidence': 0.1,
            'meal_type': 'unknown',
            'cooking_methods': [],
            'additional_notes': 'Fallback response due to API error'
        })

    def _get_fallback_result(self) -> Dict:
        """Fallback result structure"""
        return {
            'items': [],
            'totals': {
                'total_calories': 0,
                'total_protein': 0,
                'total_carbs': 0,
                'total_fat': 0,
                'total_items': 0
            },
            'overall_confidence': 0.0,
            'meal_type': 'unknown',
            'cooking_methods': [],
            'additional_notes': 'Failed to analyze image',
            'multi_item': False,
            'error': True
        }


class SmartPortionEstimator:
    """
    Estimate portion sizes using reference objects (hand, plate, etc.)
    Helps users calibrate AI estimates with real-world measurements
    """

    def __init__(self):
        pass

    def calibrate_hand_reference(self, user_height_cm: float, gender: str = 'male') -> Dict:
        """
        Estimate hand measurements based on user height and gender
        Used when user hasn't uploaded calibration photos

        Args:
            user_height_cm: User's height in centimeters
            gender: 'male' or 'female'

        Returns:
            Dict with estimated hand measurements
        """
        # Scientific correlations between height and hand size
        # Based on anthropometric studies

        if gender == 'male':
            palm_length = 10.2 + (user_height_cm - 170) * 0.035  # cm
            palm_width = 8.4 + (user_height_cm - 170) * 0.025
            fist_volume = 250 + (user_height_cm - 170) * 2.5  # ml
        else:  # female
            palm_length = 9.1 + (user_height_cm - 160) * 0.032
            palm_width = 7.6 + (user_height_cm - 160) * 0.023
            fist_volume = 220 + (user_height_cm - 160) * 2.2

        return {
            'hand_palm': {
                'length_cm': round(palm_length, 1),
                'width_cm': round(palm_width, 1),
                'area_cm2': round(palm_length * palm_width, 1)
            },
            'fist': {
                'volume_ml': round(fist_volume, 0)
            },
            'thumb': {
                'length_cm': round(palm_length * 0.6, 1),
                'tip_diameter_cm': round(palm_width * 0.18, 1)
            },
            'source': 'estimated_from_height'
        }

    def estimate_food_weight_from_hand(
        self,
        food_type: str,
        hand_comparison: str,
        hand_measurements: Dict
    ) -> Dict:
        """
        Estimate food weight based on hand comparison

        Args:
            food_type: Type of food (meat, rice, vegetables, etc.)
            hand_comparison: e.g., "palm-sized", "fist-sized", "thumb-length"
            hand_measurements: User's calibrated hand measurements

        Returns:
            Dict with weight estimation
        """

        # Food density estimates (g/cm³)
        food_densities = {
            'meat': 1.05,  # Chicken, beef, fish
            'rice': 0.75,  # Cooked rice
            'pasta': 0.65,  # Cooked pasta
            'vegetables': 0.35,  # Leafy/watery vegetables
            'bread': 0.28,
            'cheese': 1.10,
            'nuts': 0.65,
            'fruit': 0.60
        }

        density = food_densities.get(food_type, 0.75)  # Default to rice density

        # Calculate volume based on hand comparison
        if 'palm' in hand_comparison.lower():
            # Palm-sized, about 2cm thick
            palm_area = hand_measurements.get('hand_palm', {}).get('area_cm2', 75)
            volume = palm_area * 2  # 2cm thick
            weight_g = volume * density

        elif 'fist' in hand_comparison.lower():
            # Fist-sized
            fist_volume = hand_measurements.get('fist', {}).get('volume_ml', 250)
            weight_g = fist_volume * density

        elif 'thumb' in hand_comparison.lower():
            # Thumb-sized (for small portions like butter, cheese)
            thumb_length = hand_measurements.get('thumb', {}).get('length_cm', 6)
            thumb_diameter = hand_measurements.get('thumb', {}).get('tip_diameter_cm', 1.5)
            volume = 3.14159 * (thumb_diameter/2)**2 * thumb_length
            weight_g = volume * density

        else:
            # Fallback
            weight_g = 150

        return {
            'estimated_weight_grams': round(weight_g, 0),
            'method': f'hand_comparison_{hand_comparison}',
            'confidence': 0.75,  # Hand comparisons are reasonably accurate
            'density_used': density,
            'notes': f'Estimated using {hand_comparison} with {food_type} density'
        }

    def get_common_reference_volumes(self) -> Dict:
        """
        Return common household reference volumes for user guidance

        Returns:
            Dict of reference objects and their volumes
        """
        return {
            'cup': 240,  # ml
            'bowl_small': 400,
            'bowl_medium': 600,
            'bowl_large': 800,
            'plate_small': {'diameter_cm': 20},
            'plate_medium': {'diameter_cm': 25},
            'plate_large': {'diameter_cm': 30},
            'tablespoon': 15,  # ml
            'teaspoon': 5,
            'shot_glass': 45,
            'can_soda': 355,
            'water_bottle': 500
        }


# Test function
if __name__ == '__main__':
    print("Multi-Item Food Recognition System")
    print("=" * 60)

    recognizer = MultiItemFoodRecognizer()
    print("✅ Multi-item recognizer initialized")

    estimator = SmartPortionEstimator()
    print("✅ Smart portion estimator initialized")

    # Test hand calibration
    hand_ref = estimator.calibrate_hand_reference(175, 'male')
    print(f"\n📏 Estimated hand reference for 175cm male:")
    print(f"   Palm: {hand_ref['hand_palm']['length_cm']}cm × {hand_ref['hand_palm']['width_cm']}cm")
    print(f"   Fist volume: {hand_ref['fist']['volume_ml']}ml")

    print("\n✅ All systems operational!")
