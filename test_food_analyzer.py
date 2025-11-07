#!/usr/bin/env python3
"""Test food analyzer accuracy with various foods"""

from food_recognition import FoodRecognizer
import json

# Initialize recognizer
print("🔧 Initializing Food Recognizer with Ollama Cloud...\n")
recognizer = FoodRecognizer()

# Test various food descriptions
test_foods = [
    ("Big Mac", "McDonald's Big Mac burger"),
    ("Grilled chicken breast", "200g grilled chicken breast"),
    ("Banana", "Medium banana"),
    ("Greek yogurt", "Plain Greek yogurt 200g"),
    ("Pizza slice", "Large pepperoni pizza slice"),
    ("Avocado", "Whole avocado"),
    ("Protein shake", "Whey protein shake with milk"),
    ("Steak", "8oz ribeye steak"),
    ("Oatmeal", "Bowl of oatmeal with berries"),
    ("Eggs", "3 scrambled eggs")
]

print("=" * 80)
print("FOOD ANALYZER TEST RESULTS")
print("=" * 80)

for i, (food_name, description) in enumerate(test_foods, 1):
    print(f"\n{'─' * 80}")
    print(f"Test {i}/10: {description}")
    print(f"{'─' * 80}")

    try:
        # Test AI enhancement with user description
        result = recognizer._enhance_with_ai(
            image_analysis={'food_name': food_name},
            user_description=description
        )

        if result:
            print(f"✅ AI Enhancement Successful")
            print(f"   Food: {result.get('food_name', 'Unknown')}")
            print(f"   Weight: {result.get('estimated_weight_grams', 0)}g")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
            print(f"   Description: {result.get('description', 'N/A')[:100]}")
        else:
            print(f"❌ AI Enhancement failed - no result returned")

    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n{'=' * 80}")
print("✅ Test Complete!")
print(f"{'=' * 80}\n")

# Test connection
print("\n🔌 Testing Ollama Cloud connection...")
if recognizer.test_connection():
    print("✅ Ollama Cloud connection: WORKING")
else:
    print("❌ Ollama Cloud connection: FAILED")
