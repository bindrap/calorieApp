#!/usr/bin/env python3
"""
Comprehensive Calorie Tracking Accuracy Test
Tests food recognition, calorie calculation, and workout tracking
"""

import sys
from enhanced_food_database import calculate_accurate_calories, get_enhanced_nutrition_data
from activity_database import get_met_value, ACTIVITY_DATABASE

print("=" * 80)
print("CALORIE TRACKING ACCURACY TEST")
print("=" * 80)

# Test data with known calorie values
test_foods = [
    # (food_name, weight_grams, expected_calories, description)
    ("Big Mac", None, 570, "McDonald's Big Mac (typical serving)"),
    ("Big Mac", 222, 570, "McDonald's Big Mac (222g)"),
    ("Grilled chicken breast", 200, 330, "200g grilled chicken breast"),
    ("Banana", 118, 105, "Medium banana (118g)"),
    ("Greek yogurt", 200, 130, "200g Greek yogurt (2%)"),
    ("Avocado", 150, 240, "Medium avocado (150g)"),
    ("White rice", 100, 130, "100g cooked white rice"),
    ("Broccoli", 100, 34, "100g raw broccoli"),
    ("Salmon", 180, 360, "180g wild salmon"),
    ("Whole wheat bread", 30, 80, "1 slice (30g)"),
    ("Peanut butter", 32, 190, "2 tbsp (32g)"),
    ("Eggs", 150, 210, "3 large eggs (50g each)"),
    ("Apple", 182, 95, "Medium apple (182g)"),
    ("Oatmeal", 40, 150, "40g dry oats"),
    ("Almonds", 28, 164, "1oz almonds (28g)"),
]

print("\n📊 TESTING FOOD CALORIE CALCULATIONS")
print("=" * 80)

passed_tests = 0
failed_tests = 0
total_error_percentage = 0

for food_name, weight_grams, expected_calories, description in test_foods:
    print(f"\n🍽️  {description}")
    print(f"   Testing: {food_name} ({weight_grams or 'auto'}g)")

    try:
        result = calculate_accurate_calories(food_name, weight_grams)

        if result:
            calculated_calories = result['total_calories']
            protein = result['protein']
            carbs = result['carbs']
            fat = result['fat']

            # Calculate error percentage
            error_percent = abs(calculated_calories - expected_calories) / expected_calories * 100
            total_error_percentage += error_percent

            # Pass if within 10% margin
            if error_percent <= 10:
                status = "✅ PASS"
                passed_tests += 1
            else:
                status = "❌ FAIL"
                failed_tests += 1

            print(f"   Expected:   {expected_calories} cal")
            print(f"   Calculated: {calculated_calories} cal")
            print(f"   Macros: P={protein}g, C={carbs}g, F={fat}g")
            print(f"   Error: {error_percent:.1f}%")
            print(f"   {status}")
        else:
            print(f"   ❌ FAIL - No calculation result")
            failed_tests += 1

    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        failed_tests += 1

# Test workout MET calculations
print("\n\n💪 TESTING WORKOUT CALORIE CALCULATIONS")
print("=" * 80)

test_workouts = [
    # (activity, duration_min, weight_kg, expected_cal_range, description)
    ("Running", 30, 70, (250, 350), "30 min running (moderate pace)"),
    ("Jiu-Jitsu", 60, 70, (500, 650), "60 min Brazilian Jiu-Jitsu"),
    ("Walking", 30, 70, (100, 150), "30 min walking"),
    ("Cycling", 45, 70, (300, 450), "45 min cycling (moderate)"),
    ("Swimming", 30, 70, (200, 300), "30 min swimming"),
    ("Weightlifting", 45, 70, (150, 250), "45 min weightlifting"),
    ("Yoga", 60, 70, (150, 250), "60 min yoga"),
    ("Boxing", 30, 70, (250, 350), "30 min boxing"),
]

workout_passed = 0
workout_failed = 0

