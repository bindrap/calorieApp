#!/usr/bin/env python3
"""
Check AI learning system status
"""

import sqlite3
import os

def check_learning_system():
    """Check learning system database records"""

    database_path = os.environ.get('DATABASE_PATH', '/app/instance/calorie_tracker.db')

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Check user feedback records
        cursor.execute("SELECT COUNT(*) FROM user_feedback")
        feedback_count = cursor.fetchone()[0]
        print(f"User feedback records: {feedback_count}")

        if feedback_count > 0:
            cursor.execute("""
                SELECT ai_food_name, corrected_food_name, ai_calories, corrected_calories,
                       food_category, correction_type, created_at
                FROM user_feedback
                ORDER BY created_at DESC
                LIMIT 5
            """)

            records = cursor.fetchall()
            print("\nRecent feedback records:")
            for record in records:
                print(f"- {record[0]} -> {record[1]}")
                print(f"  Calories: {record[2]} -> {record[3]}")
                print(f"  Category: {record[4]}, Type: {record[5]}")
                print(f"  Date: {record[6]}\n")

        # Check food entries with corrections
        cursor.execute("""
            SELECT food_name, original_ai_food_name, calories, user_corrected, created_at
            FROM food_entries
            WHERE user_corrected = 1
            ORDER BY created_at DESC
            LIMIT 5
        """)

        corrected_entries = cursor.fetchall()
        print(f"Corrected food entries: {len(corrected_entries)}")

        for entry in corrected_entries:
            print(f"- {entry[1]} -> {entry[0]}")
            print(f"  Calories: {entry[2]}, Corrected: {entry[3]}")
            print(f"  Date: {entry[4]}\n")

        conn.close()

    except Exception as e:
        print(f"Error checking learning system: {e}")

if __name__ == "__main__":
    check_learning_system()