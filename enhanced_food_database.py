#!/usr/bin/env python3
"""
Enhanced Food Database with Accurate Brand-Name Foods
Includes McDonald's, Burger King, and other popular fast food items
"""

# Enhanced food database with accurate nutritional data
ENHANCED_FOOD_DATABASE = {
    # McDonald's Items
    'big mac': {'calories_per_100g': 257, 'protein_per_100g': 13, 'carbs_per_100g': 20, 'fat_per_100g': 17, 'typical_weight': 222, 'typical_calories': 570},
    'bigmac': {'calories_per_100g': 257, 'protein_per_100g': 13, 'carbs_per_100g': 20, 'fat_per_100g': 17, 'typical_weight': 222, 'typical_calories': 570},
    'mcdonald big mac': {'calories_per_100g': 257, 'protein_per_100g': 13, 'carbs_per_100g': 20, 'fat_per_100g': 17, 'typical_weight': 222, 'typical_calories': 570},
    'quarter pounder': {'calories_per_100g': 265, 'protein_per_100g': 15, 'carbs_per_100g': 22, 'fat_per_100g': 16, 'typical_weight': 194, 'typical_calories': 515},
    'mcchicken': {'calories_per_100g': 208, 'protein_per_100g': 12, 'carbs_per_100g': 20, 'fat_per_100g': 11, 'typical_weight': 143, 'typical_calories': 400},
    'chicken mcnuggets': {'calories_per_100g': 300, 'protein_per_100g': 18, 'carbs_per_100g': 13, 'fat_per_100g': 20, 'typical_weight': 77, 'typical_calories': 230},  # 6 pieces

    # Burger King Items
    'whopper': {'calories_per_100g': 250, 'protein_per_100g': 13, 'carbs_per_100g': 22, 'fat_per_100g': 15, 'typical_weight': 291, 'typical_calories': 660},
    'burger king whopper': {'calories_per_100g': 250, 'protein_per_100g': 13, 'carbs_per_100g': 22, 'fat_per_100g': 15, 'typical_weight': 291, 'typical_calories': 660},

    # Wendy's Items
    'baconator': {'calories_per_100g': 349, 'protein_per_100g': 20, 'carbs_per_100g': 25, 'fat_per_100g': 23, 'typical_weight': 275, 'typical_calories': 960},
    'wendys baconator': {'calories_per_100g': 349, 'protein_per_100g': 20, 'carbs_per_100g': 25, 'fat_per_100g': 23, 'typical_weight': 275, 'typical_calories': 960},
    'son of baconator': {'calories_per_100g': 290, 'protein_per_100g': 18, 'carbs_per_100g': 23, 'fat_per_100g': 18, 'typical_weight': 200, 'typical_calories': 580},

    # Pizza (more accurate data)
    'pizza slice': {'calories_per_100g': 266, 'protein_per_100g': 11, 'carbs_per_100g': 33, 'fat_per_100g': 10, 'typical_weight': 100, 'typical_calories': 285},
    'pepperoni pizza': {'calories_per_100g': 298, 'protein_per_100g': 12, 'carbs_per_100g': 30, 'fat_per_100g': 15, 'typical_weight': 120, 'typical_calories': 358},
    'cheese pizza': {'calories_per_100g': 276, 'protein_per_100g': 12, 'carbs_per_100g': 33, 'fat_per_100g': 11, 'typical_weight': 100, 'typical_calories': 276},
    'margherita pizza': {'calories_per_100g': 250, 'protein_per_100g': 11, 'carbs_per_100g': 32, 'fat_per_100g': 9, 'typical_weight': 120, 'typical_calories': 300},

    # Common Foods (updated with better data)
    'apple': {'calories_per_100g': 52, 'protein_per_100g': 0.3, 'carbs_per_100g': 14, 'fat_per_100g': 0.2, 'typical_weight': 150, 'typical_calories': 78},
    'banana': {'calories_per_100g': 89, 'protein_per_100g': 1.1, 'carbs_per_100g': 23, 'fat_per_100g': 0.3, 'typical_weight': 120, 'typical_calories': 107},

    # Rice dishes (more accurate)
    'rice and beans': {'calories_per_100g': 135, 'protein_per_100g': 4.5, 'carbs_per_100g': 24, 'fat_per_100g': 2, 'typical_weight': 200, 'typical_calories': 270},
    'rice': {'calories_per_100g': 130, 'protein_per_100g': 2.7, 'carbs_per_100g': 28, 'fat_per_100g': 0.3, 'typical_weight': 150, 'typical_calories': 195},

    # Salads
    'caesar salad': {'calories_per_100g': 90, 'protein_per_100g': 3.5, 'carbs_per_100g': 6, 'fat_per_100g': 7, 'typical_weight': 200, 'typical_calories': 180},
    'green salad': {'calories_per_100g': 20, 'protein_per_100g': 1.5, 'carbs_per_100g': 4, 'fat_per_100g': 0.2, 'typical_weight': 100, 'typical_calories': 20},

    # Chicken dishes
    'grilled chicken': {'calories_per_100g': 165, 'protein_per_100g': 31, 'carbs_per_100g': 0, 'fat_per_100g': 3.6, 'typical_weight': 120, 'typical_calories': 198},
    'fried chicken': {'calories_per_100g': 320, 'protein_per_100g': 19, 'carbs_per_100g': 8, 'fat_per_100g': 24, 'typical_weight': 100, 'typical_calories': 320},

    # Sandwiches
    'sandwich': {'calories_per_100g': 250, 'protein_per_100g': 12, 'carbs_per_100g': 30, 'fat_per_100g': 10, 'typical_weight': 150, 'typical_calories': 375},
    'club sandwich': {'calories_per_100g': 280, 'protein_per_100g': 15, 'carbs_per_100g': 25, 'fat_per_100g': 15, 'typical_weight': 200, 'typical_calories': 560},

    # Mexican food
    'burrito': {'calories_per_100g': 206, 'protein_per_100g': 8, 'carbs_per_100g': 28, 'fat_per_100g': 7, 'typical_weight': 220, 'typical_calories': 453},
    'quesadilla': {'calories_per_100g': 234, 'protein_per_100g': 11, 'carbs_per_100g': 22, 'fat_per_100g': 12, 'typical_weight': 150, 'typical_calories': 351},
    'taco': {'calories_per_100g': 206, 'protein_per_100g': 10, 'carbs_per_100g': 18, 'fat_per_100g': 11, 'typical_weight': 70, 'typical_calories': 144},

    # Indian Foods
    'roti': {'calories_per_100g': 299, 'protein_per_100g': 9, 'carbs_per_100g': 50, 'fat_per_100g': 8, 'typical_weight': 40, 'typical_calories': 120},
    'chapati': {'calories_per_100g': 299, 'protein_per_100g': 9, 'carbs_per_100g': 50, 'fat_per_100g': 8, 'typical_weight': 40, 'typical_calories': 120},
    'naan': {'calories_per_100g': 310, 'protein_per_100g': 9, 'carbs_per_100g': 45, 'fat_per_100g': 12, 'typical_weight': 80, 'typical_calories': 248},
    'dal': {'calories_per_100g': 130, 'protein_per_100g': 8, 'carbs_per_100g': 20, 'fat_per_100g': 2, 'typical_weight': 150, 'typical_calories': 195},
    'dal curry': {'calories_per_100g': 130, 'protein_per_100g': 8, 'carbs_per_100g': 20, 'fat_per_100g': 2, 'typical_weight': 150, 'typical_calories': 195},
    'lentil curry': {'calories_per_100g': 130, 'protein_per_100g': 8, 'carbs_per_100g': 20, 'fat_per_100g': 2, 'typical_weight': 150, 'typical_calories': 195},
    'roti and dal': {'calories_per_100g': 180, 'protein_per_100g': 8, 'carbs_per_100g': 30, 'fat_per_100g': 4, 'typical_weight': 240, 'typical_calories': 432},  # 2 roti + dal
    'rice and dal': {'calories_per_100g': 135, 'protein_per_100g': 5, 'carbs_per_100g': 25, 'fat_per_100g': 2, 'typical_weight': 250, 'typical_calories': 338},

    # Common mixed dishes
    'pasta with sauce': {'calories_per_100g': 131, 'protein_per_100g': 5, 'carbs_per_100g': 25, 'fat_per_100g': 1.1, 'typical_weight': 250, 'typical_calories': 328},
    'spaghetti': {'calories_per_100g': 158, 'protein_per_100g': 6, 'carbs_per_100g': 31, 'fat_per_100g': 1, 'typical_weight': 200, 'typical_calories': 316},

    # Breakfast items
    'pancakes': {'calories_per_100g': 227, 'protein_per_100g': 6, 'carbs_per_100g': 28, 'fat_per_100g': 9, 'typical_weight': 80, 'typical_calories': 182},  # per pancake
    'waffle': {'calories_per_100g': 291, 'protein_per_100g': 8, 'carbs_per_100g': 33, 'fat_per_100g': 14, 'typical_weight': 75, 'typical_calories': 218},
    'french toast': {'calories_per_100g': 230, 'protein_per_100g': 8, 'carbs_per_100g': 25, 'fat_per_100g': 11, 'typical_weight': 65, 'typical_calories': 150},  # per slice
}

