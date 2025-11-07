#!/usr/bin/env python3
"""
Migration to add user_description column to analysis_logs table
"""

import sqlite3
import os
import sys

def migrate_database():
    """Add user_description column to analysis_logs table"""

    db_path = os.environ.get('DATABASE_PATH', 'instance/calorie_tracker.db')

    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🔍 Checking analysis_logs table...")

        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_logs'")
        if not cursor.fetchone():
            print("   ⚠️  analysis_logs table doesn't exist yet")
            conn.close()
            return True  # Not an error, just not created yet

        # Check if user_description column exists
        cursor.execute("PRAGMA table_info(analysis_logs)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'user_description' in columns:
            print("   ✅ user_description column already exists")
        else:
            print("   ➕ Adding user_description column...")
            cursor.execute("ALTER TABLE analysis_logs ADD COLUMN user_description TEXT")
            conn.commit()
            print("   ✅ Added user_description column")

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
