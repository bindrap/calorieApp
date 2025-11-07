#!/usr/bin/env python3
"""
Unified Health Timeline Models
Comprehensive event system for tracking all health-related activities
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# This will be imported from app.py
# from app import db

class HealthEvent(db.Model):
    """
    Polymorphic base model for unified health timeline
    All health events (food, workouts, sleep, mood, etc.) can be queried through this
    """
    __tablename__ = 'health_events'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Event classification
    event_type = db.Column(db.String(50), nullable=False, index=True)  # 'food', 'workout', 'sleep', 'mood', 'biometric', 'wearable_sync'
    event_subtype = db.Column(db.String(100))  # More specific classification

    # Timing
    occurred_at = db.Column(db.DateTime, nullable=False, index=True)  # When the event actually happened
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)  # When it was logged

    # Core data (JSON for flexibility)
    event_data = db.Column(db.Text)  # JSON containing event-specific data

    # Aggregated metrics (for quick queries)
    calories_net = db.Column(db.Numeric(8,2))  # Positive for food, negative for exercise
    duration_minutes = db.Column(db.Integer)

    # References to specific entries
    food_entry_id = db.Column(db.Integer, db.ForeignKey('food_entries.id'))
    workout_entry_id = db.Column(db.Integer, db.ForeignKey('workout_entries.id'))
    sleep_entry_id = db.Column(db.Integer, db.ForeignKey('sleep_entries.id'))
    mood_entry_id = db.Column(db.Integer, db.ForeignKey('mood_entries.id'))
    biometric_entry_id = db.Column(db.Integer, db.ForeignKey('biometric_entries.id'))

    # Metadata
    source = db.Column(db.String(100))  # 'manual', 'ai', 'barcode', 'wearable', 'api_sync'
    confidence_score = db.Column(db.Numeric(3,2))

    # Tags and search
    tags = db.Column(db.Text)  # JSON array of tags
    searchable_text = db.Column(db.Text)  # Full-text search field

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    food_entry = db.relationship('FoodEntry', foreign_keys=[food_entry_id])
    workout_entry = db.relationship('WorkoutEntry', foreign_keys=[workout_entry_id])

    def __repr__(self):
        return f'<HealthEvent {self.event_type} at {self.occurred_at}>'


class SleepEntry(db.Model):
    """Track sleep data from wearables or manual entry"""
    __tablename__ = 'sleep_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Sleep timing
    sleep_start = db.Column(db.DateTime, nullable=False)
    sleep_end = db.Column(db.DateTime, nullable=False)
    total_duration_minutes = db.Column(db.Integer, nullable=False)

    # Sleep stages (from wearables)
    deep_sleep_minutes = db.Column(db.Integer)
    light_sleep_minutes = db.Column(db.Integer)
    rem_sleep_minutes = db.Column(db.Integer)
    awake_minutes = db.Column(db.Integer)

    # Sleep quality metrics
    sleep_score = db.Column(db.Integer)  # 0-100 score
    hrv = db.Column(db.Numeric(6,2))  # Heart rate variability
    resting_hr = db.Column(db.Integer)  # Resting heart rate
    respiratory_rate = db.Column(db.Numeric(4,1))

    # User-reported quality
    quality_rating = db.Column(db.Integer)  # 1-5 stars
    notes = db.Column(db.Text)

    # Data source
    source = db.Column(db.String(50))  # 'manual', 'apple_health', 'google_fit', 'whoop', 'oura'
    external_id = db.Column(db.String(200))  # ID from external system

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to health timeline
    health_event = db.relationship('HealthEvent', backref='sleep_entry', uselist=False)


class MoodEntry(db.Model):
    """Track mood, energy, and subjective wellness"""
    __tablename__ = 'mood_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Mood metrics (1-10 scales)
    mood_score = db.Column(db.Integer, nullable=False)  # 1=terrible, 10=excellent
    energy_level = db.Column(db.Integer, nullable=False)  # 1=exhausted, 10=energized
    stress_level = db.Column(db.Integer)  # 1=calm, 10=very stressed
    motivation = db.Column(db.Integer)  # 1=unmotivated, 10=highly motivated

    # Emotional tags
    emotions = db.Column(db.Text)  # JSON array: ['happy', 'anxious', 'focused', etc.]

    # Physical feelings
    physical_state = db.Column(db.Text)  # JSON: {'soreness': 6, 'hunger': 4, 'pain': 2}

    # Context
    notes = db.Column(db.Text)
    factors = db.Column(db.Text)  # JSON: ['poor_sleep', 'stressful_work', 'good_workout']

    # Timing
    logged_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to health timeline
    health_event = db.relationship('HealthEvent', backref='mood_entry', uselist=False)


class BiometricEntry(db.Model):
    """Track biometric measurements (weight, body fat, heart rate, etc.)"""
    __tablename__ = 'biometric_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Body metrics
    weight_kg = db.Column(db.Numeric(6,2))
    body_fat_percentage = db.Column(db.Numeric(4,2))
    muscle_mass_kg = db.Column(db.Numeric(6,2))
    bmi = db.Column(db.Numeric(4,2))

    # Cardiovascular
    resting_heart_rate = db.Column(db.Integer)
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    vo2_max = db.Column(db.Numeric(5,2))

    # Body measurements
    waist_cm = db.Column(db.Numeric(5,2))
    chest_cm = db.Column(db.Numeric(5,2))
    hips_cm = db.Column(db.Numeric(5,2))
    thigh_cm = db.Column(db.Numeric(5,2))
    bicep_cm = db.Column(db.Numeric(5,2))

    # Blood work (optional)
    glucose_mg_dl = db.Column(db.Integer)
    cholesterol_total = db.Column(db.Integer)
    hdl_cholesterol = db.Column(db.Integer)
    ldl_cholesterol = db.Column(db.Integer)
    triglycerides = db.Column(db.Integer)

    # Metadata
    measurement_type = db.Column(db.String(50))  # 'weight', 'body_composition', 'blood_pressure', 'blood_work'
    source = db.Column(db.String(50))  # 'manual', 'smart_scale', 'apple_health', etc.
    notes = db.Column(db.Text)

    measured_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to health timeline
    health_event = db.relationship('HealthEvent', backref='biometric_entry', uselist=False)


class WearableSync(db.Model):
    """Track synchronization with wearable devices and health apps"""
    __tablename__ = 'wearable_syncs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Sync details
    platform = db.Column(db.String(50), nullable=False)  # 'apple_health', 'google_fit', 'fitbit', 'garmin', 'whoop', 'oura'
    sync_type = db.Column(db.String(50))  # 'steps', 'heart_rate', 'sleep', 'workouts', 'full'

    # Sync window
    sync_start_date = db.Column(db.DateTime, nullable=False)
    sync_end_date = db.Column(db.DateTime, nullable=False)

    # Results
    records_synced = db.Column(db.Integer, default=0)
    records_created = db.Column(db.Integer, default=0)
    records_updated = db.Column(db.Integer, default=0)
    records_failed = db.Column(db.Integer, default=0)

    # Status
    status = db.Column(db.String(20), default='pending')  # 'pending', 'in_progress', 'completed', 'failed'
    error_message = db.Column(db.Text)

    # Synced data summary (JSON)
    sync_summary = db.Column(db.Text)  # JSON: total steps, calories, activities, etc.

    synced_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MealSuggestion(db.Model):
    """AI-generated meal suggestions to hit macro targets"""
    __tablename__ = 'meal_suggestions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Suggestion context
    suggestion_type = db.Column(db.String(50))  # 'breakfast', 'lunch', 'dinner', 'snack', 'pre_workout', 'post_workout'
    target_time = db.Column(db.DateTime)  # Suggested meal time

    # Current macro status (what user needs to hit targets)
    remaining_calories = db.Column(db.Numeric(8,2))
    remaining_protein = db.Column(db.Numeric(6,2))
    remaining_carbs = db.Column(db.Numeric(6,2))
    remaining_fat = db.Column(db.Numeric(6,2))

    # AI suggestion
    suggested_meal = db.Column(db.String(500), nullable=False)  # e.g., "Grilled chicken breast with rice and vegetables"
    reasoning = db.Column(db.Text)  # Why this was suggested

    # Predicted nutrition
    predicted_calories = db.Column(db.Numeric(8,2))
    predicted_protein = db.Column(db.Numeric(6,2))
    predicted_carbs = db.Column(db.Numeric(6,2))
    predicted_fat = db.Column(db.Numeric(6,2))

    # Alternative suggestions
    alternatives = db.Column(db.Text)  # JSON array of alternative meals

    # User interaction
    viewed = db.Column(db.Boolean, default=False)
    accepted = db.Column(db.Boolean)
    dismissed_reason = db.Column(db.String(100))

    # If accepted, link to the actual food entry
    food_entry_id = db.Column(db.Integer, db.ForeignKey('food_entries.id'))

    suggested_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatMessage(db.Model):
    """AI coach chat interactions for conversational logging and advice"""
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Message details
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)

    # Structured data extraction (if user logs food/workout via chat)
    extracted_intent = db.Column(db.String(50))  # 'log_food', 'log_workout', 'ask_question', 'get_advice'
    extracted_data = db.Column(db.Text)  # JSON containing parsed information

    # Action taken
    action_performed = db.Column(db.String(100))  # 'created_food_entry', 'created_workout', 'provided_advice'
    related_entry_id = db.Column(db.Integer)  # ID of created food/workout entry
    related_entry_type = db.Column(db.String(50))  # 'food_entry', 'workout_entry'

    # Context
    conversation_id = db.Column(db.String(100))  # Group related messages
    parent_message_id = db.Column(db.Integer, db.ForeignKey('chat_messages.id'))

    # AI metadata
    model_used = db.Column(db.String(100))
    tokens_used = db.Column(db.Integer)
    processing_time_ms = db.Column(db.Integer)

    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserStreak(db.Model):
    """Track user streaks for gamification"""
    __tablename__ = 'user_streaks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Streak type
    streak_type = db.Column(db.String(50), nullable=False)  # 'food_logging', 'workout', 'goal_hitting'

    # Current streak
    current_streak_days = db.Column(db.Integer, default=0)
    longest_streak_days = db.Column(db.Integer, default=0)

    # Dates
    streak_started_at = db.Column(db.Date)
    last_activity_date = db.Column(db.Date)
    longest_streak_ended_at = db.Column(db.Date)

    # Stats
    total_activities = db.Column(db.Integer, default=0)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserLevel(db.Model):
    """Gamification: User leveling system"""
    __tablename__ = 'user_levels'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Level and XP
    current_level = db.Column(db.Integer, default=1)
    current_xp = db.Column(db.Integer, default=0)
    xp_for_next_level = db.Column(db.Integer, default=100)
    total_xp_earned = db.Column(db.Integer, default=0)

    # Achievement points
    achievement_points = db.Column(db.Integer, default=0)

    # Stats
    total_food_logs = db.Column(db.Integer, default=0)
    total_workouts = db.Column(db.Integer, default=0)
    total_days_active = db.Column(db.Integer, default=0)

    # Badges/titles unlocked
    titles_unlocked = db.Column(db.Text)  # JSON array
    current_title = db.Column(db.String(100))

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReferenceObject(db.Model):
    """User's calibrated reference objects for portion estimation"""
    __tablename__ = 'reference_objects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Reference object details
    object_type = db.Column(db.String(50), nullable=False)  # 'hand_palm', 'fist', 'thumb', 'plate', 'bowl', 'cup'

    # Calibrated measurements
    length_cm = db.Column(db.Numeric(6,2))
    width_cm = db.Column(db.Numeric(6,2))
    height_cm = db.Column(db.Numeric(6,2))
    volume_ml = db.Column(db.Numeric(8,2))
    area_cm2 = db.Column(db.Numeric(8,2))

    # Calibration images (if user uploaded reference photos)
    calibration_image = db.Column(db.String(255))

    # Usage stats
    times_used = db.Column(db.Integer, default=0)
    last_used = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
