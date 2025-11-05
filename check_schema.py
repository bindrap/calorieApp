#!/usr/bin/env python3
"""Check database schema"""
import sqlite3
import os

db_path = 'instance/calorie_tracker.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n=== FOOD_ENTRIES COLUMNS ===")
    cursor.execute("PRAGMA table_info(food_entries);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"{col[1]} ({col[2]})")

    print("\n=== ALL TABLES ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

    conn.close()
else:
    print(f"Database not found at {db_path}")
