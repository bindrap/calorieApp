#!/usr/bin/env python3
"""
Test fuzzy matching learning system
"""

import os
import sys
sys.path.append('/app')

from app import app, get_learning_context, apply_learning_adjustments

def test_fuzzy_matching():
    """Test fuzzy matching for your specific food example"""

    # Test food names from your corrections
    test_foods = [
        "cold cut sliced deli meat",  # The new upload that didn't work
        "sliced cold cut ham",        # Your second correction
        "cold cut slices (deli meat)" # Your first correction
    ]

    print("Testing fuzzy matching for cold cut foods...")
    print("=" * 50)

    for food_name in test_foods:
        print(f"\nTesting: '{food_name}'")

        # Get learning context
        context = get_learning_context(user_id=1, food_name=food_name)

        print(f"  Exact corrections: {len(context['exact_corrections'])}")
        print(f"  Fuzzy corrections: {len(context['fuzzy_corrections'])}")

        if context['exact_corrections']:
            print("  Exact matches found:")
            for correction in context['exact_corrections']:
                print(f"    - {correction.ai_food_name} -> {correction.corrected_food_name}")
                print(f"      Calories: {correction.ai_calories} -> {correction.corrected_calories}")

        if context['fuzzy_corrections']:
            print("  Fuzzy matches found:")
            for correction in context['fuzzy_corrections']:
                print(f"    - {correction.ai_food_name} -> {correction.corrected_food_name}")
                print(f"      Calories: {correction.ai_calories} -> {correction.corrected_calories}")

        # Test learning adjustments
        analysis_result = {
            'food_name': food_name,
            'weight_grams': 100,
            'calories': 250,  # Simulated AI prediction
            'protein': 15,
            'carbs': 20,
            'fat': 10
        }

        print(f"  Original prediction: {analysis_result['calories']} calories")

        # Apply learning
        adjusted_result = apply_learning_adjustments(analysis_result, user_id=1)

        print(f"  After learning: {adjusted_result['calories']} calories")

        if 'learning_applied' in adjusted_result:
            print(f"  Learning applied: {adjusted_result['learning_applied']}")
        else:
            print("  No learning applied")

if __name__ == "__main__":
    with app.app_context():
        test_fuzzy_matching()