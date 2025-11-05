#!/usr/bin/env python3
"""
Database Migration Script for Enhanced Workout Features
Adds all new columns and tables for comprehensive fitness tracking
"""

import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'instance/calorie_tracker.db')

def migrate_database():
    """Add all new columns and tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    migrations = []

    # Add activity-specific fields to workout_entries
    workout_fields = [
        ("distance_km", "DECIMAL(8,2)"),
        ("pace_min_per_km", "DECIMAL(5,2)"),
        ("elevation_gain_m", "DECIMAL(8,2)"),
        ("laps", "INTEGER"),
        ("pool_length_m", "INTEGER"),
        ("stroke_type", "VARCHAR(50)"),
        ("exercises", "TEXT"),
        ("total_sets", "INTEGER"),
        ("total_reps", "INTEGER"),
        ("total_weight_kg", "DECIMAL(8,2)"),
        ("rounds", "INTEGER"),
        ("notes", "TEXT"),
        ("equipment", "VARCHAR(200)"),
        ("location", "VARCHAR(200)"),
        ("template_id", "INTEGER"),
    ]

    for field_name, field_type in workout_fields:
        migrations.append(
            f"ALTER TABLE workout_entries ADD COLUMN {field_name} {field_type}"
        )

    # Create workout_goals table
    migrations.append("""
        CREATE TABLE IF NOT EXISTS workout_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_type VARCHAR(50) NOT NULL,
            target_value DECIMAL(10,2) NOT NULL,
            current_value DECIMAL(10,2) DEFAULT 0,
            period VARCHAR(20) NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            activity_type VARCHAR(100),
            is_completed BOOLEAN DEFAULT 0,
            completed_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create workout_templates table
    migrations.append("""
        CREATE TABLE IF NOT EXISTS workout_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            activity_type VARCHAR(100) NOT NULL,
            intensity VARCHAR(20) NOT NULL,
            default_duration_minutes INTEGER,
            template_data TEXT,
            times_used INTEGER DEFAULT 0,
            last_used DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create achievements table
    migrations.append("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            icon VARCHAR(10),
            category VARCHAR(50),
            criteria_type VARCHAR(50) NOT NULL,
            criteria_value DECIMAL(10,2) NOT NULL,
            points INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create user_achievements table
    migrations.append("""
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_id INTEGER NOT NULL,
            unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            progress_value DECIMAL(10,2),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (achievement_id) REFERENCES achievements(id)
        )
    """)

    # Create personal_records table
    migrations.append("""
        CREATE TABLE IF NOT EXISTS personal_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            activity_type VARCHAR(100) NOT NULL,
            record_type VARCHAR(50) NOT NULL,
            value DECIMAL(10,2) NOT NULL,
            unit VARCHAR(20),
            workout_entry_id INTEGER,
            achieved_at DATETIME NOT NULL,
            previous_value DECIMAL(10,2),
            improvement DECIMAL(10,2),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (workout_entry_id) REFERENCES workout_entries(id)
        )
    """)

    # Execute migrations
    for migration in migrations:
        try:
            cursor.execute(migration)
            print(f"✅ Executed: {migration[:60]}...")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e) or "already exists" in str(e):
                print(f"⏭️  Skipped (already exists): {migration[:60]}...")
            else:
                print(f"❌ Error: {e}")
                print(f"   Migration: {migration[:100]}...")

    # Seed default achievements
    seed_achievements(cursor)

    conn.commit()
    conn.close()
    print("\n✅ Database migration completed successfully!")

def seed_achievements(cursor):
    """Seed default achievements"""
    achievements = [
        ("First Workout", "Complete your first workout", "🎯", "milestone", "workout_count", 1, 10),
        ("5 Workouts", "Complete 5 workouts", "💪", "milestone", "workout_count", 5, 50),
        ("10 Workouts", "Complete 10 workouts", "🔥", "milestone", "workout_count", 10, 100),
        ("25 Workouts", "Complete 25 workouts", "⭐", "milestone", "workout_count", 25, 250),
        ("50 Workouts", "Complete 50 workouts", "🏆", "milestone", "workout_count", 50, 500),
        ("100 Workouts", "Century Club", "👑", "milestone", "workout_count", 100, 1000),
        ("1000 Calories Burned", "Burn 1000 calories total", "🔥", "volume", "total_calories_burned", 1000, 100),
        ("5000 Calories Burned", "Burn 5000 calories total", "🔥🔥", "volume", "total_calories_burned", 5000, 500),
        ("10000 Calories Burned", "Burn 10,000 calories total", "🔥🔥🔥", "volume", "total_calories_burned", 10000, 1000),
        ("7 Day Streak", "Workout 7 days in a row", "📅", "streak", "streak_days", 7, 200),
        ("30 Day Streak", "Workout 30 days in a row", "🗓️", "streak", "streak_days", 30, 1000),
        ("Marathon Runner", "Run 42.2 km total", "🏃", "volume", "total_distance_running", 42.2, 500),
        ("Swimmer", "Swim 1000 meters", "🏊", "volume", "total_distance_swimming", 1, 200),
        ("Early Bird", "Complete a workout before 7 AM", "🌅", "special", "early_workout", 1, 50),
        ("Night Owl", "Complete a workout after 9 PM", "🌙", "special", "late_workout", 1, 50),
    ]

    for ach in achievements:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO achievements
                (name, description, icon, category, criteria_type, criteria_value, points)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ach)
        except Exception as e:
            print(f"Error seeding achievement {ach[0]}: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("ENHANCED WORKOUT FEATURES DATABASE MIGRATION")
    print("=" * 80)
    migrate_database()
