#!/usr/bin/env python3
"""
Test workout calorie calculation
"""

import os
import sys
sys.path.append('/app')

from app import app, calculate_calories_burned

def test_workout_calculations():
    """Test the MET-based calorie calculation"""

    print("Testing workout calorie calculations...")
    print("=" * 50)

    # Test weight in kg
    weight_kg = 70.0  # 70kg person

    # Test cases: (activity, intensity, duration_minutes, expected_approx_calories)
    test_cases = [
        ("Jiu Jitsu", "high", 60, 700),  # 10 MET * 70kg * 1hr = 700 cal
        ("Running", "high", 30, 385),    # 11 MET * 70kg * 0.5hr = 385 cal
        ("Weight Training", "moderate", 45, 252),  # 4.8 MET * 70kg * 0.75hr = 252 cal
        ("Yoga", "light", 30, 87.5),     # 2.5 MET * 70kg * 0.5hr = 87.5 cal
        ("Walking", "light", 60, 210),   # 3.0 MET * 70kg * 1hr = 210 cal
    ]

    print(f"Test subject: 70kg person\n")

    for activity, intensity, duration, expected in test_cases:
        calories = calculate_calories_burned(activity, intensity, duration, weight_kg)

        print(f"Activity: {activity}")
        print(f"  Intensity: {intensity}")
        print(f"  Duration: {duration} minutes")
        print(f"  Calculated: {calories} calories")
        print(f"  Expected: ~{expected} calories")

        # Check if calculation is within reasonable range (±10%)
        if abs(calories - expected) / expected <= 0.1:
            print(f"  ✓ PASS - Within expected range")
        else:
            print(f"  ✗ FAIL - Outside expected range")
        print()

if __name__ == "__main__":
    with app.app_context():
        test_workout_calculations()