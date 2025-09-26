#!/usr/bin/env python3
"""
Calorie Tracker Flask Application
AI-powered food recognition and calorie tracking system
"""

import os
import sqlite3
from datetime import datetime
import pytz
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import json
from pathlib import Path

# Import our custom modules (will create these)
from food_recognition import FoodRecognizer
from calorie_calculator import CalorieCalculator

# Flask app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
import os
database_path = os.environ.get('DATABASE_PATH', 'calorie_tracker.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize our custom services
food_recognizer = FoodRecognizer()
calorie_calculator = CalorieCalculator()

# Toronto timezone helper
def toronto_now():
    """Get current time in Toronto timezone"""
    toronto_tz = pytz.timezone('America/Toronto')
    return datetime.now(toronto_tz)

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    food_entries = db.relationship('FoodEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    workout_entries = db.relationship('WorkoutEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    settings = db.relationship('UserSettings', backref='user', uselist=False, cascade='all, delete-orphan')

class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Nutrition goals
    calorie_goal = db.Column(db.Integer, default=3000)
    protein_goal = db.Column(db.Integer, default=160)
    fat_goal = db.Column(db.Integer, default=100)
    carb_goal = db.Column(db.Integer, default=375)  # 50% of 3000 cal

    # User profile for calorie burn calculations
    weight_kg = db.Column(db.Numeric(5,2))  # Weight in kilograms
    height_cm = db.Column(db.Numeric(5,2))  # Height in centimeters
    age = db.Column(db.Integer)  # Age in years
    gender = db.Column(db.String(10))  # 'male', 'female', 'other'

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FoodDatabase(db.Model):
    __tablename__ = 'food_database'

    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(200), nullable=False)
    food_code = db.Column(db.String(50))
    calories_per_100g = db.Column(db.Numeric(8,2), nullable=False)
    protein_per_100g = db.Column(db.Numeric(8,2), default=0)
    carbs_per_100g = db.Column(db.Numeric(8,2), default=0)
    fat_per_100g = db.Column(db.Numeric(8,2), default=0)
    fiber_per_100g = db.Column(db.Numeric(8,2), default=0)
    sugar_per_100g = db.Column(db.Numeric(8,2), default=0)
    sodium_per_100g = db.Column(db.Numeric(8,2), default=0)
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FoodEntry(db.Model):
    __tablename__ = 'food_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_name = db.Column(db.String(200), nullable=False)
    estimated_weight_grams = db.Column(db.Numeric(8,2))
    actual_weight_grams = db.Column(db.Numeric(8,2))
    calories = db.Column(db.Numeric(8,2), nullable=False)
    protein = db.Column(db.Numeric(8,2), default=0)
    carbs = db.Column(db.Numeric(8,2), default=0)
    fat = db.Column(db.Numeric(8,2), default=0)

    # AI analysis results
    ai_confidence_score = db.Column(db.Numeric(3,2))
    ai_identified_foods = db.Column(db.Text)  # JSON string

    # User corrections
    user_corrected = db.Column(db.Boolean, default=False)
    original_ai_food_name = db.Column(db.String(200))

    # Image information
    image_filename = db.Column(db.String(255))
    image_path = db.Column(db.String(500))

    # Timing
    consumed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to analysis log
    analysis_log = db.relationship('AnalysisLog', backref='food_entry', uselist=False)

class AnalysisLog(db.Model):
    __tablename__ = 'analysis_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_entry_id = db.Column(db.Integer, db.ForeignKey('food_entries.id'))
    image_filename = db.Column(db.String(255))

    # AI Analysis Steps
    raw_ai_response = db.Column(db.Text)  # Raw LLM response
    identified_foods = db.Column(db.Text)  # JSON list of detected foods
    weight_estimation_logic = db.Column(db.Text)  # How weight was estimated
    calorie_calculation_steps = db.Column(db.Text)  # Step-by-step calculation
    data_source_used = db.Column(db.String(100))  # Which data source was used
    fallback_reasoning = db.Column(db.Text)  # Why fallbacks were used

    # Final Results
    final_food_name = db.Column(db.String(200))
    final_weight_grams = db.Column(db.Numeric(8,2))
    final_calories = db.Column(db.Numeric(8,2))
    final_protein = db.Column(db.Numeric(8,2))
    final_carbs = db.Column(db.Numeric(8,2))
    final_fat = db.Column(db.Numeric(8,2))

    # Confidence and Debugging
    ai_confidence = db.Column(db.Numeric(3,2))
    processing_time_ms = db.Column(db.Integer)
    errors_encountered = db.Column(db.Text)  # Any errors during processing

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WorkoutEntry(db.Model):
    __tablename__ = 'workout_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)  # "Jiu Jitsu", "Running", etc.
    intensity = db.Column(db.String(20), nullable=False)  # "light", "moderate", "high"
    duration_minutes = db.Column(db.Integer, nullable=False)  # Workout duration in minutes
    calories_burned = db.Column(db.Numeric(8,2), nullable=False)  # Calculated calories burned
    logged_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserFeedback(db.Model):
    __tablename__ = 'user_feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Original AI prediction
    ai_food_name = db.Column(db.String(200))
    ai_weight_grams = db.Column(db.Numeric(8,2))
    ai_calories = db.Column(db.Numeric(8,2))
    ai_protein = db.Column(db.Numeric(8,2))
    ai_carbs = db.Column(db.Numeric(8,2))
    ai_fat = db.Column(db.Numeric(8,2))

    # User corrections
    corrected_food_name = db.Column(db.String(200))
    corrected_weight_grams = db.Column(db.Numeric(8,2))
    corrected_calories = db.Column(db.Numeric(8,2))
    corrected_protein = db.Column(db.Numeric(8,2))
    corrected_carbs = db.Column(db.Numeric(8,2))
    corrected_fat = db.Column(db.Numeric(8,2))

    # Context for learning
    image_features = db.Column(db.Text)  # JSON string of visual features
    food_category = db.Column(db.String(100))
    confidence_level = db.Column(db.Numeric(3,2))

    # Learning metadata
    correction_type = db.Column(db.String(50))  # 'name', 'portion', 'nutrition', 'all'
    learned_from = db.Column(db.Integer, db.ForeignKey('food_entries.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Stats calculation functions
def calculate_today_stats(user_id):
    """Calculate today's nutrition and workout stats for a user"""
    from datetime import date
    today = date.today()

    # Get today's food entries
    today_entries = FoodEntry.query.filter_by(user_id=user_id)\
        .filter(FoodEntry.consumed_at >= today)\
        .all()

    total_calories = sum(float(entry.calories) for entry in today_entries)
    total_protein = sum(float(entry.protein or 0) for entry in today_entries)
    total_carbs = sum(float(entry.carbs or 0) for entry in today_entries)
    total_fat = sum(float(entry.fat or 0) for entry in today_entries)
    meal_count = len(today_entries)

    # Get today's workout entries
    today_workouts = WorkoutEntry.query.filter_by(user_id=user_id)\
        .filter(WorkoutEntry.logged_at >= today)\
        .all()

    total_calories_burned = sum(float(workout.calories_burned) for workout in today_workouts)
    workout_count = len(today_workouts)

    return {
        'calories': round(total_calories, 1),
        'meals': meal_count,
        'protein': round(total_protein, 1),
        'carbs': round(total_carbs, 1),
        'fat': round(total_fat, 1),
        'calories_burned': round(total_calories_burned, 1),
        'workouts': workout_count
    }

def calculate_quick_stats(user_id):
    """Calculate quick stats for sidebar"""
    from datetime import date, timedelta

    # This week's entries
    week_start = date.today() - timedelta(days=7)
    week_entries = FoodEntry.query.filter_by(user_id=user_id)\
        .filter(FoodEntry.consumed_at >= week_start)\
        .count()

    # Total entries ever
    total_entries = FoodEntry.query.filter_by(user_id=user_id).count()

    return {
        'this_week': week_entries,
        'total_logged': total_entries
    }

def calculate_history_stats(user_id):
    """Calculate statistics for the history page"""
    from datetime import date, timedelta

    # Today's calories
    today = date.today()
    today_entries = FoodEntry.query.filter_by(user_id=user_id)\
        .filter(FoodEntry.consumed_at >= today)\
        .all()
    today_calories = sum(float(entry.calories) for entry in today_entries)

    # This week's entries count
    week_start = date.today() - timedelta(days=7)
    week_entries = FoodEntry.query.filter_by(user_id=user_id)\
        .filter(FoodEntry.consumed_at >= week_start)\
        .count()

    # Calculate average daily calories (last 30 days)
    month_start = date.today() - timedelta(days=30)
    month_entries = FoodEntry.query.filter_by(user_id=user_id)\
        .filter(FoodEntry.consumed_at >= month_start)\
        .all()

    if month_entries:
        total_month_calories = sum(float(entry.calories) for entry in month_entries)
        avg_daily_calories = total_month_calories / 30
    else:
        avg_daily_calories = 0

    return {
        'today_calories': round(today_calories, 0),
        'this_week_entries': week_entries,
        'avg_daily_calories': round(avg_daily_calories, 0)
    }

def get_user_goals(user_id):
    """Get user's nutrition goals, creating defaults if needed"""
    settings = UserSettings.query.filter_by(user_id=user_id).first()

    if not settings:
        # Create default settings
        settings = UserSettings(
            user_id=user_id,
            calorie_goal=3000,
            protein_goal=160,
            fat_goal=100,
            carb_goal=375
        )
        db.session.add(settings)
        db.session.commit()

    return {
        'calorie_goal': settings.calorie_goal,
        'protein_goal': settings.protein_goal,
        'fat_goal': settings.fat_goal,
        'carb_goal': settings.carb_goal
    }

def log_analysis_process(user_id, food_entry_id, image_filename, analysis_data):
    """Log detailed AI analysis process for troubleshooting"""
    import time

    analysis_log = AnalysisLog(
        user_id=user_id,
        food_entry_id=food_entry_id,
        image_filename=image_filename,

        # AI Analysis Steps
        raw_ai_response=analysis_data.get('raw_ai_response', ''),
        identified_foods=json.dumps(analysis_data.get('identified_foods', [])),
        weight_estimation_logic=analysis_data.get('weight_estimation_logic', ''),
        calorie_calculation_steps=analysis_data.get('calorie_calculation_steps', ''),
        data_source_used=analysis_data.get('data_source_used', ''),
        fallback_reasoning=analysis_data.get('fallback_reasoning', ''),

        # Final Results
        final_food_name=analysis_data.get('final_food_name', ''),
        final_weight_grams=analysis_data.get('final_weight_grams', 0),
        final_calories=analysis_data.get('final_calories', 0),
        final_protein=analysis_data.get('final_protein', 0),
        final_carbs=analysis_data.get('final_carbs', 0),
        final_fat=analysis_data.get('final_fat', 0),

        # Confidence and Debugging
        ai_confidence=analysis_data.get('ai_confidence', 0),
        processing_time_ms=analysis_data.get('processing_time_ms', 0),
        errors_encountered=analysis_data.get('errors_encountered', '')
    )

    db.session.add(analysis_log)
    db.session.commit()

    return analysis_log.id

# AI Learning Functions
def capture_user_feedback(entry, original_analysis=None):
    """Capture user corrections for AI learning"""
    if not entry.user_corrected or not original_analysis:
        return

    # Determine what was corrected
    correction_types = []
    if original_analysis.get('food_name') != entry.food_name:
        correction_types.append('name')
    if abs(float(original_analysis.get('weight_grams', 0)) - float(entry.actual_weight_grams or 0)) > 5:
        correction_types.append('portion')
    if (abs(float(original_analysis.get('calories', 0)) - float(entry.calories)) > 10 or
        abs(float(original_analysis.get('protein', 0)) - float(entry.protein or 0)) > 2):
        correction_types.append('nutrition')

    correction_type = ','.join(correction_types) if correction_types else 'all'

    # Store the feedback
    feedback = UserFeedback(
        user_id=entry.user_id,
        ai_food_name=original_analysis.get('food_name'),
        ai_weight_grams=original_analysis.get('weight_grams'),
        ai_calories=original_analysis.get('calories'),
        ai_protein=original_analysis.get('protein'),
        ai_carbs=original_analysis.get('carbs'),
        ai_fat=original_analysis.get('fat'),
        corrected_food_name=entry.food_name,
        corrected_weight_grams=entry.actual_weight_grams,
        corrected_calories=entry.calories,
        corrected_protein=entry.protein,
        corrected_carbs=entry.carbs,
        corrected_fat=entry.fat,
        food_category=classify_food_category(entry.food_name),
        confidence_level=entry.ai_confidence_score,
        correction_type=correction_type,
        learned_from=entry.id
    )

    db.session.add(feedback)
    db.session.commit()

def classify_food_category(food_name):
    """Comprehensive food category classification for all food types"""
    food_name_lower = food_name.lower()

    # Grains & Carbs
    if any(word in food_name_lower for word in ['pizza', 'pasta', 'bread', 'rice', 'noodle', 'bagel', 'cereal', 'oatmeal', 'quinoa', 'barley', 'wheat', 'tortilla', 'wrap', 'sandwich']):
        return 'grain'

    # Proteins (including deli meats)
    elif any(word in food_name_lower for word in ['chicken', 'beef', 'pork', 'fish', 'meat', 'turkey', 'ham', 'salami', 'cold cut', 'deli', 'sausage', 'bacon', 'egg', 'tofu', 'beans', 'lentil', 'salmon', 'tuna']):
        return 'protein'

    # Fruits
    elif any(word in food_name_lower for word in ['apple', 'banana', 'orange', 'fruit', 'berry', 'grape', 'mango', 'pineapple', 'strawberry', 'blueberry', 'cherry', 'peach', 'pear', 'kiwi']):
        return 'fruit'

    # Vegetables
    elif any(word in food_name_lower for word in ['salad', 'vegetable', 'broccoli', 'carrot', 'spinach', 'lettuce', 'tomato', 'pepper', 'onion', 'potato', 'sweet potato', 'corn', 'peas', 'green', 'cabbage']):
        return 'vegetable'

    # Dairy
    elif any(word in food_name_lower for word in ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'cottage cheese', 'mozzarella', 'cheddar', 'parmesan']):
        return 'dairy'

    # Snacks & Processed
    elif any(word in food_name_lower for word in ['chips', 'crackers', 'pretzels', 'popcorn', 'nuts', 'trail mix', 'granola']):
        return 'snack'

    # Desserts & Sweets
    elif any(word in food_name_lower for word in ['cake', 'cookie', 'ice cream', 'candy', 'chocolate', 'brownie', 'pie', 'donut', 'muffin', 'sweet', 'dessert']):
        return 'dessert'

    # Fast Food
    elif any(word in food_name_lower for word in ['burger', 'fries', 'mcdonalds', 'subway', 'kfc', 'taco', 'burrito']):
        return 'fast_food'

    # Beverages
    elif any(word in food_name_lower for word in ['coffee', 'tea', 'soda', 'juice', 'water', 'beer', 'wine', 'smoothie', 'shake']):
        return 'beverage'

    else:
        return 'other'

def get_learning_context(user_id, food_name, food_category=None):
    """Get historical user corrections for similar foods"""
    if not food_category:
        food_category = classify_food_category(food_name)

    # Get recent corrections for similar foods
    similar_corrections = UserFeedback.query.filter_by(
        user_id=user_id,
        food_category=food_category
    ).order_by(UserFeedback.created_at.desc()).limit(10).all()

    # Get corrections for exact food names
    exact_corrections = UserFeedback.query.filter_by(
        user_id=user_id,
        ai_food_name=food_name
    ).order_by(UserFeedback.created_at.desc()).limit(5).all()

    # Get fuzzy matches for similar food names
    fuzzy_corrections = []
    if not exact_corrections:
        # Look for similar food names if no exact matches
        all_corrections = UserFeedback.query.filter_by(user_id=user_id).all()
        food_words = set(food_name.lower().split())

        for correction in all_corrections:
            if correction.ai_food_name:
                correction_words = set(correction.ai_food_name.lower().split())
                # If they share 2+ words, consider it a fuzzy match
                common_words = food_words.intersection(correction_words)
                if len(common_words) >= 2:
                    fuzzy_corrections.append(correction)

        # Sort fuzzy corrections by relevance: prioritize corrections with calorie changes, then by recency
        def correction_priority(correction):
            has_calorie_change = (correction.ai_calories and correction.corrected_calories and
                                abs(float(correction.corrected_calories) - float(correction.ai_calories)) / float(correction.ai_calories) > 0.5)
            has_portion_change = (correction.corrected_weight_grams and correction.ai_weight_grams and
                                abs(float(correction.corrected_weight_grams) - float(correction.ai_weight_grams)) / float(correction.ai_weight_grams) > 0.2)

            # Priority: corrections with significant changes first, then by recency
            priority_score = 0
            if has_calorie_change:
                priority_score += 100
            if has_portion_change:
                priority_score += 50
            # Add timestamp as tiebreaker (more recent = higher)
            priority_score += correction.created_at.timestamp() / 1000000
            return priority_score

        fuzzy_corrections.sort(key=correction_priority, reverse=True)
        fuzzy_corrections = fuzzy_corrections[:5]

    return {
        'similar_corrections': similar_corrections,
        'exact_corrections': exact_corrections,
        'fuzzy_corrections': fuzzy_corrections,
        'food_category': food_category
    }

def calculate_calories_burned(activity_type, intensity, duration_minutes, weight_kg):
    """
    Calculate calories burned using MET (Metabolic Equivalent) formula
    Formula: Calories Burned = MET × weight_kg × duration_hours
    """

    # MET values based on intensity levels
    met_values = {
        'light': {
            'default': 2.5,
            'yoga': 2.5,
            'walking': 3.0,
            'stretching': 2.3
        },
        'moderate': {
            'default': 5.0,
            'weight training': 4.8,
            'cycling': 5.8,
            'brisk walking': 4.5,
            'swimming': 5.8,
            'dancing': 4.8
        },
        'high': {
            'default': 9.0,
            'running': 11.0,
            'hiit': 12.0,
            'jiu jitsu': 10.0,
            'martial arts': 10.0,
            'boxing': 12.0,
            'basketball': 8.0,
            'soccer': 10.0
        }
    }

    # Get MET value for the activity
    activity_lower = activity_type.lower()
    intensity_mets = met_values.get(intensity, met_values['moderate'])

    # Try to find specific activity MET, otherwise use default for intensity
    met_value = intensity_mets.get('default')
    for activity, met in intensity_mets.items():
        if activity in activity_lower:
            met_value = met
            break

    # Convert duration to hours
    duration_hours = duration_minutes / 60.0

    # Calculate calories burned
    calories_burned = met_value * weight_kg * duration_hours

    return round(calories_burned, 2)

def apply_learning_adjustments(analysis_result, user_id):
    """Apply user learning patterns to AI analysis results"""
    food_name = analysis_result.get('food_name', '')
    learning_context = get_learning_context(user_id, food_name)

    # Apply exact food name corrections first
    exact_corrections = learning_context['exact_corrections']
    fuzzy_corrections = learning_context['fuzzy_corrections']

    # Use exact corrections if available, otherwise try fuzzy matches
    corrections_to_use = exact_corrections if exact_corrections else fuzzy_corrections
    correction_type = 'exact' if exact_corrections else 'fuzzy'

    learning_types = []

    if corrections_to_use:
        latest_correction = corrections_to_use[0]

        # Apply learning even with just 1 correction for significant changes
        if len(corrections_to_use) >= 1:
            # Apply name correction if it's a significant change
            if latest_correction.corrected_food_name != latest_correction.ai_food_name:
                analysis_result['food_name'] = latest_correction.corrected_food_name
                learning_types.append('name_correction')

            # Determine if this is primarily a portion correction or calorie correction
            has_portion_change = (latest_correction.corrected_weight_grams and latest_correction.ai_weight_grams and
                                abs(float(latest_correction.corrected_weight_grams) - float(latest_correction.ai_weight_grams)) / float(latest_correction.ai_weight_grams) > 0.2)

            has_calorie_change = (latest_correction.ai_calories and latest_correction.corrected_calories and
                                abs(float(latest_correction.corrected_calories) - float(latest_correction.ai_calories)) / float(latest_correction.ai_calories) > 0.5)

            if has_portion_change:
                # This is primarily a portion size correction
                weight_ratio = float(latest_correction.corrected_weight_grams) / float(latest_correction.ai_weight_grams)
                if 0.3 <= weight_ratio <= 5.0:  # Reasonable adjustment range
                    analysis_result['weight_grams'] *= weight_ratio
                    analysis_result['calories'] *= weight_ratio
                    learning_types.append('portion_adjustment')
            elif has_calorie_change:
                # This is primarily a calorie density correction (not portion)
                calorie_ratio = float(latest_correction.corrected_calories) / float(latest_correction.ai_calories)
                analysis_result['calories'] *= calorie_ratio
                learning_types.append('calorie_correction')

            # Set the learning applied field to show all types
            if learning_types:
                analysis_result['learning_applied'] = f"{correction_type}_{'_'.join(learning_types)}"

    # Apply category-based corrections
    similar_corrections = learning_context['similar_corrections']
    if similar_corrections and len(similar_corrections) >= 3:
        # Calculate average correction ratios for this food category
        calorie_ratios = []
        for correction in similar_corrections:
            if correction.ai_calories and correction.corrected_calories:
                ratio = float(correction.corrected_calories) / float(correction.ai_calories)
                if 0.3 <= ratio <= 3.0:  # Reasonable range
                    calorie_ratios.append(ratio)

        if calorie_ratios:
            avg_calorie_ratio = sum(calorie_ratios) / len(calorie_ratios)
            # Apply adjustment if it's consistent
            if abs(avg_calorie_ratio - 1.0) > 0.1:  # Only if significant difference
                analysis_result['calories'] *= avg_calorie_ratio
                analysis_result['learning_applied'] = 'category_calorie_adjustment'

    return analysis_result

# Routes
@app.route('/')
def index():
    """Home page - shows recent food entries and stats if logged in"""
    if current_user.is_authenticated:
        recent_entries = FoodEntry.query.filter_by(user_id=current_user.id)\
                                      .order_by(FoodEntry.consumed_at.desc())\
                                      .limit(10).all()

        # Calculate today's stats
        today_stats = calculate_today_stats(current_user.id)
        quick_stats = calculate_quick_stats(current_user.id)
        user_goals = get_user_goals(current_user.id)

        response = make_response(render_template('dashboard.html',
                               recent_entries=recent_entries,
                               today_stats=today_stats,
                               quick_stats=quick_stats,
                               user_goals=user_goals))

        # Disable caching to ensure fresh data
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        # Add timestamp for forcing fresh reload when redirected from edit
        if request.args.get('_refresh'):
            response.headers['X-Refresh'] = request.args.get('_refresh')

        return response
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))

        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_food():
    """Upload food image for recognition"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, WEBP, BMP, or TIFF images only.')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        timestamp = toronto_now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the image with AI
        try:
            import time
            start_time = time.time()

            # Recognize food in image
            recognition_result = food_recognizer.analyze_image(filepath)

            # Apply user learning adjustments to AI analysis
            analysis_result = {
                'food_name': recognition_result['primary_food'],
                'weight_grams': recognition_result.get('estimated_weight', 100),
                'calories': 0,  # Will be calculated next
                'protein': 0,
                'carbs': 0,
                'fat': 0
            }

            # Calculate calories
            calorie_result = calorie_calculator.calculate_calories(recognition_result)
            analysis_result.update({
                'calories': calorie_result['total_calories'],
                'protein': calorie_result.get('protein', 0),
                'carbs': calorie_result.get('carbs', 0),
                'fat': calorie_result.get('fat', 0)
            })

            # Apply learning adjustments based on user history
            try:
                analysis_result = apply_learning_adjustments(analysis_result, current_user.id)
            except Exception as e:
                print(f"Error applying learning adjustments: {e}")
                # Continue with original analysis if learning fails

            processing_time = int((time.time() - start_time) * 1000)  # Convert to ms

            # Store the initial entry (user can edit later) with learning adjustments applied
            food_entry = FoodEntry(
                user_id=current_user.id,
                food_name=analysis_result['food_name'],
                estimated_weight_grams=analysis_result['weight_grams'],
                calories=analysis_result['calories'],
                protein=analysis_result.get('protein', 0),
                carbs=analysis_result.get('carbs', 0),
                fat=analysis_result.get('fat', 0),
                ai_confidence_score=recognition_result.get('confidence'),
                ai_identified_foods=json.dumps(recognition_result.get('all_foods', [])),
                original_ai_food_name=recognition_result['primary_food'],
                image_filename=filename,
                image_path=filepath,
                consumed_at=toronto_now()
            )

            db.session.add(food_entry)
            db.session.commit()

            # Prepare detailed learning information for logging
            learning_info = ""
            if 'learning_applied' in analysis_result:
                learning_info = f"🧠 AI Learning Applied: {analysis_result['learning_applied']}. "

                # Track all adjustments made by learning
                original_name = recognition_result['primary_food']
                adjusted_name = analysis_result['food_name']
                if original_name != adjusted_name:
                    learning_info += f"Food name corrected: '{original_name}' → '{adjusted_name}'. "

                original_calories = calorie_result['total_calories']
                adjusted_calories = analysis_result['calories']
                if abs(original_calories - adjusted_calories) > 1:
                    learning_info += f"Calories adjusted: {original_calories} → {adjusted_calories}. "

                original_weight = recognition_result.get('estimated_weight', 0)
                adjusted_weight = analysis_result['weight_grams']
                if abs(original_weight - adjusted_weight) > 1:
                    learning_info += f"Weight adjusted: {original_weight}g → {adjusted_weight}g. "

                learning_info += "Based on your previous corrections for similar foods. "

            # Log detailed analysis for troubleshooting
            analysis_data = {
                'raw_ai_response': recognition_result.get('raw_response', 'AI recognition completed'),
                'identified_foods': recognition_result.get('all_foods', []),
                'weight_estimation_logic': f"Estimated weight: {recognition_result.get('estimated_weight', 0)}g based on visual analysis",
                'calorie_calculation_steps': f"Data source: {calorie_result.get('data_source', 'unknown')}, "
                                           f"Calculation: {recognition_result.get('estimated_weight', 0)}g × "
                                           f"{calorie_result.get('calories_per_100g', 0)}/100 = {calorie_result['total_calories']} calories",
                'data_source_used': calorie_result.get('data_source', 'unknown'),
                'fallback_reasoning': learning_info + calorie_result.get('fallback_reasoning', ''),
                'final_food_name': analysis_result['food_name'],  # Use adjusted food name
                'final_weight_grams': analysis_result['weight_grams'],  # Use adjusted weight
                'final_calories': analysis_result['calories'],  # Use adjusted calories
                'final_protein': analysis_result.get('protein', 0),  # Use adjusted protein
                'final_carbs': analysis_result.get('carbs', 0),  # Use adjusted carbs
                'final_fat': analysis_result.get('fat', 0),  # Use adjusted fat
                'ai_confidence': recognition_result.get('confidence', 0),
                'processing_time_ms': processing_time,
                'errors_encountered': ''
            }

            log_analysis_process(current_user.id, food_entry.id, filename, analysis_data)

            flash('Food logged successfully!')
            return redirect(url_for('edit_entry', entry_id=food_entry.id))

        except Exception as e:
            flash(f'Error processing image: {str(e)}')
            return redirect(url_for('upload_food'))

    return render_template('upload.html')

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    """Edit a food entry"""
    entry = FoodEntry.query.get_or_404(entry_id)

    # Ensure user owns this entry
    if entry.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Store original AI analysis for learning
        original_analysis = {
            'food_name': entry.original_ai_food_name or entry.food_name,
            'weight_grams': entry.estimated_weight_grams,
            'calories': entry.calories,
            'protein': entry.protein,
            'carbs': entry.carbs,
            'fat': entry.fat
        }

        # Update entry with user corrections
        entry.food_name = request.form['food_name']
        entry.actual_weight_grams = float(request.form.get('weight', 0))
        entry.calories = float(request.form['calories'])
        entry.protein = float(request.form.get('protein', 0))
        entry.carbs = float(request.form.get('carbs', 0))
        entry.fat = float(request.form.get('fat', 0))
        entry.user_corrected = True
        entry.updated_at = datetime.utcnow()

        db.session.commit()

        # Capture user feedback for AI learning
        try:
            capture_user_feedback(entry, original_analysis)
        except Exception as e:
            print(f"Error capturing user feedback: {e}")

        flash('Entry updated successfully!')
        return redirect(url_for('index', _refresh=datetime.utcnow().timestamp()))

    return render_template('edit_entry.html', entry=entry)

@app.route('/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    """Delete a food entry"""
    entry = FoodEntry.query.get_or_404(entry_id)

    # Ensure user owns this entry
    if entry.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('history'))

    # Delete associated image if it exists
    if entry.image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], entry.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete the entry
    db.session.delete(entry)
    db.session.commit()

    flash('Food entry deleted successfully!')
    return redirect(url_for('history'))

@app.route('/history')
@login_required
def history():
    """View food history"""
    page = request.args.get('page', 1, type=int)
    entries = FoodEntry.query.filter_by(user_id=current_user.id)\
                           .order_by(FoodEntry.consumed_at.desc())\
                           .paginate(page=page, per_page=20, error_out=False)

    # Calculate history stats
    history_stats = calculate_history_stats(current_user.id)

    return render_template('history.html', entries=entries, history_stats=history_stats)

@app.route('/workout', methods=['GET', 'POST'])
@login_required
def log_workout():
    """Log a workout entry"""
    if request.method == 'POST':
        activity_type = request.form.get('activity_type')
        intensity = request.form.get('intensity')
        duration_minutes = int(request.form.get('duration_minutes'))

        # Get user weight for calculation
        user_settings = UserSettings.query.filter_by(user_id=current_user.id).first()
        if not user_settings or not user_settings.weight_kg:
            flash('Please set your weight in profile to track workouts', 'error')
            return redirect(url_for('profile'))

        # Calculate calories burned
        calories_burned = calculate_calories_burned(
            activity_type, intensity, duration_minutes, float(user_settings.weight_kg)
        )

        # Create workout entry
        workout = WorkoutEntry(
            user_id=current_user.id,
            activity_type=activity_type,
            intensity=intensity,
            duration_minutes=duration_minutes,
            calories_burned=calories_burned
        )

        db.session.add(workout)
        db.session.commit()

        flash(f'Workout logged! You burned {calories_burned} calories.', 'success')
        return redirect(url_for('index'))

    return render_template('log_workout.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile and settings"""
    user_settings = UserSettings.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        if not user_settings:
            user_settings = UserSettings(user_id=current_user.id)
            db.session.add(user_settings)

        # Update profile fields
        user_settings.weight_kg = request.form.get('weight_kg')
        user_settings.height_cm = request.form.get('height_cm')
        user_settings.age = request.form.get('age', type=int)
        user_settings.gender = request.form.get('gender')

        # Update nutrition goals
        user_settings.calorie_goal = request.form.get('calorie_goal', type=int)
        user_settings.protein_goal = request.form.get('protein_goal', type=int)
        user_settings.fat_goal = request.form.get('fat_goal', type=int)
        user_settings.carb_goal = request.form.get('carb_goal', type=int)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', settings=user_settings)

