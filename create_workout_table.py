#!/usr/bin/env python3
"""
Migration script to create workout_entries table and related tables
"""

import sqlite3
import os
import sys

def migrate_database():
    """Create workout_entries table with all columns"""

    db_path = os.environ.get('DATABASE_PATH', 'instance/calorie_tracker.db')

    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🔍 Checking if workout_entries table exists...")

        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workout_entries'")
        table_exists = cursor.fetchone()

        if table_exists:
            print("   ✅ workout_entries table already exists")

            # Check which columns exist
            cursor.execute("PRAGMA table_info(workout_entries);")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"   Found {len(columns)} columns")

            # Add missing columns
            migrations_needed = []
            new_columns = {
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

            for col_name, col_type in new_columns.items():
                if col_name not in columns:
                    migrations_needed.append(f"ALTER TABLE workout_entries ADD COLUMN {col_name} {col_type}")
                    print(f"   ➕ Will add: {col_name}")

            if migrations_needed:
                print(f"\n🔧 Running {len(migrations_needed)} migrations...")
                for migration in migrations_needed:
                    cursor.execute(migration)
                    print(f"   ✅ {migration}")
                conn.commit()
                print("\n✅ Columns added successfully!")
            else:
                print("\n✅ All columns already exist")

        else:
            print("   ⚠️  workout_entries table does not exist, creating it...")

            # Create the full table
            cursor.execute("""
                CREATE TABLE workout_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity_type VARCHAR(100) NOT NULL,
                    intensity VARCHAR(20) NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    exertion_rating INTEGER,
                    calories_burned DECIMAL(8,2) NOT NULL,

                    -- Activity-specific fields
                    distance_km DECIMAL(8,2),
                    pace_min_per_km DECIMAL(5,2),
                    elevation_gain_m DECIMAL(8,2),

                    -- Swimming specific
                    laps INTEGER,
                    pool_length_m INTEGER,
                    stroke_type VARCHAR(50),

                    -- Strength training specific
                    exercises TEXT,
                    total_sets INTEGER,
                    total_reps INTEGER,
                    total_weight_kg DECIMAL(8,2),

                    -- Combat sports specific
                    rounds INTEGER,

                    -- Miscellaneous
                    notes TEXT,
                    equipment VARCHAR(200),
                    location VARCHAR(200),
                    template_id INTEGER,

                    -- Timestamps
                    logged_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (template_id) REFERENCES workout_templates (id)
                )
            """)

            print("   ✅ Created workout_entries table with all columns")
            conn.commit()

        conn.close()
        print("\n✅ Migration completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
