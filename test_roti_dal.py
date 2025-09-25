#!/usr/bin/env python3
"""
Test roti dal calculation to understand why it's showing 196 calories instead of 350-500
"""

import sys
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from food_recognition import FoodRecognizer
from calorie_calculator import CalorieCalculator
from enhanced_food_database import get_enhanced_nutrition_data, calculate_accurate_calories

def test_roti_dal_calculation():
    print("🍽️ Testing Roti Dal Calorie Calculation")
    print("Expected: 350-500 calories (Google)")
    print("Current System: 196 calories (150g)")
    print("=" * 60)

    # Test what our system would recognize from the filename
    print("\n1️⃣ Testing Food Recognition from Filename:")
    recognizer = FoodRecognizer()

    # Simulate what happens when rotiDal.jpeg is analyzed
    mock_filepath = "static/uploads/rotiDal.jpeg"

    try:
        # This should call our recognition system
        result = recognizer.analyze_image(mock_filepath)

        print("📋 Recognition Results:")
        print(f"  Primary Food: {result['primary_food']}")
        print(f"  All Foods: {result['all_foods']}")
        print(f"  Estimated Weight: {result['estimated_weight']}g")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Description: {result['description']}")

        # Now test calorie calculation
        print(f"\n2️⃣ Testing Calorie Calculation:")
        calculator = CalorieCalculator()
        calorie_result = calculator.calculate_calories(result)

        print(f"  🔥 Calories: {calorie_result['total_calories']}")
        print(f"  🥩 Protein: {calorie_result['protein']}g")
        print(f"  🍞 Carbs: {calorie_result['carbs']}g")
        print(f"  🧈 Fat: {calorie_result['fat']}g")
        print(f"  📁 Source: {calorie_result['data_source']}")

        # Analyze the issue
        expected_min = 350
        expected_max = 500
        actual = calorie_result['total_calories']

        print(f"\n📊 ACCURACY ANALYSIS:")
        print(f"  Expected Range: {expected_min}-{expected_max} calories")
        print(f"  Actual Result: {actual} calories")
        print(f"  Difference: {expected_min - actual} to {expected_max - actual} calories short")
        print(f"  Percentage Error: {((expected_min + expected_max)/2 - actual) / ((expected_min + expected_max)/2) * 100:.1f}% too low")

        if actual < expected_min:
            print(f"\n❌ MAJOR ISSUE: Severely underestimating calories!")
            print(f"💡 LIKELY PROBLEMS:")
            print(f"  1. Weight estimation too low (150g for roti+dal is very light)")
            print(f"  2. Missing Indian foods from enhanced database")
            print(f"  3. System treating as single food instead of combination")
            print(f"  4. Roti calories underestimated (should be ~100 cal each)")
            print(f"  5. Dal calories underestimated (should be ~150-200 cal per serving)")

    except Exception as e:
        print(f"❌ Error during recognition: {e}")
        import traceback
        traceback.print_exc()

    # Test individual components
    print(f"\n3️⃣ Testing Individual Components:")

    # Test roti calculation
    print(f"\n🥖 Individual Roti Test:")
    test_foods = [
        {'name': 'roti', 'weight': 40, 'expected': 100},  # 1 roti ~40g, ~100 cal
        {'name': 'chapati', 'weight': 40, 'expected': 100},
        {'name': 'dal', 'weight': 150, 'expected': 200},  # 1 serving dal ~150g, ~200 cal
        {'name': 'lentil curry', 'weight': 150, 'expected': 200}
    ]

    calculator = CalorieCalculator()

    for food_test in test_foods:
        recognition_result = {
            'primary_food': food_test['name'],
            'all_foods': [food_test['name']],
            'estimated_weight': food_test['weight'],
            'confidence': 0.85
        }

        result = calculator.calculate_calories(recognition_result)
        expected = food_test['expected']
        actual = result['total_calories']

        print(f"  {food_test['name']:15} ({food_test['weight']}g): {actual:6.1f} cal (expected {expected:3d} cal) - {'✅' if abs(actual - expected) < 30 else '❌'}")

    print(f"\n🎯 RECOMMENDED FIXES:")
    print(f"  1. Add Indian foods to enhanced database:")
    print(f"     - roti/chapati: ~250 cal/100g (40g = 100 cal)")
    print(f"     - dal: ~130 cal/100g (150g = 195 cal)")
    print(f"  2. Improve multi-food detection for combination plates")
    print(f"  3. Better weight estimation for Indian meals")
    print(f"  4. Total for 2 rotis + dal should be: 300-350 calories minimum")

if __name__ == "__main__":
    test_roti_dal_calculation()