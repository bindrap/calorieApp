#!/usr/bin/env python3
"""
Quick fix script to add missing columns to your local database
Run this in your local environment to fix the schema
"""

import sqlite3
import os

def fix_database():
    """Add all missing columns"""

    # Use the same path as app.py
    db_path = os.environ.get('DATABASE_PATH', 'instance/calorie_tracker.db')

    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print(f"   Current directory: {os.getcwd()}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print(f"🔍 Fixing database at: {db_path}")
        print(f"   File size: {os.path.getsize(db_path)} bytes")

        # Check workout_entries table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workout_entries'")
        if not cursor.fetchone():
            print("❌ workout_entries table doesn't exist!")
            print("   Creating table...")
            cursor.execute("""
                CREATE TABLE workout_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity_type VARCHAR(100) NOT NULL,
                    intensity VARCHAR(20) NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    exertion_rating INTEGER,
                    calories_burned DECIMAL(8,2) NOT NULL,
                    distance_km DECIMAL(8,2),
                    pace_min_per_km DECIMAL(5,2),
                    elevation_gain_m DECIMAL(8,2),
                    laps INTEGER,
                    pool_length_m INTEGER,
                    stroke_type VARCHAR(50),
                    exercises TEXT,
                    total_sets INTEGER,
                    total_reps INTEGER,
                    total_weight_kg DECIMAL(8,2),
                    rounds INTEGER,
                    notes TEXT,
                    equipment VARCHAR(200),
                    location VARCHAR(200),
                    template_id INTEGER,
                    logged_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            print("   ✅ Created workout_entries table with all columns")
        else:
            # Check which columns exist
            cursor.execute("PRAGMA table_info(workout_entries)")
            columns = [col[1] for col in cursor.fetchall()]

            print(f"   Found workout_entries table with {len(columns)} columns")

            # Add missing columns
            needed_columns = {
                'distance_km': 'DECIMAL(8,2)',
                'pace_min_per_km': 'DECIMAL(5,2)',
                'elevation_gain_m': 'DECIMAL(8,2)',
                'laps': 'INTEGER',
                'pool_length_m': 'INTEGER',
                'stroke_type': 'VARCHAR(50)',
                'exercises': 'TEXT',
                'total_sets': 'INTEGER',
                'total_reps': 'INTEGER',
                'total_weight_kg': 'DECIMAL(8,2)',
                'rounds': 'INTEGER',
                'notes': 'TEXT',
                'equipment': 'VARCHAR(200)',
                'location': 'VARCHAR(200)',
                'template_id': 'INTEGER'
            }

            added = 0
            for col_name, col_type in needed_columns.items():
                if col_name not in columns:
                    cursor.execute(f"ALTER TABLE workout_entries ADD COLUMN {col_name} {col_type}")
                    print(f"   ✅ Added: {col_name}")
                    added += 1

            if added == 0:
                print("   ✅ All columns already exist!")
            else:
                print(f"   ✅ Added {added} missing columns")

        # Check food_entries for user_description
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='food_entries'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(food_entries)")
            columns = [col[1] for col in cursor.fetchall()]

            food_columns = {
                'user_description': 'TEXT',
                'barcode_upc': 'VARCHAR(50)',
                'barcode_source': 'VARCHAR(100)'
            }

            for col_name, col_type in food_columns.items():
                if col_name not in columns:
                    cursor.execute(f"ALTER TABLE food_entries ADD COLUMN {col_name} {col_type}")
                    print(f"   ✅ Added to food_entries: {col_name}")

        conn.commit()
        conn.close()

        print("\n✅ Database fixed successfully!")
        print("   You can now run the app: python3 app.py")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = fix_database()
    sys.exit(0 if success else 1)
