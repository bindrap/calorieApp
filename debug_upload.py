#!/usr/bin/env python3
"""
Debug script to test the upload and food recognition process
"""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, '/mnt/c/Users/bindrap/Documents/calorieApp')

from food_recognition import FoodRecognizer
from calorie_calculator import CalorieCalculator
from PIL import Image, ImageDraw
import tempfile

def create_test_image():
    """Create a test food image"""
    img = Image.new('RGB', (300, 300), color='orange')
    draw = ImageDraw.Draw(img)

    # Draw pizza-like elements
    draw.ellipse([50, 50, 250, 250], fill='red', outline='brown', width=5)
    draw.ellipse([100, 100, 140, 140], fill='yellow')
    draw.ellipse([160, 120, 200, 160], fill='yellow')

    # Save to static/uploads directory like the real app
    uploads_dir = Path('/mnt/c/Users/bindrap/Documents/calorieApp/static/uploads')
    uploads_dir.mkdir(exist_ok=True)

    test_file = uploads_dir / 'test_pizza_margherita.jpg'
    img.save(test_file, 'JPEG')

    return str(test_file)

def debug_upload_process():
    """Debug the entire upload process step by step"""
    print("🔍 Debugging Upload Process")
    print("=" * 40)

    # Step 1: Create test image
    print("📸 Step 1: Creating test image...")
    try:
        image_path = create_test_image()
        print(f"✅ Test image created: {image_path}")
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return

    # Step 2: Initialize food recognizer
    print("\n🤖 Step 2: Initializing food recognizer...")
    try:
        food_recognizer = FoodRecognizer()
        print("✅ Food recognizer initialized")

        # Test connection
        if food_recognizer.test_connection():
            print("✅ API connection successful")
        else:
            print("❌ API connection failed")
            return

    except Exception as e:
        print(f"❌ Failed to initialize food recognizer: {e}")
        return

    # Step 3: Analyze image
    print("\n🔍 Step 3: Analyzing image...")
    try:
        recognition_result = food_recognizer.analyze_image(image_path)
        print("✅ Image analysis completed")
        print(f"📋 Recognition result: {recognition_result}")
    except Exception as e:
        print(f"❌ Image analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Step 4: Calculate calories
    print("\n🧮 Step 4: Calculating calories...")
    try:
        calorie_calculator = CalorieCalculator()
        calorie_result = calorie_calculator.calculate_calories(recognition_result)
        print("✅ Calorie calculation completed")
        print(f"📋 Calorie result: {calorie_result}")
    except Exception as e:
        print(f"❌ Calorie calculation failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # Step 5: Simulate database entry creation
    print("\n💾 Step 5: Simulating database entry...")
    try:
        # This is what the Flask app would create
        food_entry_data = {
            'user_id': 1,  # Test user
            'food_name': recognition_result['primary_food'],
            'estimated_weight_grams': recognition_result.get('estimated_weight'),
            'calories': calorie_result['total_calories'],
            'protein': calorie_result.get('protein', 0),
            'carbs': calorie_result.get('carbs', 0),
            'fat': calorie_result.get('fat', 0),
            'ai_confidence_score': recognition_result.get('confidence'),
            'ai_identified_foods': str(recognition_result.get('all_foods', [])),
            'original_ai_food_name': recognition_result['primary_food'],
            'image_filename': Path(image_path).name,
            'image_path': image_path,
        }

        print("✅ Database entry data prepared:")
        for key, value in food_entry_data.items():
            print(f"  {key}: {value}")

    except Exception as e:
        print(f"❌ Database entry preparation failed: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n🎉 All steps completed successfully!")
    print("The upload process should work in the web app.")

    # Clean up
    try:
        os.unlink(image_path)
        print("🧹 Test file cleaned up")
    except:
        pass

if __name__ == "__main__":
    debug_upload_process()