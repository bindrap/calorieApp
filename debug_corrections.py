#!/usr/bin/env python3
"""
Debug correction values
"""

import os
import sys
sys.path.append('/app')

from app import app, UserFeedback

def debug_corrections():
    """Debug correction values for cold cut foods"""

    print("Checking cold cut correction values...")
    print("=" * 50)

    with app.app_context():
        corrections = UserFeedback.query.filter(UserFeedback.ai_food_name.like('%cold cut%')).all()

        for correction in corrections:
            print(f"AI Food Name: {correction.ai_food_name}")
            print(f"Corrected Food Name: {correction.corrected_food_name}")
            print(f"AI Calories: {correction.ai_calories}")
            print(f"Corrected Calories: {correction.corrected_calories}")
            print(f"AI Weight: {correction.ai_weight_grams}")
            print(f"Corrected Weight: {correction.corrected_weight_grams}")
            print(f"Correction Type: {correction.correction_type}")
            print("-" * 30)

if __name__ == "__main__":
    debug_corrections()