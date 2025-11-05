#!/usr/bin/env python3
"""
Gamification Service
Handles streaks, achievements, leveling, and rewards to keep users motivated
"""

from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Tuple
import json


class GamificationService:
    """
    Service for managing gamification features: streaks, levels, achievements
    """

    def __init__(self):
        self.xp_per_level_base = 100  # XP needed for level 1→2
        self.xp_scale_factor = 1.15  # Each level requires 15% more XP

    # ==================== STREAK MANAGEMENT ====================

    def update_streak(
        self,
        user_id: int,
        streak_type: str,
        activity_date: date,
        current_streak_data: Optional[Dict] = None
    ) -> Dict:
        """
        Update user's streak for a specific activity type

        Args:
            user_id: User ID
            streak_type: 'food_logging', 'workout', 'goal_hitting'
            activity_date: Date of the activity
            current_streak_data: Current streak info from database

        Returns:
            Updated streak data
        """

        if not current_streak_data:
            # New streak
            return {
                'current_streak_days': 1,
                'longest_streak_days': 1,
                'streak_started_at': activity_date,
                'last_activity_date': activity_date,
                'total_activities': 1,
                'streak_status': 'started',
                'days_since_break': 0
            }

        last_activity = current_streak_data.get('last_activity_date')
        current_streak = current_streak_data.get('current_streak_days', 0)
        longest_streak = current_streak_data.get('longest_streak_days', 0)

        # Calculate days difference
        if isinstance(last_activity, str):
            last_activity = datetime.fromisoformat(last_activity).date()

        days_diff = (activity_date - last_activity).days

        if days_diff == 0:
            # Same day, no change to streak
            return {
                **current_streak_data,
                'total_activities': current_streak_data.get('total_activities', 0) + 1
            }

        elif days_diff == 1:
            # Consecutive day - streak continues!
            new_streak = current_streak + 1
            return {
                'current_streak_days': new_streak,
                'longest_streak_days': max(new_streak, longest_streak),
                'streak_started_at': current_streak_data.get('streak_started_at'),
                'last_activity_date': activity_date,
                'total_activities': current_streak_data.get('total_activities', 0) + 1,
                'streak_status': 'active',
                'days_since_break': 0,
                'milestone_reached': self._check_streak_milestone(new_streak)
            }

        else:
            # Streak broken - start new streak
            return {
                'current_streak_days': 1,
                'longest_streak_days': longest_streak,
                'streak_started_at': activity_date,
                'last_activity_date': activity_date,
                'total_activities': current_streak_data.get('total_activities', 0) + 1,
                'streak_status': 'restarted',
                'days_since_break': days_diff - 1,
                'longest_streak_ended_at': last_activity if current_streak == longest_streak else None
            }

    def _check_streak_milestone(self, streak_days: int) -> Optional[str]:
        """Check if streak reached a milestone"""
        milestones = [7, 14, 30, 60, 100, 365]
        if streak_days in milestones:
            return f"{streak_days}_day_streak"
        return None

    def get_streak_message(self, streak_data: Dict) -> str:
        """Get motivational message based on streak status"""

        current = streak_data.get('current_streak_days', 0)
        status = streak_data.get('streak_status', 'active')

        if status == 'started':
            return "🎯 Streak started! Keep it up tomorrow!"

        elif status == 'active':
            if current >= 365:
                return f"👑 LEGENDARY! {current} day streak! You're unstoppable!"
            elif current >= 100:
                return f"🏆 AMAZING! {current} day streak! You're an inspiration!"
            elif current >= 30:
                return f"⭐ Incredible! {current} day streak! You're crushing it!"
            elif current >= 7:
                return f"🔥 {current} day streak! You're on fire!"
            else:
                return f"💪 {current} days in a row! Keep building momentum!"

        elif status == 'restarted':
            return f"🔄 Fresh start! You've got this. Previous best: {streak_data.get('longest_streak_days', 0)} days."

        return "Keep going!"

    # ==================== LEVEL & XP MANAGEMENT ====================

    def calculate_xp_for_next_level(self, current_level: int) -> int:
        """Calculate XP needed for next level"""
        return int(self.xp_per_level_base * (self.xp_scale_factor ** (current_level - 1)))

    def award_xp(
        self,
        user_id: int,
        xp_amount: int,
        xp_source: str,
        current_level_data: Dict
    ) -> Dict:
        """
        Award XP to user and check for level ups

        Args:
            user_id: User ID
            xp_amount: Amount of XP to award
            xp_source: Source of XP ('food_log', 'workout', 'achievement', 'streak_milestone')
            current_level_data: Current level info from database

        Returns:
            Updated level data with level_up flag
        """

        current_level = current_level_data.get('current_level', 1)
        current_xp = current_level_data.get('current_xp', 0)
        xp_needed = current_level_data.get('xp_for_next_level', 100)
        total_xp = current_level_data.get('total_xp_earned', 0)

        # Add XP
        new_current_xp = current_xp + xp_amount
        new_total_xp = total_xp + xp_amount

        # Check for level up
        levels_gained = 0
        while new_current_xp >= xp_needed:
            new_current_xp -= xp_needed
            current_level += 1
            levels_gained += 1
            xp_needed = self.calculate_xp_for_next_level(current_level)

        result = {
            'current_level': current_level,
            'current_xp': new_current_xp,
            'xp_for_next_level': xp_needed,
            'total_xp_earned': new_total_xp,
            'xp_awarded': xp_amount,
            'xp_source': xp_source,
            'leveled_up': levels_gained > 0,
            'levels_gained': levels_gained
        }

        # Add title if leveled up
        if levels_gained > 0:
            result['new_title'] = self._get_title_for_level(current_level)
            result['rewards'] = self._get_level_up_rewards(current_level)

        return result

    def calculate_xp_for_activity(self, activity_type: str, activity_data: Dict) -> int:
        """
        Calculate XP earned for an activity

        Args:
            activity_type: 'food_log', 'workout', 'goal_complete', 'streak_day'
            activity_data: Additional data about the activity

        Returns:
            XP amount
        """

        base_xp = {
            'food_log': 10,
            'food_log_with_photo': 15,
            'food_log_accurate': 20,  # If user corrects or confirms AI
            'workout': 25,
            'workout_intense': 40,
            'goal_complete': 50,
            'daily_goal_hit': 100,
            'weekly_goal_hit': 250,
            'streak_day': 5,
            'streak_week': 50,
            'streak_month': 200,
            'achievement': 100
        }

        xp = base_xp.get(activity_type, 10)

        # Bonuses
        if activity_type == 'workout':
            duration = activity_data.get('duration_minutes', 0)
            if duration >= 60:
                xp += 20  # Bonus for 60+ min workout
            intensity = activity_data.get('intensity', 'moderate')
            if intensity == 'high':
                xp += 15  # Bonus for high intensity

        elif activity_type == 'food_log':
            if activity_data.get('has_photo'):
                xp += 5
            if activity_data.get('user_corrected') or activity_data.get('user_confirmed'):
                xp += 5
            if activity_data.get('barcode_scanned'):
                xp += 10  # Bonus for accurate barcode scanning

        return xp

    def _get_title_for_level(self, level: int) -> str:
        """Get title/rank for level"""
        titles = [
            (1, "Beginner"),
            (5, "Novice Tracker"),
            (10, "Dedicated Logger"),
            (15, "Nutrition Enthusiast"),
            (20, "Macro Master"),
            (25, "Fitness Guru"),
            (30, "Health Champion"),
            (40, "Wellness Warrior"),
            (50, "Legendary Tracker"),
            (75, "Elite Nutritionist"),
            (100, "Grand Master")
        ]

        for threshold, title in reversed(titles):
            if level >= threshold:
                return title

        return "Beginner"

    def _get_level_up_rewards(self, new_level: int) -> Dict:
        """Get rewards for leveling up"""
        rewards = {
            'message': f"🎉 Congratulations! You reached Level {new_level}!",
            'badges': []
        }

        # Milestone rewards
        if new_level == 5:
            rewards['badges'].append('First Milestone')
            rewards['unlock'] = 'Advanced nutrition insights'
        elif new_level == 10:
            rewards['badges'].append('Dedicated User')
            rewards['unlock'] = 'Custom meal templates'
        elif new_level == 25:
            rewards['badges'].append('Expert Tracker')
            rewards['unlock'] = 'Priority AI suggestions'
        elif new_level == 50:
            rewards['badges'].append('Legend')
            rewards['unlock'] = 'Exclusive themes'
        elif new_level == 100:
            rewards['badges'].append('Grand Master')
            rewards['unlock'] = 'All premium features'

        return rewards

    # ==================== ACHIEVEMENT MANAGEMENT ====================

    def check_achievements(
        self,
        user_id: int,
        user_stats: Dict,
        recent_activity: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Check if user has unlocked any new achievements

        Args:
            user_id: User ID
            user_stats: User's cumulative stats
            recent_activity: Most recent activity that triggered this check

        Returns:
            List of newly unlocked achievements
        """

        unlocked = []

        # Define achievement criteria
        achievements = self._get_achievement_definitions()

        for achievement in achievements:
            if self._check_achievement_criteria(achievement, user_stats, recent_activity):
                unlocked.append({
                    'achievement_id': achievement['id'],
                    'name': achievement['name'],
                    'description': achievement['description'],
                    'icon': achievement['icon'],
                    'category': achievement['category'],
                    'points': achievement['points'],
                    'unlocked_at': datetime.utcnow(),
                    'message': f"🏆 Achievement Unlocked: {achievement['name']}!"
                })

        return unlocked

    def _get_achievement_definitions(self) -> List[Dict]:
        """Get all achievement definitions"""
        return [
            # Milestone achievements
            {'id': 'first_workout', 'name': 'First Workout', 'description': 'Complete your first workout', 'icon': '🎯', 'category': 'milestone', 'criteria_type': 'workout_count', 'criteria_value': 1, 'points': 10},
            {'id': '5_workouts', 'name': '5 Workouts', 'description': 'Complete 5 workouts', 'icon': '💪', 'category': 'milestone', 'criteria_type': 'workout_count', 'criteria_value': 5, 'points': 50},
            {'id': '10_workouts', 'name': '10 Workouts', 'description': 'Complete 10 workouts', 'icon': '🔥', 'category': 'milestone', 'criteria_type': 'workout_count', 'criteria_value': 10, 'points': 100},
            {'id': '50_workouts', 'name': '50 Workouts', 'description': 'Complete 50 workouts', 'icon': '🏆', 'category': 'milestone', 'criteria_type': 'workout_count', 'criteria_value': 50, 'points': 500},
            {'id': '100_workouts', 'name': 'Century Club', 'description': 'Complete 100 workouts', 'icon': '👑', 'category': 'milestone', 'criteria_type': 'workout_count', 'criteria_value': 100, 'points': 1000},

            # Calorie achievements
            {'id': '1k_calories_burned', 'name': '1K Calories Burned', 'description': 'Burn 1,000 calories total', 'icon': '🔥', 'category': 'volume', 'criteria_type': 'total_calories_burned', 'criteria_value': 1000, 'points': 100},
            {'id': '5k_calories_burned', 'name': '5K Calories Burned', 'description': 'Burn 5,000 calories total', 'icon': '🔥🔥', 'category': 'volume', 'criteria_type': 'total_calories_burned', 'criteria_value': 5000, 'points': 500},
            {'id': '10k_calories_burned', 'name': '10K Calories Burned', 'description': 'Burn 10,000 calories total', 'icon': '🔥🔥🔥', 'category': 'volume', 'criteria_type': 'total_calories_burned', 'criteria_value': 10000, 'points': 1000},

            # Streak achievements
            {'id': '7_day_streak', 'name': '7 Day Streak', 'description': 'Log activity 7 days in a row', 'icon': '📅', 'category': 'streak', 'criteria_type': 'streak_days', 'criteria_value': 7, 'points': 200},
            {'id': '30_day_streak', 'name': '30 Day Streak', 'description': 'Log activity 30 days in a row', 'icon': '🗓️', 'category': 'streak', 'criteria_type': 'streak_days', 'criteria_value': 30, 'points': 1000},
            {'id': '100_day_streak', 'name': '100 Day Streak', 'description': 'Log activity 100 days in a row', 'icon': '🏅', 'category': 'streak', 'criteria_type': 'streak_days', 'criteria_value': 100, 'points': 5000},

            # Special achievements
            {'id': 'early_bird', 'name': 'Early Bird', 'description': 'Complete a workout before 7 AM', 'icon': '🌅', 'category': 'special', 'criteria_type': 'early_workout', 'criteria_value': 1, 'points': 50},
            {'id': 'night_owl', 'name': 'Night Owl', 'description': 'Complete a workout after 9 PM', 'icon': '🌙', 'category': 'special', 'criteria_type': 'late_workout', 'criteria_value': 1, 'points': 50},
            {'id': 'perfect_week', 'name': 'Perfect Week', 'description': 'Hit your calorie goal every day for a week', 'icon': '⭐', 'category': 'special', 'criteria_type': 'perfect_week', 'criteria_value': 1, 'points': 300},

            # Food logging achievements
            {'id': '100_meals_logged', 'name': '100 Meals Logged', 'description': 'Log 100 meals', 'icon': '🍽️', 'category': 'milestone', 'criteria_type': 'food_log_count', 'criteria_value': 100, 'points': 200},
            {'id': '500_meals_logged', 'name': '500 Meals Logged', 'description': 'Log 500 meals', 'icon': '📊', 'category': 'milestone', 'criteria_type': 'food_log_count', 'criteria_value': 500, 'points': 1000},
        ]

    def _check_achievement_criteria(
        self,
        achievement: Dict,
        user_stats: Dict,
        recent_activity: Optional[Dict]
    ) -> bool:
        """Check if achievement criteria is met"""

        criteria_type = achievement['criteria_type']
        criteria_value = achievement['criteria_value']

        # Check different criteria types
        if criteria_type == 'workout_count':
            return user_stats.get('total_workouts', 0) >= criteria_value

        elif criteria_type == 'total_calories_burned':
            return user_stats.get('total_calories_burned', 0) >= criteria_value

        elif criteria_type == 'streak_days':
            return user_stats.get('current_streak_days', 0) >= criteria_value

        elif criteria_type == 'food_log_count':
            return user_stats.get('total_food_logs', 0) >= criteria_value

        elif criteria_type == 'early_workout':
            if recent_activity and recent_activity.get('type') == 'workout':
                workout_time = recent_activity.get('logged_at')
                if workout_time and workout_time.hour < 7:
                    return True

        elif criteria_type == 'late_workout':
            if recent_activity and recent_activity.get('type') == 'workout':
                workout_time = recent_activity.get('logged_at')
                if workout_time and workout_time.hour >= 21:
                    return True

        elif criteria_type == 'perfect_week':
            return user_stats.get('perfect_weeks', 0) >= criteria_value

        return False

    # ==================== LEADERBOARD & SOCIAL ====================

    def get_user_rank(self, user_xp: int, all_users_xp: List[int]) -> Tuple[int, int]:
        """
        Get user's rank among all users

        Args:
            user_xp: User's total XP
            all_users_xp: List of all users' XP

        Returns:
            Tuple of (rank, percentile)
        """

        sorted_xp = sorted(all_users_xp, reverse=True)
        rank = sorted_xp.index(user_xp) + 1 if user_xp in sorted_xp else len(sorted_xp) + 1
        percentile = int((1 - (rank - 1) / len(sorted_xp)) * 100) if sorted_xp else 0

        return rank, percentile


# Test function
if __name__ == '__main__':
    print("Gamification Service")
    print("=" * 60)

    service = GamificationService()
    print("✅ Gamification service initialized")

    # Test streak update
    print("\n🔥 Testing streak update:")
    streak = service.update_streak(
        user_id=1,
        streak_type='workout',
        activity_date=date.today(),
        current_streak_data={'current_streak_days': 6, 'longest_streak_days': 10, 'last_activity_date': date.today() - timedelta(days=1)}
    )
    print(f"   Streak: {streak['current_streak_days']} days")
    print(f"   Message: {service.get_streak_message(streak)}")

    # Test XP and leveling
    print("\n⭐ Testing XP and leveling:")
    level_data = {
        'current_level': 5,
        'current_xp': 80,
        'xp_for_next_level': 100,
        'total_xp_earned': 500
    }
    xp_result = service.award_xp(1, 50, 'workout', level_data)
    print(f"   Level: {xp_result['current_level']}")
    print(f"   XP: {xp_result['current_xp']} / {xp_result['xp_for_next_level']}")
    if xp_result['leveled_up']:
        print(f"   🎉 LEVEL UP! New title: {xp_result['new_title']}")

    # Test achievement checking
    print("\n🏆 Testing achievement checking:")
    user_stats = {
        'total_workouts': 10,
        'total_calories_burned': 5500,
        'current_streak_days': 7
    }
    achievements = service.check_achievements(1, user_stats)
    print(f"   Unlocked {len(achievements)} achievements:")
    for ach in achievements:
        print(f"   - {ach['icon']} {ach['name']}")

    print("\n✅ Gamification service ready!")
