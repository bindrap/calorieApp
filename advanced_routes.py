#!/usr/bin/env python3
"""
Advanced Features Routes Integration
Flask routes for AI Coach, Health Timeline, Gamification, and Mood Tracking
Add these imports and routes to app.py
"""

# ==================== ADDITIONAL IMPORTS ====================
# Add these to the top of app.py after existing imports

from datetime import date, timedelta
from sqlalchemy import func, and_, or_

# Import new modules
from ai_chat_coach import AIChatCoach
from gamification_service import GamificationService
from meal_suggestion_engine import MealSuggestionEngine
from multi_item_recognition import MultiItemFoodRecognizer, SmartPortionEstimator

# Note: Models from health_timeline_models.py should be integrated into app.py's models section
# For now, we'll define them inline in the routes that need them

# Initialize services
ai_coach = AIChatCoach()
gamification_service = GamificationService()
meal_suggester = MealSuggestionEngine()
multi_item_recognizer = MultiItemFoodRecognizer()

# ==================== HELPER FUNCTIONS ====================

def get_user_context(user_id):
    """Get user's current context for AI coach"""
    user = User.query.get(user_id)
    settings = UserSettings.query.filter_by(user_id=user_id).first()

    if not settings:
        return {
            'consumed_today': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0},
            'goals': {'calories': 3000, 'protein': 160, 'carbs': 375, 'fat': 100},
            'remaining': {'calories': 3000, 'protein': 160, 'carbs': 375, 'fat': 100}
        }

    # Get today's food entries
    today = date.today()
    food_entries = FoodEntry.query.filter(
        FoodEntry.user_id == user_id,
        func.date(FoodEntry.consumed_at) == today
    ).all()

    # Calculate consumed
    consumed = {
        'calories': sum(float(entry.calories or 0) for entry in food_entries),
        'protein': sum(float(entry.protein or 0) for entry in food_entries),
        'carbs': sum(float(entry.carbs or 0) for entry in food_entries),
        'fat': sum(float(entry.fat or 0) for entry in food_entries)
    }

    # Get workouts
    workout_entries = WorkoutEntry.query.filter(
        WorkoutEntry.user_id == user_id,
        func.date(WorkoutEntry.logged_at) == today
    ).all()

    calories_burned = sum(float(entry.calories_burned or 0) for entry in workout_entries)

    goals = {
        'calories': settings.calorie_goal,
        'protein': settings.protein_goal,
        'carbs': settings.carb_goal,
        'fat': settings.fat_goal
    }

    remaining = {
        'calories': goals['calories'] - consumed['calories'] + calories_burned,
        'protein': goals['protein'] - consumed['protein'],
        'carbs': goals['carbs'] - consumed['carbs'],
        'fat': goals['fat'] - consumed['fat']
    }

    return {
        'consumed_today': consumed,
        'goals': goals,
        'remaining': remaining,
        'calories_burned': calories_burned
    }


