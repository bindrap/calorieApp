#!/usr/bin/env python3
"""
Database migration script to add AI learning tables
"""

import sqlite3
import os
import sys

def migrate_database():
    """Add UserFeedback table to existing database"""

    # Get database path
    database_path = os.environ.get('DATABASE_PATH', 'calorie_tracker.db')

    if not os.path.exists(database_path):
        print(f"Database file {database_path} does not exist!")
        return False

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Check if user_feedback table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='user_feedback'
        """)

        if cursor.fetchone():
            print("UserFeedback table already exists, skipping migration.")
            conn.close()
            return True

        # Create user_feedback table
        cursor.execute("""
            CREATE TABLE user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                ai_food_name VARCHAR(200),
                ai_weight_grams DECIMAL(8,2),
                ai_calories DECIMAL(8,2),
                ai_protein DECIMAL(8,2),
                ai_carbs DECIMAL(8,2),
                ai_fat DECIMAL(8,2),
                corrected_food_name VARCHAR(200),
                corrected_weight_grams DECIMAL(8,2),
                corrected_calories DECIMAL(8,2),
                corrected_protein DECIMAL(8,2),
                corrected_carbs DECIMAL(8,2),
                corrected_fat DECIMAL(8,2),
                image_features TEXT,
                food_category VARCHAR(100),
                confidence_level DECIMAL(3,2),
                correction_type VARCHAR(50),
                learned_from INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (learned_from) REFERENCES food_entries (id)
            )
        """)

        print("Created user_feedback table successfully!")

        # Commit changes
        conn.commit()
        conn.close()

        print("Database migration completed successfully!")
        return True

    except Exception as e:
        print(f"Error during migration: {e}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)