for activity, duration_min, weight_kg, expected_range, description in test_workouts:
    print(f"\n🏃 {description}")
    print(f"   Testing: {activity} for {duration_min} min at {weight_kg}kg")

    try:
        # Get MET value
        met = get_met_value(activity, "moderate")

        if met:
            # Calculate calories: MET * weight_kg * duration_hours
            duration_hours = duration_min / 60.0
            calculated_calories = met * weight_kg * duration_hours

            min_expected, max_expected = expected_range

            # Check if within expected range
            if min_expected <= calculated_calories <= max_expected:
                status = "✅ PASS"
                workout_passed += 1
            else:
                status = "❌ FAIL"
                workout_failed += 1

            print(f"   MET value: {met}")
            print(f"   Expected range: {min_expected}-{max_expected} cal")
            print(f"   Calculated: {calculated_calories:.0f} cal")
            print(f"   {status}")
        else:
            print(f"   ❌ FAIL - No MET value found")
            workout_failed += 1

    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        workout_failed += 1

# Test specific enhanced database entries
print("\n\n🔍 TESTING ENHANCED FOOD DATABASE")
print("=" * 80)

enhanced_foods = [
    "Big Mac",
    "Grilled chicken breast",
    "Greek yogurt",
    "Banana",
    "Avocado",
]

for food in enhanced_foods:
    data = get_enhanced_nutrition_data(food)
    if data:
        print(f"\n✅ {food}:")
        print(f"   Per 100g: {data.get('calories_per_100g')}cal, "
              f"P={data.get('protein_per_100g')}g, "
              f"C={data.get('carbs_per_100g')}g, "
              f"F={data.get('fat_per_100g')}g")
        if 'typical_calories' in data:
            print(f"   Typical serving: {data['typical_weight']}g = {data['typical_calories']}cal")
    else:
        print(f"\n❌ {food}: Not in enhanced database")

# Summary Report
print("\n\n" + "=" * 80)
print("📋 TEST SUMMARY REPORT")
print("=" * 80)

total_food_tests = passed_tests + failed_tests
food_pass_rate = (passed_tests / total_food_tests * 100) if total_food_tests > 0 else 0
avg_error = total_error_percentage / total_food_tests if total_food_tests > 0 else 0

print(f"\n🍽️  FOOD CALORIE ACCURACY:")
print(f"   Total tests: {total_food_tests}")
print(f"   Passed: {passed_tests} ✅")
print(f"   Failed: {failed_tests} ❌")
print(f"   Pass rate: {food_pass_rate:.1f}%")
print(f"   Average error: {avg_error:.1f}%")

total_workout_tests = workout_passed + workout_failed
workout_pass_rate = (workout_passed / total_workout_tests * 100) if total_workout_tests > 0 else 0

print(f"\n💪 WORKOUT CALORIE ACCURACY:")
print(f"   Total tests: {total_workout_tests}")
print(f"   Passed: {workout_passed} ✅")
print(f"   Failed: {workout_failed} ❌")
print(f"   Pass rate: {workout_pass_rate:.1f}%")

overall_pass_rate = ((passed_tests + workout_passed) / (total_food_tests + total_workout_tests) * 100)

print(f"\n🎯 OVERALL ACCURACY:")
print(f"   Total tests: {total_food_tests + total_workout_tests}")
print(f"   Passed: {passed_tests + workout_passed} ✅")
print(f"   Failed: {failed_tests + workout_failed} ❌")
print(f"   Overall pass rate: {overall_pass_rate:.1f}%")

print("\n" + "=" * 80)

# Grade the system
if overall_pass_rate >= 90:
    grade = "A - Excellent accuracy! ⭐⭐⭐⭐⭐"
elif overall_pass_rate >= 80:
    grade = "B - Good accuracy ⭐⭐⭐⭐"
elif overall_pass_rate >= 70:
    grade = "C - Acceptable accuracy ⭐⭐⭐"
elif overall_pass_rate >= 60:
    grade = "D - Needs improvement ⭐⭐"
else:
    grade = "F - Significant issues ⭐"

print(f"📊 GRADE: {grade}")
print("=" * 80)

# Exit with appropriate code
sys.exit(0 if overall_pass_rate >= 80 else 1)
