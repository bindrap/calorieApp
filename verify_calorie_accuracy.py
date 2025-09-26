#!/usr/bin/env python3
"""
Verify calorie burn accuracy by comparing with standard references
"""

import os
import sys
sys.path.append('/app')

from app import app, calculate_calories_burned

def verify_calorie_accuracy():
    """Compare our calculations with standard references"""

    print("🔥 CALORIE BURN ACCURACY VERIFICATION")
    print("=" * 60)

    # Standard reference person: 155 lbs (70.3 kg)
    weight_lbs = 155
    weight_kg = weight_lbs / 2.20462

    print(f"Reference Person: {weight_lbs} lbs ({weight_kg:.1f} kg)")
    print()

    # Compare with Harvard Health/Mayo Clinic standards
    activities = [
        {
            'name': 'Jiu Jitsu / Martial Arts',
            'our_intensity': 'high',
            'duration': 60,
            'harvard_cal_per_hour': 670,  # Harvard Health data for 155lb person
            'notes': 'High-intensity martial arts'
        },
        {
            'name': 'Running (6 mph)',
            'our_intensity': 'high',
            'duration': 60,
            'harvard_cal_per_hour': 670,
            'notes': 'Moderate pace running'
        },
        {
            'name': 'Weight Training',
            'our_intensity': 'moderate',
            'duration': 60,
            'harvard_cal_per_hour': 224,
            'notes': 'General weight lifting'
        },
        {
            'name': 'Walking (3.5 mph)',
            'our_intensity': 'light',
            'duration': 60,
            'harvard_cal_per_hour': 298,
            'notes': 'Brisk walking pace'
        },
        {
            'name': 'Yoga',
            'our_intensity': 'light',
            'duration': 60,
            'harvard_cal_per_hour': 149,
            'notes': 'Hatha yoga'
        },
        {
            'name': 'Cycling (moderate)',
            'our_intensity': 'moderate',
            'duration': 60,
            'harvard_cal_per_hour': 480,
            'notes': '12-14 mph pace'
        }
    ]

    print("COMPARISON WITH HARVARD HEALTH STANDARDS:")
    print("-" * 60)

    total_diff = 0
    count = 0

    for activity in activities:
        our_calories = calculate_calories_burned(
            activity['name'],
            activity['our_intensity'],
            activity['duration'],
            weight_kg
        )

        harvard_calories = activity['harvard_cal_per_hour']
        diff_percent = abs(our_calories - harvard_calories) / harvard_calories * 100

        status = "✅ EXCELLENT" if diff_percent < 10 else "⚠️  GOOD" if diff_percent < 20 else "❌ CHECK"

        print(f"{activity['name']:20} | Our: {our_calories:3.0f} | Harvard: {harvard_calories:3.0f} | Diff: {diff_percent:4.1f}% | {status}")
        print(f"{'':20} | {activity['notes']}")
        print()

        total_diff += diff_percent
        count += 1

    avg_diff = total_diff / count
    print(f"AVERAGE DIFFERENCE: {avg_diff:.1f}%")

    if avg_diff < 15:
        print("🎯 RESULT: Your calorie calculations are HIGHLY ACCURATE!")
    elif avg_diff < 25:
        print("✅ RESULT: Your calorie calculations are reasonably accurate.")
    else:
        print("⚠️ RESULT: Consider reviewing MET values for better accuracy.")

    print()
    print("🔍 HOW TO VERIFY YOUR PERSONAL ACCURACY:")
    print("-" * 60)
    print("1. HEART RATE METHOD:")
    print("   - Use: (220 - age) × 0.7 = target heart rate for moderate exercise")
    print("   - If your heart rate matches this during 'moderate' workouts, it's accurate")
    print()
    print("2. FITNESS TRACKER COMPARISON:")
    print("   - Compare with Apple Watch, Fitbit, Garmin, etc.")
    print("   - Look for 10-20% difference (acceptable range)")
    print()
    print("3. PERCEIVED EXERTION SCALE (1-10):")
    print("   - Light intensity: 3-4 (can sing while exercising)")
    print("   - Moderate: 5-6 (can talk but not sing)")
    print("   - High: 7-9 (difficult to talk)")
    print()
    print("4. SWEAT/RECOVERY TEST:")
    print("   - Light: Minimal sweat, easy recovery")
    print("   - Moderate: Light sweat, recovery in 2-5 minutes")
    print("   - High: Heavy sweat, recovery 5+ minutes")

if __name__ == "__main__":
    with app.app_context():
        verify_calorie_accuracy()