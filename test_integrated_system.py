#!/usr/bin/env python3
"""
Test the integrated calorie calculation system with hyper-accurate web search
This should now show Big Mac with 570 calories instead of 480
"""

import sys
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from food_recognition import FoodRecognizer
from calorie_calculator import CalorieCalculator
import tempfile
from PIL import Image, ImageDraw
import random

def create_big_mac_image():
    """Create a test image that looks like a Big Mac"""
    img = Image.new('RGB', (400, 300), color='lightgray')
    draw = ImageDraw.Draw(img)

    # Draw burger layers
    # Bottom bun (tan)
    draw.ellipse([100, 200, 300, 280], fill='tan')
    # Lettuce (green)
    draw.ellipse([110, 180, 290, 200], fill='green')
    # Meat patty (brown)
    draw.ellipse([120, 160, 280, 180], fill='saddlebrown')
    # Cheese (yellow)
    draw.ellipse([115, 150, 285, 165], fill='gold')
    # Middle bun (tan)
    draw.ellipse([110, 130, 290, 155], fill='tan')
    # More lettuce
    draw.ellipse([115, 120, 285, 135], fill='green')
    # Second patty
    draw.ellipse([120, 100, 280, 120], fill='saddlebrown')
    # Top bun (tan with sesame seeds)
    draw.ellipse([105, 80, 295, 110], fill='tan')

    # Add sesame seeds (small white dots)
    for _ in range(8):
        x = random.randint(140, 260)
        y = random.randint(85, 95)
        draw.ellipse([x-2, y-2, x+2, y+2], fill='white')

    # Save as PNG with descriptive filename
    test_file = '/tmp/big-mac-test.png'
    img.save(test_file, 'PNG')
    return test_file

def test_big_mac_accuracy():
    print("🍔 Testing Big Mac Hyper-Accurate Calorie Calculation")
    print("=" * 60)

    # Create test image
    image_path = create_big_mac_image()
    print(f"✅ Created test Big Mac image: {image_path}")

    # Initialize systems
    recognizer = FoodRecognizer()
    calculator = CalorieCalculator()

    try:
        print("\n🔄 Step 1: Analyzing Big Mac image...")
        result = recognizer.analyze_image(image_path)

        print("📋 Recognition Results:")
        print(f"  Primary Food: {result['primary_food']}")
        print(f"  All Foods: {result['all_foods']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Weight: {result['estimated_weight']}g")
        print(f"  Description: {result['description']}")

        print("\n🧮 Step 2: Calculating hyper-accurate calories...")
        calorie_result = calculator.calculate_calories(result)

        print("\n📊 NUTRITION RESULTS:")
        print(f"  🍔 Food: {calorie_result['food_name']}")
        print(f"  ⚖️  Weight: {calorie_result['weight_grams']}g")
        print(f"  🔥 Calories: {calorie_result['total_calories']}")
        print(f"  🥩 Protein: {calorie_result['protein']}g")
        print(f"  🍞 Carbs: {calorie_result['carbs']}g")
        print(f"  🧈 Fat: {calorie_result['fat']}g")
        print(f"  📁 Data Source: {calorie_result['data_source']}")

        if 'confidence_score' in calorie_result:
            print(f"  🎯 Confidence: {calorie_result['confidence_score']:.2f}")
        if 'brand' in calorie_result:
            print(f"  🏢 Brand: {calorie_result['brand']}")
        if 'source' in calorie_result:
            print(f"  🌐 Source: {calorie_result['source']}")

        # Check accuracy
        expected_calories = 570  # Google says Big Mac = 570 calories
        actual_calories = calorie_result['total_calories']

        print(f"\n🎯 ACCURACY CHECK:")
        print(f"  Expected (Google): {expected_calories} calories")
        print(f"  Our Result: {actual_calories} calories")
        print(f"  Difference: {abs(actual_calories - expected_calories)} calories")

        if abs(actual_calories - expected_calories) <= 50:
            print(f"  ✅ EXCELLENT! Within 50 calories of expected value")
        elif abs(actual_calories - expected_calories) <= 100:
            print(f"  ⚠️  GOOD: Within 100 calories of expected value")
        else:
            print(f"  ❌ NEEDS IMPROVEMENT: More than 100 calories difference")

        # Show improvement from old system
        old_estimate = 480.7  # Previous result
        print(f"\n📈 IMPROVEMENT:")
        print(f"  Old System: {old_estimate} calories (off by {abs(old_estimate - expected_calories)})")
        print(f"  New System: {actual_calories} calories (off by {abs(actual_calories - expected_calories)})")

        if abs(actual_calories - expected_calories) < abs(old_estimate - expected_calories):
            print(f"  🎉 SUCCESS: New system is more accurate!")
        else:
            print(f"  ⚠️  May need further tuning")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    # Clean up
    import os
    try:
        os.unlink(image_path)
    except:
        pass

if __name__ == "__main__":
    test_big_mac_accuracy()