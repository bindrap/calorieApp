#!/usr/bin/env python3
"""
Migration script to add user_description and barcode columns to food_entries table
"""

import sqlite3
import os
import sys

def migrate_database():
    """Add missing columns to food_entries table"""

    db_path = os.environ.get('DATABASE_PATH', 'instance/calorie_tracker.db')

    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🔍 Checking current schema...")

        # Get current columns
        cursor.execute("PRAGMA table_info(food_entries);")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"   Found {len(columns)} columns in food_entries")

        migrations_needed = []

        # Check and add user_description
        if 'user_description' not in columns:
            migrations_needed.append(
                "ALTER TABLE food_entries ADD COLUMN user_description TEXT"
            )
            print("   ➕ Will add: user_description")
        else:
            print("   ✅ user_description already exists")

        # Check and add barcode_upc
        if 'barcode_upc' not in columns:
            migrations_needed.append(
                "ALTER TABLE food_entries ADD COLUMN barcode_upc VARCHAR(50)"
            )
            print("   ➕ Will add: barcode_upc")
        else:
            print("   ✅ barcode_upc already exists")

        # Check and add barcode_source
        if 'barcode_source' not in columns:
            migrations_needed.append(
                "ALTER TABLE food_entries ADD COLUMN barcode_source VARCHAR(100)"
            )
            print("   ➕ Will add: barcode_source")
        else:
            print("   ✅ barcode_source already exists")

        # Execute migrations
        if migrations_needed:
            print(f"\n🔧 Running {len(migrations_needed)} migrations...")
            for migration in migrations_needed:
                cursor.execute(migration)
                print(f"   ✅ {migration}")

            conn.commit()
            print("\n✅ Migration completed successfully!")
        else:
            print("\n✅ All columns already exist, no migration needed")

        conn.close()
        return True

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
