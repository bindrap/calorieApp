#!/usr/bin/env python3
"""
Test the fixed food recognition module
"""

from food_recognition import FoodRecognizer
from PIL import Image
import io
import base64
import tempfile

def create_test_image():
    """Create a simple test food image"""
    # Create a simple image that looks like a pizza
    img = Image.new('RGB', (300, 300), color='red')  # Red base

    # Add some yellow circles for cheese
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)

    # Draw some pizza-like elements
    draw.ellipse([50, 50, 100, 100], fill='yellow')  # Cheese
    draw.ellipse([150, 80, 200, 130], fill='yellow')  # More cheese
    draw.ellipse([100, 150, 150, 200], fill='green')  # Pepperoni/vegetables
    draw.ellipse([180, 180, 230, 230], fill='brown')  # Pepperoni

    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        img.save(f.name, 'JPEG')
        return f.name

def test_food_recognition():
    print("🧪 Testing Fixed Food Recognition")
    print("=" * 40)

    # Initialize recognizer
    recognizer = FoodRecognizer()

    # Test connection first
    print("🔄 Testing connection...")
    if recognizer.test_connection():
        print("✅ Connection test passed")
    else:
        print("❌ Connection test failed")
        return

    # Create test image
    print("🔄 Creating test image...")
    test_image_path = create_test_image()
    print(f"✅ Test image created: {test_image_path}")

    # Analyze the image
    print("🔄 Analyzing test image...")
    try:
        result = recognizer.analyze_image(test_image_path)

        print("\n📋 Recognition Results:")
        print(f"Primary Food: {result['primary_food']}")
        print(f"All Foods: {result['all_foods']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Estimated Weight: {result['estimated_weight']}g")
        print(f"Description: {result['description']}")

        if result['confidence'] > 0.5:
            print("✅ Recognition successful!")
        else:
            print("⚠️ Low confidence, but working")

    except Exception as e:
        print(f"❌ Recognition failed: {e}")

    # Clean up
    import os
    try:
        os.unlink(test_image_path)
    except:
        pass

if __name__ == "__main__":
    test_food_recognition()