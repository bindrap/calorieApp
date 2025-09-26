#!/usr/bin/env python3
"""Database migration to add background settings to user_settings table"""

import sqlite3
import os

def migrate_backgrounds():
    """Add background settings columns to user_settings table"""
    # Database path
    db_path = os.path.join('instance', 'calorie_tracker.db')

    if not os.path.exists(db_path):
        print("Database not found. Creating new database with background fields.")
        return

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(user_settings)")
        columns = [row[1] for row in cursor.fetchall()]

        # Add background_type column if it doesn't exist
        if 'background_type' not in columns:
            cursor.execute("""
                ALTER TABLE user_settings
                ADD COLUMN background_type VARCHAR(20) DEFAULT 'default'
            """)
            print("Added background_type column")
        else:
            print("background_type column already exists")

        # Add background_filename column if it doesn't exist
        if 'background_filename' not in columns:
            cursor.execute("""
                ALTER TABLE user_settings
                ADD COLUMN background_filename VARCHAR(255)
            """)
            print("Added background_filename column")
        else:
            print("background_filename column already exists")

        # Commit changes
        conn.commit()
        print("Background settings migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()

    finally:
        conn.close()

if __name__ == "__main__":
    migrate_backgrounds()