# Category mappings for better food recognition
FOOD_CATEGORIES = {
    'fast_food': ['big mac', 'bigmac', 'whopper', 'quarter pounder', 'mcchicken', 'baconator', 'son of baconator'],
    'pizza': ['pizza', 'pepperoni pizza', 'cheese pizza', 'margherita pizza'],
    'mexican': ['burrito', 'quesadilla', 'taco', 'salsa'],
    'asian': ['rice', 'noodles', 'sushi', 'stir fry'],
    'indian': ['roti', 'chapati', 'naan', 'dal', 'curry', 'biryani', 'tandoori', 'roti and dal', 'rice and dal'],
    'breakfast': ['pancakes', 'waffle', 'french toast', 'eggs', 'bacon'],
    'salads': ['caesar salad', 'green salad', 'garden salad'],
    'sandwiches': ['sandwich', 'club sandwich', 'blt', 'grilled cheese']
}

def get_enhanced_nutrition_data(food_name: str) -> dict:
    """Get enhanced nutrition data for a food item"""
    food_lower = food_name.lower().strip()

    # Direct lookup
    if food_lower in ENHANCED_FOOD_DATABASE:
        return ENHANCED_FOOD_DATABASE[food_lower]

    # Fuzzy matching
    for food_key, nutrition in ENHANCED_FOOD_DATABASE.items():
        if food_lower in food_key or food_key in food_lower:
            return nutrition

    # Category-based matching
    for category, foods in FOOD_CATEGORIES.items():
        for food in foods:
            if food in food_lower or food_lower in food:
                if food in ENHANCED_FOOD_DATABASE:
                    return ENHANCED_FOOD_DATABASE[food]

    return None

