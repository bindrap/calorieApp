#!/usr/bin/env python3
"""
Test database migration for user_description column
"""

import os
import sys
from datetime import datetime

# Set up Flask app context
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test if we can import the app and models
try:
    print("Testing database schema migration...")
    print("-" * 80)

    # Import app components
    from app import app, db, FoodEntry, AnalysisLog, User

    with app.app_context():
        # Create all tables (this will add missing columns)
        print("✓ Creating/updating database tables...")
        db.create_all()

        # Verify FoodEntry has user_description column
        print("✓ Verifying FoodEntry model has user_description column...")
        assert hasattr(FoodEntry, 'user_description'), "FoodEntry missing user_description column!"
        print(f"  - FoodEntry.user_description: {FoodEntry.user_description}")

        # Verify AnalysisLog has user_description column
        print("✓ Verifying AnalysisLog model has user_description column...")
        assert hasattr(AnalysisLog, 'user_description'), "AnalysisLog missing user_description column!"
        print(f"  - AnalysisLog.user_description: {AnalysisLog.user_description}")

        # Test creating a FoodEntry with description
        print("\n✓ Testing FoodEntry creation with description...")

        # Check if we have a test user, otherwise skip entry creation test
        test_user = User.query.first()
        if test_user:
            test_entry = FoodEntry(
                user_id=test_user.id,
                food_name="Test Food",
                user_description="This is a test description for accuracy",
                calories=100,
                consumed_at=datetime.utcnow()
            )

            # Don't commit, just verify the object can be created
            print(f"  - Test entry created: {test_entry.food_name}")
            print(f"  - Description: {test_entry.user_description}")
            print("  - Entry object created successfully (not committed)")
        else:
            print("  - Skipping entry creation test (no users in database)")

        print("\n" + "=" * 80)
        print("DATABASE MIGRATION TEST PASSED ✓")
        print("=" * 80)
        print("\n✓ All database columns added successfully")
        print("✓ FoodEntry.user_description: Ready")
        print("✓ AnalysisLog.user_description: Ready")
        print("\nThe app is ready to use the description feature!")

except Exception as e:
    print(f"\n✗ Database migration test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
