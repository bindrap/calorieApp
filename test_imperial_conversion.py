#!/usr/bin/env python3
"""
Test imperial unit conversions
"""

def test_conversions():
    """Test weight and height conversions"""

    print("Testing Imperial Unit Conversions")
    print("=" * 40)

    # Test weight conversion: lbs to kg
    test_weights = [150, 180, 200, 120]

    print("Weight Conversions (lbs → kg):")
    for lbs in test_weights:
        kg = lbs / 2.20462
        kg_back = kg * 2.20462
        print(f"  {lbs} lbs → {kg:.2f} kg → {kg_back:.1f} lbs")

    print()

    # Test height conversion: feet/inches to cm
    test_heights = [(5, 6), (5, 10), (6, 2), (5, 4)]

    print("Height Conversions (ft'in\" → cm):")
    for feet, inches in test_heights:
        total_inches = (feet * 12) + inches
        cm = total_inches * 2.54

        # Convert back
        total_inches_back = cm / 2.54
        feet_back = int(total_inches_back // 12)
        inches_back = int(total_inches_back % 12)

        print(f"  {feet}' {inches}\" → {cm:.1f} cm → {feet_back}' {inches_back}\"")

    print()

    # Test calorie calculation with converted weight
    print("Calorie Calculation Test:")
    weight_lbs = 170
    weight_kg = weight_lbs / 2.20462

    # Simulate a workout: Jiu Jitsu (10 MET) for 60 minutes
    met_value = 10.0
    duration_hours = 1.0
    calories = met_value * weight_kg * duration_hours

    print(f"  170 lbs person ({weight_kg:.1f} kg)")
    print(f"  Jiu Jitsu (10 MET) for 60 minutes")
    print(f"  Calories burned: {calories:.0f}")

if __name__ == "__main__":
    test_conversions()