def calculate_accurate_calories(food_name: str, weight_grams: float = None) -> dict:
    """Calculate accurate calories using enhanced database"""
    nutrition_data = get_enhanced_nutrition_data(food_name)

    if nutrition_data:
        # Use typical weight if no weight provided
        if weight_grams is None:
            weight_grams = nutrition_data.get('typical_weight', 100)

        # Use typical calories if available, otherwise calculate from per-100g data
        if 'typical_calories' in nutrition_data and weight_grams == nutrition_data.get('typical_weight'):
            calories = nutrition_data['typical_calories']
        else:
            # Scale from per-100g data
            scale_factor = weight_grams / 100.0
            calories = nutrition_data['calories_per_100g'] * scale_factor

        return {
            'total_calories': round(calories, 1),
            'protein': round(nutrition_data.get('protein_per_100g', 0) * (weight_grams / 100.0), 1),
            'carbs': round(nutrition_data.get('carbs_per_100g', 0) * (weight_grams / 100.0), 1),
            'fat': round(nutrition_data.get('fat_per_100g', 0) * (weight_grams / 100.0), 1),
            'weight_grams': weight_grams,
            'data_source': 'enhanced_database',
            'accuracy': 'high'
        }

    return None

if __name__ == "__main__":
    # Test the enhanced database
    test_foods = ['big mac', 'BigMac', 'whopper', 'pizza', 'rice and beans']

    for food in test_foods:
        result = calculate_accurate_calories(food)
        if result:
            print(f"{food}: {result['total_calories']} calories ({result['weight_grams']}g)")
        else:
            print(f"{food}: Not found in enhanced database")