@app.route('/api/search_food')
@login_required
def search_food():
    """API endpoint to search food database"""
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])

    foods = FoodDatabase.query.filter(
        FoodDatabase.food_name.contains(query)
    ).limit(10).all()

    results = []
    for food in foods:
        results.append({
            'name': food.food_name,
            'calories_per_100g': float(food.calories_per_100g),
            'protein_per_100g': float(food.protein_per_100g),
            'carbs_per_100g': float(food.carbs_per_100g),
            'fat_per_100g': float(food.fat_per_100g),
            'category': food.category
        })

    return jsonify(results)

@app.route('/api/stats/today')
@login_required
def api_today_stats():
    """API endpoint for today's stats"""
    stats = calculate_today_stats(current_user.id)
    return jsonify(stats)

@app.route('/api/stats/quick')
@login_required
def api_quick_stats():
    """API endpoint for quick stats"""
    stats = calculate_quick_stats(current_user.id)
    return jsonify(stats)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User settings page"""
    user_goals = get_user_goals(current_user.id)

    if request.method == 'POST':
        # Update user settings
        settings = UserSettings.query.filter_by(user_id=current_user.id).first()

        try:
            settings.calorie_goal = int(request.form['calorie_goal'])
            settings.protein_goal = int(request.form['protein_goal'])
            settings.fat_goal = int(request.form['fat_goal'])
            settings.carb_goal = int(request.form['carb_goal'])
            settings.updated_at = datetime.utcnow()

            db.session.commit()
            flash('Settings updated successfully!')
            return redirect(url_for('settings'))

        except ValueError:
            flash('Invalid input. Please enter valid numbers.')
        except Exception as e:
            flash(f'Error updating settings: {str(e)}')

    return render_template('settings.html', user_goals=user_goals)

@app.route('/api/analysis_log/<int:food_entry_id>')
@login_required
def api_analysis_log(food_entry_id):
    """API endpoint to get detailed analysis log for a food entry"""
    food_entry = FoodEntry.query.get_or_404(food_entry_id)

    # Ensure user owns this entry
    if food_entry.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    analysis_log = AnalysisLog.query.filter_by(food_entry_id=food_entry_id).first()

    if not analysis_log:
        return jsonify({'error': 'No analysis log found'}), 404

    return jsonify({
        'food_name': analysis_log.final_food_name,
        'weight_grams': float(analysis_log.final_weight_grams or 0),
        'calories': float(analysis_log.final_calories or 0),
        'protein': float(analysis_log.final_protein or 0),
        'carbs': float(analysis_log.final_carbs or 0),
        'fat': float(analysis_log.final_fat or 0),
        'data_source': analysis_log.data_source_used,
        'ai_confidence': float(analysis_log.ai_confidence or 0),
        'processing_time_ms': analysis_log.processing_time_ms,
        'weight_estimation_logic': analysis_log.weight_estimation_logic,
        'calorie_calculation_steps': analysis_log.calorie_calculation_steps,
        'fallback_reasoning': analysis_log.fallback_reasoning,
        'identified_foods': json.loads(analysis_log.identified_foods or '[]'),
        'errors_encountered': analysis_log.errors_encountered,
        'created_at': analysis_log.created_at.isoformat()
    })

@app.route('/sw.js')
def service_worker():
    """Serve the service worker file"""
    from flask import send_from_directory
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

def allowed_file(filename):
    """Check if uploaded file is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff', 'tif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    """Initialize database with schema and sample data"""
    with app.app_context():
        db.create_all()

        # Add sample food data if database is empty
        if FoodDatabase.query.count() == 0:
            sample_foods = [
                ('Apple', 52, 0.3, 14, 0.2, 'fruits'),
                ('Banana', 89, 1.1, 23, 0.3, 'fruits'),
                ('Rice (cooked)', 130, 2.7, 28, 0.3, 'grains'),
                ('Chicken Breast', 165, 31, 0, 3.6, 'protein'),
                ('Broccoli', 34, 2.8, 7, 0.4, 'vegetables'),
                ('Bread (white)', 265, 9, 49, 3.2, 'grains'),
                ('Egg', 155, 13, 1.1, 11, 'protein'),
                ('Salmon', 208, 20, 0, 13, 'protein'),
                ('Pasta (cooked)', 131, 5, 25, 1.1, 'grains'),
                ('Milk (whole)', 61, 3.2, 4.8, 3.3, 'dairy')
            ]

            for name, cal, protein, carbs, fat, category in sample_foods:
                food = FoodDatabase(
                    food_name=name,
                    calories_per_100g=cal,
                    protein_per_100g=protein,
                    carbs_per_100g=carbs,
                    fat_per_100g=fat,
                    category=category
                )
                db.session.add(food)

            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5151)