def get_or_create_user_level(user_id):
    """Get or create user level data"""
    # Check if user_levels table exists
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        if 'user_levels' not in tables:
            # Table doesn't exist yet, return default
            return {
                'current_level': 1,
                'current_xp': 0,
                'xp_for_next_level': 100,
                'total_xp_earned': 0,
                'achievement_points': 0,
                'total_food_logs': 0,
                'total_workouts': 0,
                'total_days_active': 0,
                'current_title': 'Beginner'
            }

        # Use raw SQL to avoid ORM issues if model not defined
        result = db.session.execute(
            "SELECT * FROM user_levels WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        if result:
            return {
                'current_level': result[2] if len(result) > 2 else 1,
                'current_xp': result[3] if len(result) > 3 else 0,
                'xp_for_next_level': result[4] if len(result) > 4 else 100,
                'total_xp_earned': result[5] if len(result) > 5 else 0,
                'achievement_points': result[6] if len(result) > 6 else 0,
                'total_food_logs': result[7] if len(result) > 7 else 0,
                'total_workouts': result[8] if len(result) > 8 else 0,
                'total_days_active': result[9] if len(result) > 9 else 0,
                'current_title': result[11] if len(result) > 11 else 'Beginner'
            }
        else:
            # Create new user level
            db.session.execute(
                """INSERT INTO user_levels
                   (user_id, current_level, current_xp, xp_for_next_level, total_xp_earned,
                    achievement_points, total_food_logs, total_workouts, total_days_active, current_title)
                   VALUES (?, 1, 0, 100, 0, 0, 0, 0, 0, 'Beginner')""",
                (user_id,)
            )
            db.session.commit()

            return {
                'current_level': 1,
                'current_xp': 0,
                'xp_for_next_level': 100,
                'total_xp_earned': 0,
                'achievement_points': 0,
                'total_food_logs': 0,
                'total_workouts': 0,
                'total_days_active': 0,
                'current_title': 'Beginner'
            }
    except Exception as e:
        print(f"Error getting user level: {e}")
        return {
            'current_level': 1,
            'current_xp': 0,
            'xp_for_next_level': 100,
            'total_xp_earned': 0,
            'achievement_points': 0,
            'total_food_logs': 0,
            'total_workouts': 0,
            'total_days_active': 0,
            'current_title': 'Beginner'
        }


def get_user_streaks(user_id):
    """Get user's streaks"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        if 'user_streaks' not in tables:
            return {
                'food_logging': {'current_streak_days': 0, 'longest_streak_days': 0},
                'workout': {'current_streak_days': 0, 'longest_streak_days': 0},
                'goal_hitting': {'current_streak_days': 0, 'longest_streak_days': 0}
            }

        streaks = {}
        for streak_type in ['food_logging', 'workout', 'goal_hitting']:
            result = db.session.execute(
                "SELECT current_streak_days, longest_streak_days FROM user_streaks WHERE user_id = ? AND streak_type = ?",
                (user_id, streak_type)
            ).fetchone()

            if result:
                streaks[streak_type] = {
                    'current_streak_days': result[0],
                    'longest_streak_days': result[1]
                }
            else:
                streaks[streak_type] = {'current_streak_days': 0, 'longest_streak_days': 0}

        return streaks
    except Exception as e:
        print(f"Error getting streaks: {e}")
        return {
            'food_logging': {'current_streak_days': 0, 'longest_streak_days': 0},
            'workout': {'current_streak_days': 0, 'longest_streak_days': 0},
            'goal_hitting': {'current_streak_days': 0, 'longest_streak_days': 0}
        }


# ==================== AI COACH ROUTES ====================

@app.route('/ai-coach')
@login_required
def ai_coach_page():
    """Render AI coach chat interface"""
    return render_template('ai_coach.html')


@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """Process chat messages"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        confirmation_data = data.get('confirmation_data')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Get user context
        context = get_user_context(current_user.id)

        # Handle confirmation flow
        if confirmation_data and message.lower() in ['confirm', 'cancel']:
            if message.lower() == 'confirm':
                # Execute the action
                intent = confirmation_data.get('intent')

                if intent == 'log_food':
                    # Create food entry
                    extracted = confirmation_data.get('extracted_data', {})
                    nutrition = confirmation_data.get('estimated_nutrition', {})

                    foods_text = ', '.join([f"{food['name']}" for food in extracted.get('foods', [])])

                    entry = FoodEntry(
                        user_id=current_user.id,
                        food_name=foods_text,
                        calories=nutrition.get('calories', 0),
                        protein=nutrition.get('protein', 0),
                        carbs=nutrition.get('carbs', 0),
                        fat=nutrition.get('fat', 0),
                        consumed_at=toronto_now()
                    )
                    db.session.add(entry)
                    db.session.commit()

                    return jsonify({
                        'intent': 'log_food',
                        'status': 'completed',
                        'response': f'✅ Logged {foods_text}! Entry saved successfully.',
                        'action_required': None
                    })

                elif intent == 'log_workout':
                    # Create workout entry
                    extracted = confirmation_data.get('extracted_data', {})
                    calories = confirmation_data.get('estimated_calories', 0)

                    entry = WorkoutEntry(
                        user_id=current_user.id,
                        activity_type=extracted.get('activity_type', 'Unknown'),
                        intensity=extracted.get('intensity', 'moderate'),
                        duration_minutes=extracted.get('duration_minutes', 0),
                        calories_burned=calories,
                        logged_at=toronto_now()
                    )
                    db.session.add(entry)
                    db.session.commit()

                    return jsonify({
                        'intent': 'log_workout',
                        'status': 'completed',
                        'response': f'✅ Logged {extracted.get("activity_type")}! Workout saved successfully.',
                        'action_required': None
                    })
            else:
                return jsonify({
                    'intent': 'cancel',
                    'status': 'cancelled',
                    'response': 'Okay, cancelled. Let me know if you need anything else!',
                    'action_required': None
                })

        # Process new message with AI coach
        result = ai_coach.process_message(message, context)

        # Save chat message to database (if table exists)
        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            if 'chat_messages' in inspector.get_table_names():
                db.session.execute(
                    """INSERT INTO chat_messages (user_id, role, content, extracted_intent, conversation_id, sent_at)
                       VALUES (?, 'user', ?, ?, ?, ?)""",
                    (current_user.id, message, result.get('intent'), conversation_id, datetime.utcnow())
                )
                db.session.execute(
                    """INSERT INTO chat_messages (user_id, role, content, extracted_intent, conversation_id, sent_at)
                       VALUES (?, 'assistant', ?, ?, ?, ?)""",
                    (current_user.id, result.get('response'), result.get('intent'), conversation_id, datetime.utcnow())
                )
                db.session.commit()
        except Exception as e:
            print(f"Error saving chat messages: {e}")

        return jsonify(result)

    except Exception as e:
        print(f"Error in chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'intent': 'error',
            'status': 'error',
            'response': 'Sorry, I encountered an error processing your message. Please try again.',
            'error': str(e)
        }), 500


