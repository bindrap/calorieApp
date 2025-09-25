#!/usr/bin/env python3
"""
Test multiple fast food items to verify hyper-accurate web search integration
"""

import sys
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from food_recognition import FoodRecognizer
from calorie_calculator import CalorieCalculator

def test_fast_food_items():
    print("🍔 Testing Multiple Fast Food Items - Hyper-Accurate System")
    print("=" * 70)

    # Test cases with expected Google calorie values
    test_cases = [
        {
            'name': 'Big Mac',
            'expected_calories': 570,
            'recognition_result': {
                'primary_food': 'Big Mac',
                'all_foods': ['Big Mac', 'hamburger'],
                'estimated_weight': 222,
                'confidence': 0.95,
                'description': 'McDonald\'s Big Mac burger'
            }
        },
        {
            'name': 'Whopper',
            'expected_calories': 660,
            'recognition_result': {
                'primary_food': 'Whopper',
                'all_foods': ['Whopper', 'burger'],
                'estimated_weight': 291,
                'confidence': 0.92,
                'description': 'Burger King Whopper'
            }
        },
        {
            'name': 'Quarter Pounder',
            'expected_calories': 520,
            'recognition_result': {
                'primary_food': 'Quarter Pounder',
                'all_foods': ['Quarter Pounder', 'burger'],
                'estimated_weight': 194,
                'confidence': 0.90,
                'description': 'McDonald\'s Quarter Pounder burger'
            }
        }
    ]

    calculator = CalorieCalculator()

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print("-" * 40)

        try:
            # Calculate calories using our enhanced system
            result = calculator.calculate_calories(test_case['recognition_result'])

            print(f"  🍔 Food: {result['food_name']}")
            print(f"  ⚖️  Weight: {result['weight_grams']}g")
            print(f"  🔥 Calories: {result['total_calories']}")
            print(f"  🥩 Protein: {result['protein']}g")
            print(f"  🍞 Carbs: {result['carbs']}g")
            print(f"  🧈 Fat: {result['fat']}g")
            print(f"  📁 Source: {result['data_source']}")

            # Accuracy check
            expected = test_case['expected_calories']
            actual = result['total_calories']
            difference = abs(actual - expected)

            print(f"\n  🎯 Accuracy Check:")
            print(f"     Expected: {expected} calories")
            print(f"     Actual: {actual} calories")
            print(f"     Difference: {difference} calories")

            if difference <= 30:
                print(f"     ✅ EXCELLENT! (±30 calories)")
            elif difference <= 60:
                print(f"     ⚠️  GOOD (±60 calories)")
            else:
                print(f"     ❌ NEEDS IMPROVEMENT (>{60} calories off)")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n🎉 Test Complete! The system should now provide hyper-accurate")
    print(f"   calorie data for fast food items via web search integration.")

if __name__ == "__main__":
    test_fast_food_items()