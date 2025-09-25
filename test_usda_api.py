#!/usr/bin/env python3
"""
Test USDA API integration with the provided API key
"""

import sys
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from calorie_calculator import CalorieCalculator

def test_usda_api():
    print("🇺🇸 Testing USDA API Integration")
    print("API Key: bSMXb6Dq3W5l1ebpOKvpaBUNHocBCZkfdkTTw0n1")
    print("=" * 50)

    calculator = CalorieCalculator()

    # Test foods that should be in USDA database
    test_foods = [
        {'name': 'apple', 'weight': 150},
        {'name': 'banana', 'weight': 120},
        {'name': 'chicken breast', 'weight': 100},
        {'name': 'broccoli', 'weight': 100},
        {'name': 'rice', 'weight': 150}
    ]

    for food_test in test_foods:
        print(f"\n🧪 Testing: {food_test['name']} ({food_test['weight']}g)")
        print("-" * 30)

        # Create mock recognition result
        recognition_result = {
            'primary_food': food_test['name'],
            'all_foods': [food_test['name']],
            'estimated_weight': food_test['weight'],
            'confidence': 0.85,
            'description': f'Testing {food_test["name"]} with USDA API'
        }

        try:
            result = calculator.calculate_calories(recognition_result)

            print(f"  🔥 Calories: {result['total_calories']}")
            print(f"  🥩 Protein: {result['protein']}g")
            print(f"  🍞 Carbs: {result['carbs']}g")
            print(f"  🧈 Fat: {result['fat']}g")
            print(f"  📁 Source: {result['data_source']}")

            if result['data_source'] == 'calculated' and calculator.usda_api_key:
                print("  ✅ USDA API successfully used!")
            elif result['data_source'] == 'enhanced_database':
                print("  ✅ Enhanced database used (priority over USDA)")
            else:
                print(f"  ⚠️ Using fallback method: {result['data_source']}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n🎯 USDA API Integration Status:")
    if calculator.usda_api_key:
        print(f"  ✅ API Key configured: {calculator.usda_api_key[:20]}...")
        print(f"  🌐 Base URL: {calculator.usda_base_url}")
        print(f"  📊 Should provide government-verified nutrition data")
    else:
        print(f"  ❌ No API key configured")

if __name__ == "__main__":
    test_usda_api()