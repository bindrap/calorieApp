#!/usr/bin/env python3
"""
AI Meal Suggestion Engine
Recommends meals to help users hit their macro targets based on remaining calories/macros
"""

import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime, time


class MealSuggestionEngine:
    """
    AI-powered meal suggestion system
    Analyzes user's current macro status and suggests optimal meals
    """

    def __init__(self):
        self.api_url = os.environ.get('OLLAMA_API_URL', 'https://api.ollamacloud.ai/v1/chat/completions')
        self.api_key = os.environ.get('OLLAMA_API_KEY', '')
        self.model = os.environ.get('OLLAMA_MODEL', 'gpt-oss:120b')

    def suggest_meal(
        self,
        remaining_calories: float,
        remaining_protein: float,
        remaining_carbs: float,
        remaining_fat: float,
        meal_type: str = 'any',
        dietary_restrictions: Optional[List[str]] = None,
        preferences: Optional[Dict] = None
    ) -> Dict:
        """
        Generate meal suggestions based on remaining macros

        Args:
            remaining_calories: Calories left to consume today
            remaining_protein: Protein (g) left to consume
            remaining_carbs: Carbs (g) left to consume
            remaining_fat: Fat (g) left to consume
            meal_type: 'breakfast', 'lunch', 'dinner', 'snack', 'pre_workout', 'post_workout'
            dietary_restrictions: List of restrictions ['vegetarian', 'vegan', 'gluten_free', 'dairy_free', 'keto']
            preferences: User preferences (liked foods, disliked foods, etc.)

        Returns:
            Dict containing meal suggestions
        """

        print(f"🤖 Generating {meal_type} suggestions...")
        print(f"   Remaining: {remaining_calories} cal, {remaining_protein}g protein, {remaining_carbs}g carbs, {remaining_fat}g fat")

        # Build prompt
        prompt = self._build_suggestion_prompt(
            remaining_calories, remaining_protein, remaining_carbs, remaining_fat,
            meal_type, dietary_restrictions, preferences
        )

        # Call AI
        response = self._call_ai(prompt)

        # Parse response
        result = self._parse_suggestion_response(response, meal_type)

        return result

    def suggest_meal_for_time_of_day(
        self,
        current_time: time,
        remaining_macros: Dict,
        user_preferences: Dict
    ) -> Dict:
        """
        Suggest meal based on current time of day

        Args:
            current_time: Current time
            remaining_macros: Dict with remaining calories/macros
            user_preferences: User preferences and restrictions

        Returns:
            Contextual meal suggestion
        """

        hour = current_time.hour

        # Determine meal type from time
        if 5 <= hour < 11:
            meal_type = 'breakfast'
        elif 11 <= hour < 15:
            meal_type = 'lunch'
        elif 15 <= hour < 18:
            meal_type = 'snack'
        elif 18 <= hour < 23:
            meal_type = 'dinner'
        else:
            meal_type = 'snack'

        return self.suggest_meal(
            remaining_macros['calories'],
            remaining_macros['protein'],
            remaining_macros['carbs'],
            remaining_macros['fat'],
            meal_type=meal_type,
            dietary_restrictions=user_preferences.get('restrictions', []),
            preferences=user_preferences
        )

    def suggest_workout_nutrition(
        self,
        workout_type: str,
        workout_time: str,  # 'before' or 'after'
        remaining_macros: Dict
    ) -> Dict:
        """
        Suggest pre/post-workout nutrition

        Args:
            workout_type: Type of workout (strength, cardio, etc.)
            workout_time: 'before' or 'after' workout
            remaining_macros: Remaining macros for the day

        Returns:
            Workout-specific meal suggestion
        """

        if workout_time == 'before':
            meal_type = 'pre_workout'
            focus = 'carbs_and_moderate_protein'
        else:
            meal_type = 'post_workout'
            focus = 'protein_and_carbs' if workout_type == 'strength' else 'carbs_and_protein'

        # Add workout context to prompt
        prompt = f"""
🏋️ WORKOUT NUTRITION SUGGESTION

Workout Type: {workout_type}
Timing: {workout_time} workout
Focus: {focus}

Remaining Macros:
- Calories: {remaining_macros['calories']}
- Protein: {remaining_macros['protein']}g
- Carbs: {remaining_macros['carbs']}g
- Fat: {remaining_macros['fat']}g

Suggest an optimal {meal_type} meal that:
1. Supports {workout_type} training
2. Fits within remaining macros
3. Is appropriate for {workout_time} workout timing

Respond with JSON format:
```json
{{
    "primary_suggestion": {{
        "meal": "meal name",
        "foods": ["food 1", "food 2"],
        "calories": 400,
        "protein": 30,
        "carbs": 45,
        "fat": 10,
        "timing": "30-60 minutes before workout",
        "reasoning": "why this meal is optimal"
    }},
    "alternatives": [...]
}}
```
"""

        response = self._call_ai(prompt)
        return self._parse_suggestion_response(response, meal_type)

    def _build_suggestion_prompt(
        self,
        remaining_calories: float,
        remaining_protein: float,
        remaining_carbs: float,
        remaining_fat: float,
        meal_type: str,
        dietary_restrictions: Optional[List[str]],
        preferences: Optional[Dict]
    ) -> str:
        """Build AI prompt for meal suggestions"""

        prompt = f"""🍽️ SMART MEAL SUGGESTION

You are a nutrition AI assistant helping users hit their macro targets. Suggest meals that fit their remaining nutritional needs.

REMAINING MACROS (target to hit):
- Calories: {remaining_calories} cal
- Protein: {remaining_protein}g
- Carbohydrates: {remaining_carbs}g
- Fat: {remaining_fat}g

MEAL TYPE: {meal_type}
"""

        # Add dietary restrictions
        if dietary_restrictions:
            prompt += f"\nDIETARY RESTRICTIONS:\n"
            for restriction in dietary_restrictions:
                prompt += f"- {restriction}\n"

        # Add preferences
        if preferences:
            if 'liked_foods' in preferences:
                prompt += f"\nLIKED FOODS: {', '.join(preferences['liked_foods'])}\n"
            if 'disliked_foods' in preferences:
                prompt += f"\nAVOID: {', '.join(preferences['disliked_foods'])}\n"
            if 'cuisine_preferences' in preferences:
                prompt += f"\nCUISINE PREFERENCES: {', '.join(preferences['cuisine_preferences'])}\n"

        prompt += """
YOUR TASK:
1. Suggest 1 PRIMARY meal that best fits the remaining macros
2. Provide 2-3 ALTERNATIVE options
3. Each suggestion should:
   - Come close to using the remaining macros efficiently
   - Be realistic and easy to prepare
   - Consider the meal type (breakfast suggestions should be breakfast foods)
   - Be specific with portion sizes

OUTPUT FORMAT (respond with valid JSON):
```json
{
    "primary_suggestion": {
        "meal_name": "Grilled Chicken with Rice and Broccoli",
        "description": "6oz grilled chicken breast, 1 cup white rice, 1 cup steamed broccoli, 1 tbsp olive oil",
        "foods": [
            {"name": "Grilled chicken breast", "amount": "6 oz (170g)"},
            {"name": "White rice", "amount": "1 cup cooked (150g)"},
            {"name": "Steamed broccoli", "amount": "1 cup (90g)"},
            {"name": "Olive oil", "amount": "1 tbsp"}
        ],
        "predicted_nutrition": {
            "calories": 580,
            "protein": 55,
            "carbs": 48,
            "fat": 15
        },
        "macro_fit_score": 0.92,
        "reasoning": "High protein to meet remaining goal, balanced carbs, controlled fat. Simple to prepare.",
        "prep_time_minutes": 20,
        "difficulty": "easy"
    },
    "alternatives": [
        {
            "meal_name": "Salmon with Sweet Potato",
            "description": "5oz baked salmon, 1 medium sweet potato, side salad",
            "foods": [...],
            "predicted_nutrition": {...},
            "macro_fit_score": 0.88,
            "reasoning": "Omega-3 rich, good carb source, lighter option"
        },
        {
            "meal_name": "Turkey Sandwich with Fruit",
            "description": "Turkey sandwich on whole wheat with apple",
            "foods": [...],
            "predicted_nutrition": {...},
            "macro_fit_score": 0.85,
            "reasoning": "Quick and convenient, balanced macros"
        }
    ],
    "tips": [
        "Meal prep the rice ahead of time to save time",
        "Can substitute chicken with turkey or fish"
    ]
}
```

IMPORTANT RULES:
✅ DO:
- Suggest REAL, specific meals with exact portions
- Calculate nutrition accurately
- Consider meal timing (breakfast vs dinner foods)
- Respect dietary restrictions
- Prioritize macro fit (especially protein if high remaining)
- Include meal prep tips

❌ DON'T:
- Suggest vague meals like "protein and veggies"
- Exceed remaining macros significantly
- Ignore dietary restrictions
- Suggest overly complex recipes
- Recommend rare/exotic ingredients

Begin your suggestion now:
"""

        return prompt

    def _call_ai(self, prompt: str) -> str:
        """Call AI API"""

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a professional nutritionist AI assistant specializing in meal planning and macro tracking.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 2000,
            'temperature': 0.7  # Some creativity for variety
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            return content

        except Exception as e:
            print(f"❌ AI API error: {e}")
            return self._get_fallback_suggestion()

    def _parse_suggestion_response(self, response: str, meal_type: str) -> Dict:
        """Parse AI response into structured suggestions"""

        try:
            # Extract JSON
            if '```json' in response:
                json_start = response.find('```json') + 7
                json_end = response.find('```', json_start)
                json_str = response[json_start:json_end].strip()
            elif '```' in response:
                json_start = response.find('```') + 3
                json_end = response.find('```', json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response

            data = json.loads(json_str)

            result = {
                'primary_suggestion': data.get('primary_suggestion', {}),
                'alternatives': data.get('alternatives', []),
                'tips': data.get('tips', []),
                'meal_type': meal_type,
                'generated_at': datetime.utcnow().isoformat(),
                'raw_response': response
            }

            primary = result['primary_suggestion']
            print(f"✅ Suggested: {primary.get('meal_name', 'Unknown')}")
            print(f"   {primary.get('predicted_nutrition', {}).get('calories', 0)} cal, "
                  f"{primary.get('predicted_nutrition', {}).get('protein', 0)}g protein")

            return result

        except Exception as e:
            print(f"❌ Error parsing suggestion: {e}")
            return self._get_fallback_result()

    def _get_fallback_suggestion(self) -> str:
        """Fallback JSON suggestion"""
        return json.dumps({
            'primary_suggestion': {
                'meal_name': 'Grilled Chicken with Vegetables',
                'description': '6oz chicken breast, mixed vegetables, 1 cup rice',
                'foods': [
                    {'name': 'Grilled chicken breast', 'amount': '6 oz'},
                    {'name': 'Mixed vegetables', 'amount': '2 cups'},
                    {'name': 'White rice', 'amount': '1 cup cooked'}
                ],
                'predicted_nutrition': {
                    'calories': 500,
                    'protein': 50,
                    'carbs': 50,
                    'fat': 10
                },
                'macro_fit_score': 0.8,
                'reasoning': 'Balanced meal with lean protein and vegetables',
                'prep_time_minutes': 25,
                'difficulty': 'easy'
            },
            'alternatives': [],
            'tips': ['API error - showing fallback suggestion']
        })

    def _get_fallback_result(self) -> Dict:
        """Fallback result structure"""
        return {
            'primary_suggestion': {},
            'alternatives': [],
            'tips': [],
            'meal_type': 'unknown',
            'generated_at': datetime.utcnow().isoformat(),
            'error': True
        }


class AdaptiveCalorieTargetCalculator:
    """
    Calculate adaptive calorie targets based on recovery data, sleep, and activity
    """

    def calculate_adaptive_target(
        self,
        base_calorie_goal: int,
        sleep_data: Optional[Dict] = None,
        recovery_score: Optional[int] = None,
        recent_activity_level: Optional[str] = None,
        stress_level: Optional[int] = None
    ) -> Dict:
        """
        Calculate adjusted calorie target based on recovery metrics

        Args:
            base_calorie_goal: User's standard daily calorie goal
            sleep_data: Dict with sleep metrics (duration, quality, etc.)
            recovery_score: 0-100 recovery score (from wearable)
            recent_activity_level: 'low', 'moderate', 'high'
            stress_level: 1-10 stress level

        Returns:
            Dict with adjusted target and reasoning
        """

        adjustment_factor = 1.0
        adjustments = []

        # Sleep quality adjustment
        if sleep_data:
            sleep_duration = sleep_data.get('total_duration_minutes', 480) / 60  # hours
            sleep_quality = sleep_data.get('sleep_score', 75)

            if sleep_duration < 6:
                # Poor sleep = lower target (fatigue, harder to burn calories)
                adjustment_factor *= 0.95
                adjustments.append(f"Sleep duration low ({sleep_duration:.1f}h): -5%")
            elif sleep_duration < 7:
                adjustment_factor *= 0.98
                adjustments.append(f"Sleep duration suboptimal ({sleep_duration:.1f}h): -2%")

            if sleep_quality < 60:
                adjustment_factor *= 0.97
                adjustments.append(f"Poor sleep quality ({sleep_quality}/100): -3%")

        # Recovery score adjustment
        if recovery_score is not None:
            if recovery_score >= 80:
                # Well recovered = can eat more (training capacity high)
                adjustment_factor *= 1.05
                adjustments.append(f"Excellent recovery ({recovery_score}/100): +5%")
            elif recovery_score < 50:
                # Poor recovery = reduce intake
                adjustment_factor *= 0.95
                adjustments.append(f"Low recovery ({recovery_score}/100): -5%")

        # Activity level adjustment
        if recent_activity_level:
            if recent_activity_level == 'high':
                adjustment_factor *= 1.08
                adjustments.append("High recent activity: +8%")
            elif recent_activity_level == 'low':
                adjustment_factor *= 0.95
                adjustments.append("Low recent activity: -5%")

        # Stress level adjustment
        if stress_level is not None:
            if stress_level >= 8:
                # High stress = lower target (cortisol, poor recovery)
                adjustment_factor *= 0.96
                adjustments.append(f"High stress level ({stress_level}/10): -4%")

        # Calculate adjusted target
        adjusted_target = int(base_calorie_goal * adjustment_factor)
        adjustment_calories = adjusted_target - base_calorie_goal

        return {
            'base_target': base_calorie_goal,
            'adjusted_target': adjusted_target,
            'adjustment_calories': adjustment_calories,
            'adjustment_percent': round((adjustment_factor - 1) * 100, 1),
            'adjustments': adjustments,
            'recommendation': self._get_recommendation(adjustment_factor)
        }

    def _get_recommendation(self, adjustment_factor: float) -> str:
        """Get recommendation based on adjustment"""
        if adjustment_factor >= 1.05:
            return "Your body is well-recovered! Fuel your training with adequate nutrition."
        elif adjustment_factor <= 0.95:
            return "Focus on recovery today. Consider a slight calorie reduction and prioritize sleep."
        else:
            return "Maintain your usual nutrition plan."


# Test function
if __name__ == '__main__':
    print("AI Meal Suggestion Engine")
    print("=" * 60)

    engine = MealSuggestionEngine()
    print("✅ Meal suggestion engine initialized")

    calculator = AdaptiveCalorieTargetCalculator()
    print("✅ Adaptive calorie calculator initialized")

    # Test adaptive target calculation
    print("\n📊 Testing adaptive calorie target:")
    result = calculator.calculate_adaptive_target(
        base_calorie_goal=3000,
        sleep_data={'total_duration_minutes': 420, 'sleep_score': 72},
        recovery_score=65,
        recent_activity_level='moderate',
        stress_level=6
    )
    print(f"   Base target: {result['base_target']} cal")
    print(f"   Adjusted target: {result['adjusted_target']} cal ({result['adjustment_calories']:+d} cal)")
    print(f"   Adjustments: {', '.join(result['adjustments'])}")

    print("\n✅ All systems operational!")
