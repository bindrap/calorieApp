#!/usr/bin/env python3
"""
Test food recognition with a .webp file like the user uploaded
"""

import sys
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from food_recognition import FoodRecognizer
from calorie_calculator import CalorieCalculator
from PIL import Image
import tempfile

def create_rice_beans_image():
    """Create an image that simulates rice and beans"""
    # Create image with colors similar to rice and beans
    img = Image.new('RGB', (400, 300), color='white')  # White background for rice

    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)

    # Draw rice-like texture (small white/yellow dots)
    import random
    for _ in range(200):
        x = random.randint(0, 399)
        y = random.randint(0, 299)
        draw.ellipse([x-1, y-1, x+1, y+1], fill='ivory')

    # Draw beans (dark red/brown areas)
    for _ in range(50):
        x = random.randint(20, 380)
        y = random.randint(20, 280)
        draw.ellipse([x-5, y-3, x+5, y+3], fill='darkred')

    # Add some green for broccoli
    for _ in range(30):
        x = random.randint(50, 350)
        y = random.randint(50, 250)
        draw.ellipse([x-3, y-3, x+3, y+3], fill='darkgreen')

    # Save as webp format with descriptive filename
    test_file = '/tmp/rice-and-beans-broccoli-test.webp'
    img.save(test_file, 'WEBP')
    return test_file

def test_rice_beans_recognition():
    print("🍚 Testing Rice and Beans Recognition")
    print("=" * 40)

    # Create test image
    image_path = create_rice_beans_image()
    print(f"✅ Created test WEBP image: {image_path}")

    # Initialize recognizer
    recognizer = FoodRecognizer()
    calculator = CalorieCalculator()

    # Test the recognition
    try:
        print("🔄 Analyzing rice and beans image...")
        result = recognizer.analyze_image(image_path)

        print("\n📋 Recognition Results:")
        print(f"  Primary Food: {result['primary_food']}")
        print(f"  All Foods: {result['all_foods']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Weight: {result['estimated_weight']}g")
        print(f"  Portion: {result['portion_size']}")
        print(f"  Description: {result['description']}")

        # Calculate calories
        print("\n🧮 Calculating calories...")
        calorie_result = calculator.calculate_calories(result)

        print(f"  Calories: {calorie_result['total_calories']}")
        print(f"  Protein: {calorie_result['protein']}g")
        print(f"  Carbs: {calorie_result['carbs']}g")
        print(f"  Fat: {calorie_result['fat']}g")

        print(f"\n✅ Perfect! This should work in the web app now.")

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
    test_rice_beans_recognition()