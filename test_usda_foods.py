#!/usr/bin/env python3
"""
Test foods that should use USDA API (not in enhanced database)
"""

import sys
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from calorie_calculator import CalorieCalculator

def test_usda_foods():
    print("🇺🇸 Testing USDA API for Non-Enhanced Foods")
    print("=" * 50)

    calculator = CalorieCalculator()

    # Test foods that should NOT be in enhanced database
    test_foods = [
        {'name': 'carrots', 'weight': 100, 'expected_range': (35, 45)},
        {'name': 'spinach', 'weight': 100, 'expected_range': (20, 30)},
        {'name': 'sweet potato', 'weight': 100, 'expected_range': (80, 90)},
        {'name': 'quinoa', 'weight': 100, 'expected_range': (120, 140)},
        {'name': 'almonds', 'weight': 100, 'expected_range': (570, 600)}
    ]

    successful_usda_calls = 0

    for food_test in test_foods:
        print(f"\n🧪 Testing: {food_test['name']} ({food_test['weight']}g)")
        print(f"   Expected range: {food_test['expected_range'][0]}-{food_test['expected_range'][1]} calories")
        print("-" * 40)

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

            # Check if we used USDA
            if result['data_source'] == 'calculated' and calculator.usda_api_key:
                print("  ✅ USDA API used successfully!")
                successful_usda_calls += 1

                # Check if in expected range
                min_cal, max_cal = food_test['expected_range']
                actual_cal = result['total_calories']
                if min_cal <= actual_cal <= max_cal:
                    print(f"  🎯 ACCURATE: Within expected range!")
                else:
                    print(f"  ⚠️ Outside expected range (may need query adjustment)")

            elif result['data_source'] == 'enhanced_database':
                print("  ✅ Enhanced database used (higher priority)")
            else:
                print(f"  ⚠️ Fallback used: {result['data_source']}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n📊 USDA API Summary:")
    print(f"  ✅ Successful USDA calls: {successful_usda_calls}/{len(test_foods)}")
    print(f"  🔑 API Key configured: {'Yes' if calculator.usda_api_key else 'No'}")

    if successful_usda_calls > 0:
        print(f"  🎉 USDA integration working! Getting government-verified nutrition data.")
    else:
        print(f"  ⚠️ USDA API not being used - check network or API limits.")

if __name__ == "__main__":
    test_usda_foods()