@app.route('/api/daily-stats')
@login_required
def daily_stats():
    """Get today's consumption and remaining macros"""
    try:
        context = get_user_context(current_user.id)
        return jsonify(context)
    except Exception as e:
        print(f"Error getting daily stats: {e}")
        return jsonify({
            'consumed': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0},
            'goals': {'calories': 3000, 'protein': 160, 'carbs': 375, 'fat': 100},
            'remaining': {'calories': 3000, 'protein': 160, 'carbs': 375, 'fat': 100}
        })


# ==================== HEALTH TIMELINE ROUTES ====================

@app.route('/health-timeline')
@login_required
def health_timeline_page():
    """Render health timeline page"""
    return render_template('health_timeline.html')


@app.route('/api/health-timeline')
@login_required
def health_timeline_api():
    """Get health timeline events"""
    try:
        date_range = request.args.get('range', 'week')
        filters = json.loads(request.args.get('filters', '{"food": true, "workout": true, "sleep": true, "mood": true, "biometric": true}'))

        # Calculate date range
        today = date.today()
        if date_range == 'today':
            start_date = today
            end_date = today
        elif date_range == 'yesterday':
            start_date = today - timedelta(days=1)
            end_date = today - timedelta(days=1)
        elif date_range == 'week':
            start_date = today - timedelta(days=7)
            end_date = today
        elif date_range == 'month':
            start_date = today - timedelta(days=30)
            end_date = today
        else:
            start_date = today - timedelta(days=7)
            end_date = today

        events = []

        # Get food entries
        if filters.get('food', True):
            food_entries = FoodEntry.query.filter(
                FoodEntry.user_id == current_user.id,
                func.date(FoodEntry.consumed_at) >= start_date,
                func.date(FoodEntry.consumed_at) <= end_date
            ).all()

            for entry in food_entries:
                events.append({
                    'event_type': 'food',
                    'title': entry.food_name,
                    'occurred_at': entry.consumed_at.isoformat(),
                    'calories_net': float(entry.calories or 0),
                    'data': {
                        'calories': float(entry.calories or 0),
                        'protein': float(entry.protein or 0),
                        'carbs': float(entry.carbs or 0),
                        'fat': float(entry.fat or 0)
                    },
                    'source': 'manual'
                })

        # Get workout entries
        if filters.get('workout', True):
            workout_entries = WorkoutEntry.query.filter(
                WorkoutEntry.user_id == current_user.id,
                func.date(WorkoutEntry.logged_at) >= start_date,
                func.date(WorkoutEntry.logged_at) <= end_date
            ).all()

            for entry in workout_entries:
                events.append({
                    'event_type': 'workout',
                    'title': entry.activity_type,
                    'occurred_at': entry.logged_at.isoformat(),
                    'duration_minutes': entry.duration_minutes,
                    'calories_net': -float(entry.calories_burned or 0),  # Negative because burned
                    'data': {
                        'activity': entry.activity_type,
                        'intensity': entry.intensity,
                        'duration': entry.duration_minutes,
                        'calories_burned': float(entry.calories_burned or 0)
                    },
                    'source': 'manual'
                })

        # Get mood entries (if table exists)
        if filters.get('mood', True):
            try:
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                if 'mood_entries' in inspector.get_table_names():
                    mood_results = db.session.execute(
                        """SELECT mood_score, energy_level, stress_level, logged_at
                           FROM mood_entries
                           WHERE user_id = ? AND date(logged_at) >= ? AND date(logged_at) <= ?
                           ORDER BY logged_at DESC""",
                        (current_user.id, start_date, end_date)
                    ).fetchall()

                    for row in mood_results:
                        events.append({
                            'event_type': 'mood',
                            'title': f'Mood Check-in',
                            'occurred_at': row[3].isoformat() if isinstance(row[3], datetime) else row[3],
                            'data': {
                                'mood_score': row[0],
                                'energy_level': row[1],
                                'stress_level': row[2]
                            },
                            'source': 'manual'
                        })
            except Exception as e:
                print(f"Error loading mood entries: {e}")

        # Sort events by time
        events.sort(key=lambda x: x['occurred_at'], reverse=True)

        # Calculate summary
        net_calories = sum(e.get('calories_net', 0) for e in events)
        workout_count = sum(1 for e in events if e['event_type'] == 'workout')
        mood_scores = [e['data']['mood_score'] for e in events if e['event_type'] == 'mood' and 'mood_score' in e.get('data', {})]
        avg_mood = sum(mood_scores) / len(mood_scores) if mood_scores else None

        summary = {
            'net_calories': int(net_calories),
            'workout_count': workout_count,
            'avg_sleep_hours': None,  # TODO: Calculate from sleep entries
            'avg_mood': round(avg_mood, 1) if avg_mood else None
        }

        return jsonify({
            'events': events,
            'summary': summary
        })

    except Exception as e:
        print(f"Error getting timeline: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'events': [], 'summary': {}}), 500


# ==================== GAMIFICATION ROUTES ====================

@app.route('/gamification')
@login_required
def gamification_page():
    """Render gamification dashboard"""
    return render_template('gamification.html')


@app.route('/api/gamification/stats')
@login_required
def gamification_stats():
    """Get gamification stats"""
    try:
        # Get user level
        level_data = get_or_create_user_level(current_user.id)

        # Get streaks
        streaks = get_user_streaks(current_user.id)

        # Get achievements (simplified for now)
        achievements = [
            {
                'id': 1,
                'name': 'First Workout',
                'description': 'Complete your first workout',
                'icon': '🎯',
                'category': 'milestone',
                'points': 10,
                'unlocked': level_data['total_workouts'] >= 1,
                'progress': min(level_data['total_workouts'], 1),
                'criteria_value': 1,
                'unlocked_at': None
            },
            {
                'id': 2,
                'name': '10 Workouts',
                'description': 'Complete 10 workouts',
                'icon': '💪',
                'category': 'milestone',
                'points': 100,
                'unlocked': level_data['total_workouts'] >= 10,
                'progress': min(level_data['total_workouts'], 10),
                'criteria_value': 10,
                'unlocked_at': None
            },
            {
                'id': 3,
                'name': '7 Day Streak',
                'description': 'Log for 7 days in a row',
                'icon': '🔥',
                'category': 'streak',
                'points': 200,
                'unlocked': streaks['food_logging']['current_streak_days'] >= 7,
                'progress': min(streaks['food_logging']['current_streak_days'], 7),
                'criteria_value': 7,
                'unlocked_at': None
            }
        ]

        return jsonify({
            'level': level_data,
            'streaks': streaks,
            'achievements': achievements
        })

    except Exception as e:
        print(f"Error getting gamification stats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'level': {
                'current_level': 1,
                'current_xp': 0,
                'xp_for_next_level': 100,
                'total_xp_earned': 0,
                'achievement_points': 0,
                'total_food_logs': 0,
                'total_workouts': 0,
                'total_days_active': 0,
                'current_title': 'Beginner'
            },
            'streaks': {
                'food_logging': {'current_streak_days': 0, 'longest_streak_days': 0},
                'workout': {'current_streak_days': 0, 'longest_streak_days': 0},
                'goal_hitting': {'current_streak_days': 0, 'longest_streak_days': 0}
            },
            'achievements': []
        })


