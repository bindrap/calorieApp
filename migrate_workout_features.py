#!/usr/bin/env python3
"""
Database migration script to add workout tracking features
"""

import sqlite3
import os
import sys

def migrate_database():
    """Add workout tracking features to existing database"""

    # Get database path
    database_path = os.environ.get('DATABASE_PATH', 'calorie_tracker.db')

    if not os.path.exists(database_path):
        print(f"Database file {database_path} does not exist!")
        return False

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        print("Adding workout tracking features...")

        # 1. Add profile fields to user_settings table
        try:
            cursor.execute('ALTER TABLE user_settings ADD COLUMN weight_kg DECIMAL(5,2)')
            print("Added weight_kg column to user_settings")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("weight_kg column already exists")
            else:
                raise

        try:
            cursor.execute('ALTER TABLE user_settings ADD COLUMN height_cm DECIMAL(5,2)')
            print("Added height_cm column to user_settings")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("height_cm column already exists")
            else:
                raise

        try:
            cursor.execute('ALTER TABLE user_settings ADD COLUMN age INTEGER')
            print("Added age column to user_settings")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("age column already exists")
            else:
                raise

        try:
            cursor.execute('ALTER TABLE user_settings ADD COLUMN gender VARCHAR(10)')
            print("Added gender column to user_settings")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("gender column already exists")
            else:
                raise

        # 2. Create workout_entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workout_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_type VARCHAR(100) NOT NULL,
                intensity VARCHAR(20) NOT NULL,
                duration_minutes INTEGER NOT NULL,
                calories_burned DECIMAL(8,2) NOT NULL,
                logged_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("Created workout_entries table")

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