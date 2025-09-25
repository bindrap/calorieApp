#!/usr/bin/env python3
"""
Test the working food recognition module
"""

from food_recognition import FoodRecognizer
from PIL import Image, ImageDraw
import tempfile
import os

def create_test_images():
    """Create test images with different types of foods"""
    test_images = []

    # Create a pizza-like image
    img1 = Image.new('RGB', (300, 300), color='red')
    draw1 = ImageDraw.Draw(img1)
    draw1.ellipse([50, 50, 250, 250], fill='orange', outline='brown', width=5)
    draw1.ellipse([100, 100, 140, 140], fill='yellow')  # Cheese
    draw1.ellipse([160, 120, 200, 160], fill='yellow')  # More cheese

    with tempfile.NamedTemporaryFile(suffix='_pizza_margherita.jpg', delete=False) as f:
        img1.save(f.name, 'JPEG')
        test_images.append(('Pizza', f.name))

    # Create a salad-like image
    img2 = Image.new('RGB', (300, 300), color='white')
    draw2 = ImageDraw.Draw(img2)
    draw2.ellipse([50, 50, 250, 250], fill='lightgreen')
    draw2.ellipse([80, 80, 120, 120], fill='red')  # Tomato
    draw2.ellipse([180, 90, 220, 130], fill='red')  # More tomato

    with tempfile.NamedTemporaryFile(suffix='_caesar_salad.jpg', delete=False) as f:
        img2.save(f.name, 'JPEG')
        test_images.append(('Salad', f.name))

    # Create an unknown food image
    img3 = Image.new('RGB', (300, 300), color='purple')
    draw3 = ImageDraw.Draw(img3)
    draw3.rectangle([100, 100, 200, 200], fill='blue')

    with tempfile.NamedTemporaryFile(suffix='_unknown_food.jpg', delete=False) as f:
        img3.save(f.name, 'JPEG')
        test_images.append(('Unknown', f.name))

    return test_images

def test_food_recognition():
    print("🧪 Testing Working Food Recognition System")
    print("=" * 50)

    # Initialize recognizer
    recognizer = FoodRecognizer()

    # Test connection first
    print("🔄 Testing API connection...")
    if recognizer.test_connection():
        print("✅ API connection successful!")
    else:
        print("❌ API connection failed!")
        return

    # Create test images
    print("\n🔄 Creating test images...")
    test_images = create_test_images()
    print(f"✅ Created {len(test_images)} test images")

    # Test each image
    for expected_type, image_path in test_images:
        print(f"\n🔄 Testing {expected_type} image: {os.path.basename(image_path)}")

        try:
            result = recognizer.analyze_image(image_path)

            print(f"📋 Results:")
            print(f"  Primary Food: {result['primary_food']}")
            print(f"  All Foods: {result['all_foods']}")
            print(f"  Confidence: {result['confidence']:.2f}")
            print(f"  Estimated Weight: {result['estimated_weight']}g")
            print(f"  Portion Size: {result['portion_size']}")
            print(f"  Description: {result['description']}")

            # Check if it's reasonable
            if result['confidence'] > 0.5:
                print(f"✅ Good confidence recognition!")
            elif result['confidence'] > 0.3:
                print(f"⚠️ Moderate confidence, acceptable")
            else:
                print(f"⚠️ Low confidence, but working")

        except Exception as e:
            print(f"❌ Recognition failed: {e}")

    # Clean up
    print(f"\n🧹 Cleaning up test files...")
    for _, image_path in test_images:
        try:
            os.unlink(image_path)
        except:
            pass

    print("\n✅ Testing complete!")

if __name__ == "__main__":
    test_food_recognition()