#!/usr/bin/env python3
"""
Calorie Calculator Module
Calculates calories and nutritional information based on food recognition results
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Import our web search and enhanced database modules
try:
    from web_search_nutrition import WebSearchNutritionCalculator
    from enhanced_food_database import get_enhanced_nutrition_data, calculate_accurate_calories
except ImportError as e:
    logging.warning(f"Could not import enhanced modules: {e}")
    WebSearchNutritionCalculator = None
    get_enhanced_nutrition_data = None
    calculate_accurate_calories = None

@dataclass
class NutritionalInfo:
    """Nutritional information for a food item"""
    calories: float
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0
    fiber: float = 0.0
    sugar: float = 0.0
    sodium: float = 0.0

class CalorieCalculator:
    """Handles calorie and nutrition calculations"""

    def __init__(self):
        # USDA Food Data Central API (free tier)
        self.usda_api_key = "bSMXb6Dq3W5l1ebpOKvpaBUNHocBCZkfdkTTw0n1"
        self.usda_base_url = "https://api.nal.usda.gov/fdc/v1"

        # Initialize web search nutrition calculator for hyper-accurate fast food data
        self.web_search_calculator = WebSearchNutritionCalculator() if WebSearchNutritionCalculator else None

        # Local food database for fallback
        self.local_food_db = self._load_local_food_database()

    def calculate_calories(self, recognition_result: Dict) -> Dict:
        """
        Calculate calories and nutrition info based on food recognition with hyper-accuracy

        Args:
            recognition_result: Output from FoodRecognizer.analyze_image()

        Returns:
            Dict with calorie and nutrition information
        """
        try:
            food_name = recognition_result['primary_food']
            estimated_weight = recognition_result.get('estimated_weight', 100)
            all_foods = recognition_result.get('all_foods', [food_name])

            print(f"🧮 Calculating calories for: {food_name} ({estimated_weight}g)")

            # Step 1: Try enhanced database first (for branded/fast food items)
            if get_enhanced_nutrition_data and calculate_accurate_calories:
                enhanced_result = calculate_accurate_calories(food_name, estimated_weight)
                if enhanced_result:
                    print(f"✅ Found in enhanced database: {enhanced_result['total_calories']} calories")
                    enhanced_result['data_source'] = 'enhanced_database'

                    # If it's a fast food item, try web search for even more accuracy
                    if self.web_search_calculator and self._is_fast_food_item(food_name):
                        print(f"🌐 Fast food detected, attempting web search enhancement...")
                        try:
                            web_enhanced = self.web_search_calculator.enhance_nutrition_with_web_search(
                                recognition_result, enhanced_result
                            )
                            if web_enhanced.get('data_source') == 'web_search_enhanced':
                                print(f"🎯 Web search enhanced: {web_enhanced['total_calories']} calories")
                                return web_enhanced
                        except Exception as web_error:
                            print(f"⚠️ Web search failed: {web_error}, using enhanced database result")
                            pass

                    return enhanced_result

            # Step 2: Try web search for fast food items AND other branded/restaurant items
            if self.web_search_calculator and (self._is_fast_food_item(food_name) or self._is_branded_or_restaurant_item(food_name)):
                print(f"🌐 Branded/restaurant item, attempting web search...")
                web_data = self.web_search_calculator.get_web_search_nutrition(food_name, estimated_weight)
                if web_data and web_data.get('confidence', 0) > 0.7:
                    result = {
                        'food_name': web_data.get('food_name', food_name),
                        'weight_grams': web_data.get('serving_weight_grams', estimated_weight),
                        'total_calories': round(web_data.get('calories', 0), 1),
                        'protein': round(web_data.get('protein', 0), 1),
                        'carbs': round(web_data.get('carbs', 0), 1),
                        'fat': round(web_data.get('fat', 0), 1),
                        'fiber': round(web_data.get('fiber', 0), 1),
                        'sugar': round(web_data.get('sugar', 0), 1),
                        'sodium': round(web_data.get('sodium', 0), 3),
                        'data_source': 'web_search_direct',
                        'confidence_score': web_data.get('confidence', 0.9),
                        'brand': web_data.get('brand', ''),
                        'source': web_data.get('source', 'web_search')
                    }
                    print(f"🎯 Direct web search: {result['total_calories']} calories")
                    return result

            # Step 3: Try original calculation methods
            nutrition_info = self._get_nutrition_info(food_name, estimated_weight)

            # If multiple foods detected, try to estimate combined nutrition
            if len(all_foods) > 1:
                print(f"🍽️ Multiple foods detected, calculating combined nutrition...")
                nutrition_info = self._calculate_multi_food_nutrition(all_foods, estimated_weight)

            result = {
                'food_name': food_name,
                'weight_grams': estimated_weight,
                'total_calories': round(nutrition_info.calories, 1),
                'protein': round(nutrition_info.protein, 1),
                'carbs': round(nutrition_info.carbs, 1),
                'fat': round(nutrition_info.fat, 1),
                'fiber': round(nutrition_info.fiber, 1),
                'sugar': round(nutrition_info.sugar, 1),
                'sodium': round(nutrition_info.sodium, 1),
                'data_source': 'calculated'
            }

            print(f"📊 Standard calculation: {result['total_calories']} calories")
            return result

        except Exception as e:
            logging.error(f"Calorie calculation failed: {e}")
            print(f"❌ Calculation error: {e}")
            # Return fallback values
            return self._get_fallback_nutrition(recognition_result)

    def _is_fast_food_item(self, food_name: str) -> bool:
        """Check if the food item is from a fast food chain"""
        fast_food_chains = [
            'mcdonalds', 'mcdonald', 'burger king', 'kfc', 'taco bell',
            'subway', 'pizza hut', 'dominos', 'starbucks', 'dunkin',
            'wendys', 'wendy', 'chipotle', 'five guys', 'in-n-out', 'jack in the box',
            'carl jr', 'hardees', 'arbys', 'dairy queen', 'sonic',
            'papa johns', 'little caesars', 'popeyes', 'chick-fil-a'
        ]

        # Also check for specific branded items
        fast_food_items = [
            'big mac', 'whopper', 'quarter pounder', 'mcchicken', 'baconator',
            'son of baconator', 'frappuccino', 'latte', 'cappuccino'
        ]

        food_lower = food_name.lower()
        return (any(chain in food_lower for chain in fast_food_chains) or
                any(item in food_lower for item in fast_food_items))

    def _is_branded_or_restaurant_item(self, food_name: str) -> bool:
        """Check if the food item is branded or from a restaurant (worth web searching)"""
        branded_keywords = [
            # Restaurants/chains not in fast food list
            'olive garden', 'red lobster', 'applebees', 'chilis', 'outback',
            'ihop', 'dennys', 'panda express', 'pf changs', 'cheesecake factory',

            # Branded packaged foods
            'oreo', 'doritos', 'lays', 'pringles', 'pepsi', 'coca cola', 'coke',
            'snickers', 'kit kat', 'reeses', 'hershey', 'mars', 'twix',
            'cheerios', 'frosted flakes', 'lucky charms', 'fruit loops',

            # Specific branded items that need accurate data
            'ben jerry', 'haagen dazs', 'blue bell', 'breyers',
            'lean cuisine', 'hungry man', 'stouffers', 'marie callender',

            # Coffee/drinks
            'frappuccino', 'macchiato', 'cappuccino', 'americano',
            'energy drink', 'red bull', 'monster', 'rockstar',

            # Other indicators
            'brand', 'restaurant', 'chain', 'frozen meal', 'packaged'
        ]

        food_lower = food_name.lower()
        return any(keyword in food_lower for keyword in branded_keywords)

    def _get_nutrition_info(self, food_name: str, weight_grams: float) -> NutritionalInfo:
        """Get nutrition information from available sources"""

        # Try USDA API first (if API key available)
        if self.usda_api_key:
            try:
                return self._get_usda_nutrition(food_name, weight_grams)
            except Exception as e:
                logging.warning(f"USDA API failed: {e}")

        # Fallback to local database
        return self._get_local_nutrition(food_name, weight_grams)

    def _get_usda_nutrition(self, food_name: str, weight_grams: float) -> NutritionalInfo:
        """Get nutrition info from USDA Food Data Central API"""
        try:
            # Search for food with better query formatting
            search_url = f"{self.usda_base_url}/foods/search"
            search_params = {
                'query': food_name,
                'dataType': ['Foundation', 'SR Legacy'],  # Most comprehensive data
                'pageSize': 5,  # Get more results to find better matches
                'api_key': self.usda_api_key
            }

            response = requests.get(search_url, params=search_params, timeout=10)
            response.raise_for_status()
            search_data = response.json()

            if not search_data.get('foods'):
                raise Exception("No food found in USDA database")

            # Find the best match from multiple results
            best_food = None
            food_name_lower = food_name.lower()

            # Priority scoring for better matches
            scored_foods = []
            for food in search_data['foods']:
                description = food.get('description', '').lower()
                score = 0

                # High score for exact match or containing the food name
                if food_name_lower in description:
                    score += 50

                # Prefer raw/basic versions
                if 'raw' in description:
                    score += 30
                elif any(word in description for word in ['fresh', 'whole']):
                    score += 20

                # Penalize processed/prepared versions
                if any(word in description for word in ['cooked', 'prepared', 'with', 'frosted', 'sweetened', 'canned', 'frozen', 'sauce', 'souffle', 'leaves', 'flour']):
                    score -= 20

                # Bonus for exact food type matches
                if description.startswith(food_name_lower):
                    score += 40

                scored_foods.append((score, food))

            # Sort by score and take the best
            scored_foods.sort(key=lambda x: x[0], reverse=True)
            best_food = scored_foods[0][1] if scored_foods else search_data['foods'][0]

            # Get detailed nutrition info
            food_id = best_food['fdcId']
            print(f"🔍 USDA found: {best_food.get('description', 'Unknown')}")
            detail_url = f"{self.usda_base_url}/food/{food_id}"
            detail_params = {'api_key': self.usda_api_key}

            detail_response = requests.get(detail_url, params=detail_params, timeout=10)
            detail_response.raise_for_status()
            food_data = detail_response.json()

            # Extract nutrition data with safe access
            nutrients = {}
            for nutrient in food_data.get('foodNutrients', []):
                try:
                    name = nutrient.get('nutrient', {}).get('name', '')
                    unit = nutrient.get('nutrient', {}).get('unitName', '')
                    amount = nutrient.get('amount', 0)
                    if amount is not None:  # Handle None values
                        # Store name with unit for energy disambiguation
                        key = f"{name} ({unit})" if name == 'Energy' else name
                        nutrients[key] = float(amount)
                except (ValueError, TypeError):
                    continue

            # Scale to actual weight (USDA data is per 100g)
            scale_factor = weight_grams / 100.0

            # Get calories - prefer kcal over kJ
            calories = 0
            # Try to find kcal energy first
            if 'Energy (kcal)' in nutrients:
                calories = nutrients['Energy (kcal)']
            elif 'Energy (kJ)' in nutrients:
                # Convert kJ to kcal (1 kcal = 4.184 kJ)
                calories = nutrients['Energy (kJ)'] / 4.184
            else:
                # Fallback to generic Energy
                calories = nutrients.get('Energy', 0)

            return NutritionalInfo(
                calories=calories * scale_factor,
                protein=nutrients.get('Protein', 0) * scale_factor,
                carbs=nutrients.get('Carbohydrate, by difference', 0) * scale_factor,
                fat=nutrients.get('Total lipid (fat)', 0) * scale_factor,
                fiber=nutrients.get('Fiber, total dietary', 0) * scale_factor,
                sugar=nutrients.get('Sugars, total including NLEA', 0) * scale_factor,
                sodium=nutrients.get('Sodium, Na', 0) * scale_factor / 1000  # Convert mg to g
            )

        except Exception as e:
            logging.error(f"USDA API error: {e}")
            raise

    def _get_local_nutrition(self, food_name: str, weight_grams: float) -> NutritionalInfo:
        """Get nutrition info from local database with enhanced matching"""
        food_name_lower = food_name.lower()

        # Enhanced matching strategy
        best_match = None
        best_score = 0

        for food_key, nutrition_data in self.local_food_db.items():
            score = 0

            # Exact match gets highest score
            if food_name_lower == food_key:
                score = 100
            # Contains full name
            elif food_name_lower in food_key or food_key in food_name_lower:
                score = 80
            else:
                # Word-by-word matching
                food_words = set(food_name_lower.split())
                key_words = set(food_key.split())
                common_words = food_words & key_words
                if common_words:
                    # Score based on percentage of words that match
                    score = len(common_words) / max(len(food_words), len(key_words)) * 50

                    # Bonus for matching important food words
                    important_words = {'chicken', 'beef', 'pork', 'fish', 'salmon', 'pizza', 'burger', 'rice', 'pasta'}
                    if common_words & important_words:
                        score += 20

            if score > best_score:
                best_score = score
                best_match = nutrition_data

        # If no good match, try food category matching
        if not best_match or best_score < 10:
            best_match = self._match_food_category(food_name_lower)

        if not best_match:
            # Default fallback nutrition (average food item)
            best_match = {
                'calories_per_100g': 150,
                'protein_per_100g': 5,
                'carbs_per_100g': 20,
                'fat_per_100g': 5,
                'fiber_per_100g': 2,
                'sugar_per_100g': 8,
                'sodium_per_100g': 0.3
            }

        # Scale to actual weight
        scale_factor = weight_grams / 100.0

        return NutritionalInfo(
            calories=best_match['calories_per_100g'] * scale_factor,
            protein=best_match.get('protein_per_100g', 0) * scale_factor,
            carbs=best_match.get('carbs_per_100g', 0) * scale_factor,
            fat=best_match.get('fat_per_100g', 0) * scale_factor,
            fiber=best_match.get('fiber_per_100g', 0) * scale_factor,
            sugar=best_match.get('sugar_per_100g', 0) * scale_factor,
            sodium=best_match.get('sodium_per_100g', 0) * scale_factor
        )

    def _calculate_multi_food_nutrition(self, all_foods: List[str], total_weight: float) -> NutritionalInfo:
        """Calculate combined nutrition for multiple foods"""
        if len(all_foods) <= 1:
            return self._get_local_nutrition(all_foods[0] if all_foods else "unknown", total_weight)

        # Estimate weight distribution (simple equal division for now)
        weight_per_food = total_weight / len(all_foods)

        combined_nutrition = NutritionalInfo(0, 0, 0, 0, 0, 0, 0)

        for food_name in all_foods:
            food_nutrition = self._get_local_nutrition(food_name, weight_per_food)
            combined_nutrition.calories += food_nutrition.calories
            combined_nutrition.protein += food_nutrition.protein
            combined_nutrition.carbs += food_nutrition.carbs
            combined_nutrition.fat += food_nutrition.fat
            combined_nutrition.fiber += food_nutrition.fiber
            combined_nutrition.sugar += food_nutrition.sugar
            combined_nutrition.sodium += food_nutrition.sodium

        return combined_nutrition

    def _match_food_category(self, food_name_lower: str) -> dict:
        """Match food to category-based nutrition estimates"""
        # Food category patterns with better nutrition estimates
        category_nutrition = {
            # Meat/Protein patterns
            'chicken': {'calories_per_100g': 165, 'protein_per_100g': 31, 'carbs_per_100g': 0, 'fat_per_100g': 3.6, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.074},
            'beef': {'calories_per_100g': 250, 'protein_per_100g': 26, 'carbs_per_100g': 0, 'fat_per_100g': 15, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.059},
            'pork': {'calories_per_100g': 242, 'protein_per_100g': 27, 'carbs_per_100g': 0, 'fat_per_100g': 14, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.062},
            'fish': {'calories_per_100g': 206, 'protein_per_100g': 22, 'carbs_per_100g': 0, 'fat_per_100g': 12, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.059},
            'salmon': {'calories_per_100g': 208, 'protein_per_100g': 20, 'carbs_per_100g': 0, 'fat_per_100g': 13, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.054},

            # Carb-heavy foods
            'rice': {'calories_per_100g': 130, 'protein_per_100g': 2.7, 'carbs_per_100g': 28, 'fat_per_100g': 0.3, 'fiber_per_100g': 0.4, 'sugar_per_100g': 0.1, 'sodium_per_100g': 0.001},
            'pasta': {'calories_per_100g': 131, 'protein_per_100g': 5, 'carbs_per_100g': 25, 'fat_per_100g': 1.1, 'fiber_per_100g': 1.8, 'sugar_per_100g': 0.6, 'sodium_per_100g': 0.001},
            'bread': {'calories_per_100g': 265, 'protein_per_100g': 9, 'carbs_per_100g': 49, 'fat_per_100g': 3.2, 'fiber_per_100g': 2.7, 'sugar_per_100g': 5, 'sodium_per_100g': 0.491},
            'noodles': {'calories_per_100g': 138, 'protein_per_100g': 4.5, 'carbs_per_100g': 25, 'fat_per_100g': 2.2, 'fiber_per_100g': 1.8, 'sugar_per_100g': 0.6, 'sodium_per_100g': 0.001},

            # Mixed dishes (higher calorie estimates)
            'pizza': {'calories_per_100g': 280, 'protein_per_100g': 12, 'carbs_per_100g': 35, 'fat_per_100g': 12, 'fiber_per_100g': 2.5, 'sugar_per_100g': 4, 'sodium_per_100g': 0.640},
            'burger': {'calories_per_100g': 320, 'protein_per_100g': 18, 'carbs_per_100g': 28, 'fat_per_100g': 18, 'fiber_per_100g': 2, 'sugar_per_100g': 4, 'sodium_per_100g': 0.520},
            'sandwich': {'calories_per_100g': 250, 'protein_per_100g': 12, 'carbs_per_100g': 30, 'fat_per_100g': 10, 'fiber_per_100g': 3, 'sugar_per_100g': 4, 'sodium_per_100g': 0.380},
            'taco': {'calories_per_100g': 220, 'protein_per_100g': 11, 'carbs_per_100g': 20, 'fat_per_100g': 12, 'fiber_per_100g': 3, 'sugar_per_100g': 2, 'sodium_per_100g': 0.350},

            # Vegetables (default to broccoli-like)
            'vegetable': {'calories_per_100g': 35, 'protein_per_100g': 3, 'carbs_per_100g': 7, 'fat_per_100g': 0.4, 'fiber_per_100g': 3, 'sugar_per_100g': 2, 'sodium_per_100g': 0.040},
            'salad': {'calories_per_100g': 20, 'protein_per_100g': 1.5, 'carbs_per_100g': 4, 'fat_per_100g': 0.2, 'fiber_per_100g': 1.8, 'sugar_per_100g': 2, 'sodium_per_100g': 0.028},

            # Fruits
            'fruit': {'calories_per_100g': 60, 'protein_per_100g': 0.5, 'carbs_per_100g': 15, 'fat_per_100g': 0.2, 'fiber_per_100g': 2.5, 'sugar_per_100g': 12, 'sodium_per_100g': 0.001}
        }

        # Try to match food to category
        for category, nutrition in category_nutrition.items():
            if category in food_name_lower:
                return nutrition

        # Check for broader patterns
        if any(word in food_name_lower for word in ['meat', 'steak', 'roast']):
            return category_nutrition['beef']
        if any(word in food_name_lower for word in ['vegetable', 'veggie', 'green']):
            return category_nutrition['vegetable']
        if any(word in food_name_lower for word in ['fruit', 'berry', 'apple', 'orange']):
            return category_nutrition['fruit']

        return None

    def _get_fallback_nutrition(self, recognition_result: Dict) -> Dict:
        """Provide fallback nutrition values when calculation fails"""
        estimated_weight = recognition_result.get('estimated_weight', 100)

        return {
            'food_name': recognition_result.get('primary_food', 'Unknown food'),
            'weight_grams': estimated_weight,
            'total_calories': estimated_weight * 1.5,  # Rough estimate: 1.5 cal/gram
            'protein': estimated_weight * 0.05,
            'carbs': estimated_weight * 0.2,
            'fat': estimated_weight * 0.05,
            'fiber': estimated_weight * 0.02,
            'sugar': estimated_weight * 0.08,
            'sodium': estimated_weight * 0.003,
            'data_source': 'fallback_estimate'
        }

    def _load_local_food_database(self) -> Dict:
        """Load local food nutrition database"""
        # Comprehensive local food database (calories per 100g)
        return {
            'apple': {'calories_per_100g': 52, 'protein_per_100g': 0.3, 'carbs_per_100g': 14, 'fat_per_100g': 0.2, 'fiber_per_100g': 2.4, 'sugar_per_100g': 10, 'sodium_per_100g': 0.001},
            'banana': {'calories_per_100g': 89, 'protein_per_100g': 1.1, 'carbs_per_100g': 23, 'fat_per_100g': 0.3, 'fiber_per_100g': 2.6, 'sugar_per_100g': 12, 'sodium_per_100g': 0.001},
            'orange': {'calories_per_100g': 47, 'protein_per_100g': 0.9, 'carbs_per_100g': 12, 'fat_per_100g': 0.1, 'fiber_per_100g': 2.4, 'sugar_per_100g': 9, 'sodium_per_100g': 0.001},
            'rice': {'calories_per_100g': 130, 'protein_per_100g': 2.7, 'carbs_per_100g': 28, 'fat_per_100g': 0.3, 'fiber_per_100g': 0.4, 'sugar_per_100g': 0.1, 'sodium_per_100g': 0.001},
            'chicken': {'calories_per_100g': 165, 'protein_per_100g': 31, 'carbs_per_100g': 0, 'fat_per_100g': 3.6, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.074},
            'chicken breast': {'calories_per_100g': 165, 'protein_per_100g': 31, 'carbs_per_100g': 0, 'fat_per_100g': 3.6, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.074},
            'beef': {'calories_per_100g': 250, 'protein_per_100g': 26, 'carbs_per_100g': 0, 'fat_per_100g': 15, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.059},
            'pork': {'calories_per_100g': 242, 'protein_per_100g': 27, 'carbs_per_100g': 0, 'fat_per_100g': 14, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.062},
            'fish': {'calories_per_100g': 206, 'protein_per_100g': 22, 'carbs_per_100g': 0, 'fat_per_100g': 12, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.059},
            'salmon': {'calories_per_100g': 208, 'protein_per_100g': 20, 'carbs_per_100g': 0, 'fat_per_100g': 13, 'fiber_per_100g': 0, 'sugar_per_100g': 0, 'sodium_per_100g': 0.054},
            'bread': {'calories_per_100g': 265, 'protein_per_100g': 9, 'carbs_per_100g': 49, 'fat_per_100g': 3.2, 'fiber_per_100g': 2.7, 'sugar_per_100g': 5, 'sodium_per_100g': 0.491},
            'pasta': {'calories_per_100g': 131, 'protein_per_100g': 5, 'carbs_per_100g': 25, 'fat_per_100g': 1.1, 'fiber_per_100g': 1.8, 'sugar_per_100g': 0.6, 'sodium_per_100g': 0.001},
            'egg': {'calories_per_100g': 155, 'protein_per_100g': 13, 'carbs_per_100g': 1.1, 'fat_per_100g': 11, 'fiber_per_100g': 0, 'sugar_per_100g': 1.1, 'sodium_per_100g': 0.124},
            'milk': {'calories_per_100g': 61, 'protein_per_100g': 3.2, 'carbs_per_100g': 4.8, 'fat_per_100g': 3.3, 'fiber_per_100g': 0, 'sugar_per_100g': 4.8, 'sodium_per_100g': 0.044},
            'cheese': {'calories_per_100g': 402, 'protein_per_100g': 25, 'carbs_per_100g': 1.3, 'fat_per_100g': 33, 'fiber_per_100g': 0, 'sugar_per_100g': 0.5, 'sodium_per_100g': 0.621},
            'yogurt': {'calories_per_100g': 59, 'protein_per_100g': 10, 'carbs_per_100g': 3.6, 'fat_per_100g': 0.4, 'fiber_per_100g': 0, 'sugar_per_100g': 3.2, 'sodium_per_100g': 0.046},
            'broccoli': {'calories_per_100g': 34, 'protein_per_100g': 2.8, 'carbs_per_100g': 7, 'fat_per_100g': 0.4, 'fiber_per_100g': 2.6, 'sugar_per_100g': 1.5, 'sodium_per_100g': 0.033},
            'carrots': {'calories_per_100g': 41, 'protein_per_100g': 0.9, 'carbs_per_100g': 10, 'fat_per_100g': 0.2, 'fiber_per_100g': 2.8, 'sugar_per_100g': 4.7, 'sodium_per_100g': 0.069},
            'spinach': {'calories_per_100g': 23, 'protein_per_100g': 2.9, 'carbs_per_100g': 3.6, 'fat_per_100g': 0.4, 'fiber_per_100g': 2.2, 'sugar_per_100g': 0.4, 'sodium_per_100g': 0.079},
            'tomato': {'calories_per_100g': 18, 'protein_per_100g': 0.9, 'carbs_per_100g': 3.9, 'fat_per_100g': 0.2, 'fiber_per_100g': 1.2, 'sugar_per_100g': 2.6, 'sodium_per_100g': 0.005},
            'potato': {'calories_per_100g': 77, 'protein_per_100g': 2, 'carbs_per_100g': 17, 'fat_per_100g': 0.1, 'fiber_per_100g': 2.2, 'sugar_per_100g': 0.8, 'sodium_per_100g': 0.006},
            'pizza': {'calories_per_100g': 266, 'protein_per_100g': 11, 'carbs_per_100g': 33, 'fat_per_100g': 10, 'fiber_per_100g': 2.3, 'sugar_per_100g': 3.6, 'sodium_per_100g': 0.598},
            'burger': {'calories_per_100g': 295, 'protein_per_100g': 17, 'carbs_per_100g': 25, 'fat_per_100g': 15, 'fiber_per_100g': 2, 'sugar_per_100g': 4, 'sodium_per_100g': 0.497},
            'sandwich': {'calories_per_100g': 250, 'protein_per_100g': 12, 'carbs_per_100g': 30, 'fat_per_100g': 10, 'fiber_per_100g': 3, 'sugar_per_100g': 4, 'sodium_per_100g': 0.380},
            'salad': {'calories_per_100g': 20, 'protein_per_100g': 1.5, 'carbs_per_100g': 4, 'fat_per_100g': 0.2, 'fiber_per_100g': 1.8, 'sugar_per_100g': 2, 'sodium_per_100g': 0.028}
        }

    def get_calorie_breakdown(self, nutrition_info: Dict) -> Dict:
        """Calculate calorie breakdown by macronutrient"""
        protein_calories = nutrition_info.get('protein', 0) * 4  # 4 cal/g
        carb_calories = nutrition_info.get('carbs', 0) * 4      # 4 cal/g
        fat_calories = nutrition_info.get('fat', 0) * 9         # 9 cal/g

        total_macro_calories = protein_calories + carb_calories + fat_calories
        total_calories = nutrition_info.get('total_calories', total_macro_calories)

        return {
            'protein_calories': round(protein_calories, 1),
            'carb_calories': round(carb_calories, 1),
            'fat_calories': round(fat_calories, 1),
            'protein_percentage': round((protein_calories / total_calories * 100) if total_calories > 0 else 0, 1),
            'carb_percentage': round((carb_calories / total_calories * 100) if total_calories > 0 else 0, 1),
            'fat_percentage': round((fat_calories / total_calories * 100) if total_calories > 0 else 0, 1)
        }