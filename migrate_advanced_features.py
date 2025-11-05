#!/usr/bin/env python3
"""
Advanced Features Database Migration Script
Adds all new tables and columns for:
- Unified health timeline
- Multi-item meal recognition
- AI meal suggestions
- Wearable integrations
- AI chat coach
- Gamification (streaks, levels, achievements)
- Mood & energy tracking
- Sleep tracking
- Biometric tracking
"""

import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'calorie_tracker.db')


def migrate_database():
    """Add all new tables and columns for advanced features"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    migrations = []

    print("=" * 80)
    print("ADVANCED FEATURES DATABASE MIGRATION")
    print("=" * 80)
    print(f"Database: {DATABASE_PATH}")
    print(f"Started: {datetime.now()}")
    print()

    # ==================== UNIFIED HEALTH TIMELINE ====================
    print("📊 Creating unified health timeline...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS health_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_type VARCHAR(50) NOT NULL,
            event_subtype VARCHAR(100),
            occurred_at DATETIME NOT NULL,
            logged_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            event_data TEXT,
            calories_net DECIMAL(8,2),
            duration_minutes INTEGER,
            food_entry_id INTEGER,
            workout_entry_id INTEGER,
            sleep_entry_id INTEGER,
            mood_entry_id INTEGER,
            biometric_entry_id INTEGER,
            source VARCHAR(100),
            confidence_score DECIMAL(3,2),
            tags TEXT,
            searchable_text TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (food_entry_id) REFERENCES food_entries(id),
            FOREIGN KEY (workout_entry_id) REFERENCES workout_entries(id),
            FOREIGN KEY (sleep_entry_id) REFERENCES sleep_entries(id),
            FOREIGN KEY (mood_entry_id) REFERENCES mood_entries(id),
            FOREIGN KEY (biometric_entry_id) REFERENCES biometric_entries(id)
        )
    """)

    migrations.append("CREATE INDEX IF NOT EXISTS idx_health_events_user_occurred ON health_events(user_id, occurred_at)")
    migrations.append("CREATE INDEX IF NOT EXISTS idx_health_events_type ON health_events(event_type)")

    # ==================== SLEEP TRACKING ====================
    print("😴 Creating sleep tracking...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS sleep_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sleep_start DATETIME NOT NULL,
            sleep_end DATETIME NOT NULL,
            total_duration_minutes INTEGER NOT NULL,
            deep_sleep_minutes INTEGER,
            light_sleep_minutes INTEGER,
            rem_sleep_minutes INTEGER,
            awake_minutes INTEGER,
            sleep_score INTEGER,
            hrv DECIMAL(6,2),
            resting_hr INTEGER,
            respiratory_rate DECIMAL(4,1),
            quality_rating INTEGER,
            notes TEXT,
            source VARCHAR(50),
            external_id VARCHAR(200),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ==================== MOOD & ENERGY TRACKING ====================
    print("😊 Creating mood & energy tracking...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS mood_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mood_score INTEGER NOT NULL,
            energy_level INTEGER NOT NULL,
            stress_level INTEGER,
            motivation INTEGER,
            emotions TEXT,
            physical_state TEXT,
            notes TEXT,
            factors TEXT,
            logged_at DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ==================== BIOMETRIC TRACKING ====================
    print("📈 Creating biometric tracking...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS biometric_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weight_kg DECIMAL(6,2),
            body_fat_percentage DECIMAL(4,2),
            muscle_mass_kg DECIMAL(6,2),
            bmi DECIMAL(4,2),
            resting_heart_rate INTEGER,
            blood_pressure_systolic INTEGER,
            blood_pressure_diastolic INTEGER,
            vo2_max DECIMAL(5,2),
            waist_cm DECIMAL(5,2),
            chest_cm DECIMAL(5,2),
            hips_cm DECIMAL(5,2),
            thigh_cm DECIMAL(5,2),
            bicep_cm DECIMAL(5,2),
            glucose_mg_dl INTEGER,
            cholesterol_total INTEGER,
            hdl_cholesterol INTEGER,
            ldl_cholesterol INTEGER,
            triglycerides INTEGER,
            measurement_type VARCHAR(50),
            source VARCHAR(50),
            notes TEXT,
            measured_at DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ==================== WEARABLE INTEGRATIONS ====================
    print("⌚ Creating wearable sync tracking...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS wearable_syncs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            platform VARCHAR(50) NOT NULL,
            sync_type VARCHAR(50),
            sync_start_date DATETIME NOT NULL,
            sync_end_date DATETIME NOT NULL,
            records_synced INTEGER DEFAULT 0,
            records_created INTEGER DEFAULT 0,
            records_updated INTEGER DEFAULT 0,
            records_failed INTEGER DEFAULT 0,
            status VARCHAR(20) DEFAULT 'pending',
            error_message TEXT,
            sync_summary TEXT,
            synced_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ==================== AI MEAL SUGGESTIONS ====================
    print("🤖 Creating AI meal suggestions...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS meal_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            suggestion_type VARCHAR(50),
            target_time DATETIME,
            remaining_calories DECIMAL(8,2),
            remaining_protein DECIMAL(6,2),
            remaining_carbs DECIMAL(6,2),
            remaining_fat DECIMAL(6,2),
            suggested_meal VARCHAR(500) NOT NULL,
            reasoning TEXT,
            predicted_calories DECIMAL(8,2),
            predicted_protein DECIMAL(6,2),
            predicted_carbs DECIMAL(6,2),
            predicted_fat DECIMAL(6,2),
            alternatives TEXT,
            viewed BOOLEAN DEFAULT 0,
            accepted BOOLEAN,
            dismissed_reason VARCHAR(100),
            food_entry_id INTEGER,
            suggested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (food_entry_id) REFERENCES food_entries(id)
        )
    """)

    # ==================== AI CHAT COACH ====================
    print("💬 Creating AI chat coach...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            extracted_intent VARCHAR(50),
            extracted_data TEXT,
            action_performed VARCHAR(100),
            related_entry_id INTEGER,
            related_entry_type VARCHAR(50),
            conversation_id VARCHAR(100),
            parent_message_id INTEGER,
            model_used VARCHAR(100),
            tokens_used INTEGER,
            processing_time_ms INTEGER,
            sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (parent_message_id) REFERENCES chat_messages(id)
        )
    """)

    migrations.append("CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation ON chat_messages(conversation_id, sent_at)")

    # ==================== GAMIFICATION - STREAKS ====================
    print("🔥 Creating streak tracking...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS user_streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            streak_type VARCHAR(50) NOT NULL,
            current_streak_days INTEGER DEFAULT 0,
            longest_streak_days INTEGER DEFAULT 0,
            streak_started_at DATE,
            last_activity_date DATE,
            longest_streak_ended_at DATE,
            total_activities INTEGER DEFAULT 0,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    migrations.append("CREATE UNIQUE INDEX IF NOT EXISTS idx_user_streaks_unique ON user_streaks(user_id, streak_type)")

    # ==================== GAMIFICATION - LEVELS & XP ====================
    print("⭐ Creating level & XP system...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS user_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            current_level INTEGER DEFAULT 1,
            current_xp INTEGER DEFAULT 0,
            xp_for_next_level INTEGER DEFAULT 100,
            total_xp_earned INTEGER DEFAULT 0,
            achievement_points INTEGER DEFAULT 0,
            total_food_logs INTEGER DEFAULT 0,
            total_workouts INTEGER DEFAULT 0,
            total_days_active INTEGER DEFAULT 0,
            titles_unlocked TEXT,
            current_title VARCHAR(100),
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ==================== REFERENCE OBJECTS ====================
    print("📏 Creating reference objects for portion estimation...")

    migrations.append("""
        CREATE TABLE IF NOT EXISTS reference_objects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            object_type VARCHAR(50) NOT NULL,
            length_cm DECIMAL(6,2),
            width_cm DECIMAL(6,2),
            height_cm DECIMAL(6,2),
            volume_ml DECIMAL(8,2),
            area_cm2 DECIMAL(8,2),
            calibration_image VARCHAR(255),
            times_used INTEGER DEFAULT 0,
            last_used DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ==================== MULTI-ITEM MEAL TRACKING ====================
    print("🍽️ Adding multi-item meal support to food entries...")

    # Check if food_entries table exists first
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='food_entries'")
    if cursor.fetchone():
        multi_item_fields = [
            ("is_multi_item", "BOOLEAN DEFAULT 0"),
            ("parent_meal_id", "INTEGER"),
            ("item_number", "INTEGER"),
            ("total_items_in_meal", "INTEGER"),
        ]

        for field_name, field_type in multi_item_fields:
            migrations.append(f"ALTER TABLE food_entries ADD COLUMN {field_name} {field_type}")
    else:
        print("   ⏭️  Skipping food_entries modifications (table doesn't exist yet)")

    # ==================== EXECUTE MIGRATIONS ====================
    print("\n🚀 Executing migrations...")
    print("-" * 80)

    success_count = 0
    skip_count = 0
    error_count = 0

    for i, migration in enumerate(migrations, 1):
        try:
            cursor.execute(migration)
            print(f"✅ [{i}/{len(migrations)}] Executed: {migration[:70]}...")
            success_count += 1
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e) or "already exists" in str(e):
                print(f"⏭️  [{i}/{len(migrations)}] Skipped (exists): {migration[:70]}...")
                skip_count += 1
            else:
                print(f"❌ [{i}/{len(migrations)}] Error: {e}")
                print(f"   Migration: {migration[:100]}...")
                error_count += 1
        except Exception as e:
            print(f"❌ [{i}/{len(migrations)}] Error: {e}")
            error_count += 1

    # ==================== SEED INITIAL DATA ====================
    print("\n🌱 Seeding initial data...")
    print("-" * 80)

    # Check if achievements table exists and needs seeding
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='achievements'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM achievements")
        achievement_count = cursor.fetchone()[0]

        if achievement_count == 0:
            print("📦 No achievements found. Seeding will be done by existing migrate_enhanced_workout.py")
        else:
            print(f"✅ {achievement_count} achievements already exist")
    else:
        print("📦 Achievements table doesn't exist yet. Will be created by migrate_enhanced_workout.py")

    # Commit all changes
    conn.commit()
    conn.close()

    # ==================== SUMMARY ====================
    print("\n" + "=" * 80)
    print("MIGRATION SUMMARY")
    print("=" * 80)
    print(f"✅ Successful: {success_count}")
    print(f"⏭️  Skipped:    {skip_count}")
    print(f"❌ Errors:     {error_count}")
    print()
    print("📊 NEW TABLES CREATED:")
    print("   • health_events - Unified timeline for all health data")
    print("   • sleep_entries - Sleep tracking from wearables")
    print("   • mood_entries - Mood and energy tracking")
    print("   • biometric_entries - Body measurements and vitals")
    print("   • wearable_syncs - Wearable device sync history")
    print("   • meal_suggestions - AI meal recommendations")
    print("   • chat_messages - AI coach conversations")
    print("   • user_streaks - Streak tracking for gamification")
    print("   • user_levels - User leveling and XP system")
    print("   • reference_objects - Calibrated objects for portion estimation")
    print()
    print("🆕 NEW FEATURES ENABLED:")
    print("   ✨ Multi-item meal recognition")
    print("   ✨ Smart portion estimation with reference objects")
    print("   ✨ AI meal suggestions based on remaining macros")
    print("   ✨ Adaptive calorie targets (recovery-based)")
    print("   ✨ Wearable device integrations (Apple Health, Fitbit, etc.)")
    print("   ✨ AI chat coach for natural language logging")
    print("   ✨ Gamification (streaks, levels, achievements)")
    print("   ✨ Mood and energy tracking")
    print("   ✨ Sleep quality tracking")
    print("   ✨ Biometric and body composition tracking")
    print()

    if error_count == 0:
        print("✅ Database migration completed successfully!")
    else:
        print(f"⚠️  Database migration completed with {error_count} errors")

    print(f"Finished: {datetime.now()}")
    print("=" * 80)


if __name__ == "__main__":
    migrate_database()
