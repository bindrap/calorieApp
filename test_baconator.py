#!/usr/bin/env python3
"""
Test Baconator calculation to see why it's 791 calories instead of 960
"""

import sys
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from food_recognition import FoodRecognizer
from calorie_calculator import CalorieCalculator
from enhanced_food_database import get_enhanced_nutrition_data, calculate_accurate_calories
from web_search_nutrition import WebSearchNutritionCalculator

def test_baconator_calculation():
    print("🥓 Testing Baconator Calorie Calculation")
    print("Expected: 960 calories (Google)")
    print("Current: 791 calories (Our system)")
    print("=" * 50)

    # Test direct enhanced database lookup
    print("\n1️⃣ Testing Enhanced Database:")
    enhanced_data = get_enhanced_nutrition_data('baconator')
    if enhanced_data:
        result = calculate_accurate_calories('baconator')
        print(f"   Enhanced DB result: {result}")
    else:
        print("   ❌ Baconator not found in enhanced database")

    # Test web search
    print("\n2️⃣ Testing Web Search:")
    web_calculator = WebSearchNutritionCalculator()
    web_result = web_calculator.get_web_search_nutrition('baconator', 275)  # Typical Baconator weight
    if web_result:
        print(f"   🌐 Web search result: {web_result.get('calories')} calories")
        print(f"   🎯 Confidence: {web_result.get('confidence', 0)}")
        print(f"   📄 Source: {web_result.get('source', 'unknown')}")
    else:
        print("   ❌ Web search failed")

    # Test full recognition pipeline
    print("\n3️⃣ Testing Full Pipeline:")
    # Simulate recognition result
    recognition_result = {
        'primary_food': 'Baconator',
        'all_foods': ['Baconator', 'burger', 'hamburger'],
        'estimated_weight': 275,
        'confidence': 0.90,
        'description': 'Wendy\'s Baconator burger'
    }

    calculator = CalorieCalculator()
    final_result = calculator.calculate_calories(recognition_result)

    print(f"   🍔 Food: {final_result['food_name']}")
    print(f"   ⚖️  Weight: {final_result['weight_grams']}g")
    print(f"   🔥 Calories: {final_result['total_calories']}")
    print(f"   🥩 Protein: {final_result['protein']}g")
    print(f"   🍞 Carbs: {final_result['carbs']}g")
    print(f"   🧈 Fat: {final_result['fat']}g")
    print(f"   📁 Source: {final_result['data_source']}")

    # Analysis
    expected = 960
    actual = final_result['total_calories']
    difference = abs(actual - expected)

    print(f"\n📊 ACCURACY ANALYSIS:")
    print(f"   Expected: {expected} calories")
    print(f"   Actual: {actual} calories")
    print(f"   Difference: {difference} calories ({difference/expected*100:.1f}% off)")

    if difference > 100:
        print(f"   ❌ ISSUE: Large difference detected!")
        print(f"   💡 RECOMMENDATIONS:")
        print(f"      - Add Baconator to enhanced database with correct data")
        print(f"      - Improve web search prompt for Wendy's items")
        print(f"      - Check if recognition is identifying as generic 'burger'")

if __name__ == "__main__":
    test_baconator_calculation()