# ==================== MOOD TRACKING ROUTES ====================

@app.route('/mood-tracker')
@login_required
def mood_tracker_page():
    """Render mood tracker page"""
    return render_template('mood_tracker.html')


@app.route('/api/mood/log', methods=['POST'])
@login_required
def log_mood():
    """Log mood entry"""
    try:
        data = request.json

        # Check if mood_entries table exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'mood_entries' not in inspector.get_table_names():
            return jsonify({'error': 'Mood tracking not available. Please run database migration.'}), 400

        # Insert mood entry
        db.session.execute(
            """INSERT INTO mood_entries
               (user_id, mood_score, energy_level, stress_level, motivation, emotions, notes, logged_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (current_user.id, data['mood_score'], data['energy_level'], data['stress_level'],
             data['motivation'], json.dumps(data['emotions']), data.get('notes', ''), datetime.utcnow())
        )
        db.session.commit()

        return jsonify({'success': True, 'message': 'Mood entry logged successfully'})

    except Exception as e:
        print(f"Error logging mood: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/mood/recent')
@login_required
def recent_moods():
    """Get recent mood entries"""
    try:
        limit = int(request.args.get('limit', 5))

        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'mood_entries' not in inspector.get_table_names():
            return jsonify([])

        results = db.session.execute(
            """SELECT mood_score, energy_level, stress_level, motivation, emotions, notes, logged_at
               FROM mood_entries
               WHERE user_id = ?
               ORDER BY logged_at DESC
               LIMIT ?""",
            (current_user.id, limit)
        ).fetchall()

        entries = []
        for row in results:
            entries.append({
                'mood_score': row[0],
                'energy_level': row[1],
                'stress_level': row[2],
                'motivation': row[3],
                'emotions': row[4],  # JSON string
                'notes': row[5],
                'logged_at': row[6].isoformat() if isinstance(row[6], datetime) else row[6]
            })

        return jsonify(entries)

    except Exception as e:
        print(f"Error getting recent moods: {e}")
        return jsonify([])


@app.route('/api/mood/today-summary')
@login_required
def today_mood_summary():
    """Get today's mood summary"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if 'mood_entries' not in inspector.get_table_names():
            return jsonify({'count': 0})

        today = date.today()
        results = db.session.execute(
            """SELECT mood_score, energy_level, stress_level, motivation
               FROM mood_entries
               WHERE user_id = ? AND date(logged_at) = ?""",
            (current_user.id, today)
        ).fetchall()

        if not results:
            return jsonify({'count': 0})

        mood_scores = [row[0] for row in results]
        energy_scores = [row[1] for row in results]
        stress_scores = [row[2] for row in results]
        motivation_scores = [row[3] for row in results]

        return jsonify({
            'count': len(results),
            'avg_mood': sum(mood_scores) / len(mood_scores),
            'avg_energy': sum(energy_scores) / len(energy_scores),
            'avg_stress': sum(stress_scores) / len(stress_scores),
            'avg_motivation': sum(motivation_scores) / len(motivation_scores)
        })

    except Exception as e:
        print(f"Error getting today summary: {e}")
        return jsonify({'count': 0})


# ==================== END OF ROUTES ====================
# These routes should be added to app.py before the "if __name__ == '__main__':" line
