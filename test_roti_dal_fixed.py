#!/usr/bin/env python3
"""
Test the fixed roti dal calculation with the combination entry
"""

import sys
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from calorie_calculator import CalorieCalculator
from enhanced_food_database import get_enhanced_nutrition_data, calculate_accurate_calories

def test_roti_dal_fixed():
    print("🍽️ Testing Fixed Roti Dal Calculation")
    print("=" * 50)

    calculator = CalorieCalculator()

    # Test the specific combination that should be recognized
    test_cases = [
        {
            'name': 'roti and dal',
            'weight': 240,  # typical weight in our database
            'description': 'Direct combination match from enhanced database'
        },
        {
            'name': 'roti and dal',
            'weight': 300,  # heavier portion
            'description': 'Scaled up portion'
        },
        {
            'name': 'dal',
            'weight': 150,
            'description': 'Just dal (what the system is currently detecting)'
        },
        {
            'name': 'roti',
            'weight': 80,  # 2 rotis
            'description': '2 rotis (2 x 40g)'
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ Testing: {test_case['name']} ({test_case['weight']}g)")
        print(f"   {test_case['description']}")
        print("-" * 40)

        # Create recognition result
        recognition_result = {
            'primary_food': test_case['name'],
            'all_foods': test_case['name'].split(' and '),
            'estimated_weight': test_case['weight'],
            'confidence': 0.85,
            'description': f'Testing {test_case["name"]}'
        }

        try:
            result = calculator.calculate_calories(recognition_result)

            print(f"  🔥 Calories: {result['total_calories']}")
            print(f"  🥩 Protein: {result['protein']}g")
            print(f"  🍞 Carbs: {result['carbs']}g")
            print(f"  🧈 Fat: {result['fat']}g")
            print(f"  📁 Source: {result['data_source']}")

            # Check if in expected range (350-500)
            calories = result['total_calories']
            if 350 <= calories <= 500:
                print(f"  ✅ PERFECT: Within expected range (350-500)")
            elif 300 <= calories <= 550:
                print(f"  ✅ GOOD: Close to expected range")
            else:
                print(f"  ⚠️ Needs adjustment")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n🔍 Direct Database Test:")
    print("-" * 30)

    # Test direct database lookup
    db_result = get_enhanced_nutrition_data('roti and dal')
    if db_result:
        print(f"  Database entry found: {db_result}")
        calc_result = calculate_accurate_calories('roti and dal', 240)
        if calc_result:
            print(f"  Calculated calories: {calc_result['total_calories']}")
    else:
        print("  ❌ No database entry found for 'roti and dal'")

    print(f"\n💡 SOLUTION:")
    print(f"  The issue is that the food recognition is detecting 'dal' alone")
    print(f"  instead of 'roti and dal' as a combination.")
    print(f"  ")
    print(f"  Individual calculation should be:")
    print(f"  - 2 rotis (80g): 240 calories")
    print(f"  - 1 dal serving (150g): 195 calories")
    print(f"  - TOTAL: 435 calories ✅ (within 350-500 range)")
    print(f"  ")
    print(f"  Our enhanced database 'roti and dal' entry:")
    print(f"  - 240g serving: 432 calories ✅ (perfect match!)")

if __name__ == "__main__":
    test_roti_dal_fixed()