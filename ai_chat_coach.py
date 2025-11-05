#!/usr/bin/env python3
"""
AI Chat Coach System
Natural language food/workout logging and personalized nutrition coaching
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Set API key BEFORE importing ollama
os.environ['OLLAMA_API_KEY'] = os.environ.get('OLLAMA_API_KEY', 'fe0c789532b44e988904c67a8bae43bd.s4tncu8N0QrXikNECVubiWGg')

import ollama


class AIChatCoach:
    """
    AI-powered chat coach for conversational food logging and nutrition advice
    """

    def __init__(self):
        # Use Ollama Cloud - API key already set in environment
        self.model = 'gpt-oss:120b-cloud'

        # Conversation history (in production, load from database)
        self.conversation_history = []

    def process_message(
        self,
        user_message: str,
        user_context: Optional[Dict] = None
    ) -> Dict:
        """
        Process user message and determine intent + extract data

        Args:
            user_message: User's message
            user_context: Current user context (today's macros, goals, etc.)

        Returns:
            Dict containing response, intent, and extracted data
        """

        print(f"💬 Processing message: {user_message[:100]}...")

        # Detect intent
        intent = self._detect_intent(user_message)

        # Route to appropriate handler
        if intent == 'log_food':
            return self._handle_food_logging(user_message, user_context)
        elif intent == 'log_workout':
            return self._handle_workout_logging(user_message, user_context)
        elif intent == 'ask_nutrition':
            return self._handle_nutrition_question(user_message, user_context)
        elif intent == 'get_advice':
            return self._handle_advice_request(user_message, user_context)
        elif intent == 'check_progress':
            return self._handle_progress_check(user_message, user_context)
        elif intent == 'meal_suggestion':
            return self._handle_meal_suggestion(user_message, user_context)
        else:
            return self._handle_general_conversation(user_message, user_context)

    def _detect_intent(self, message: str) -> str:
        """
        Detect user's intent from message

        Returns:
            Intent string: 'log_food', 'log_workout', 'ask_nutrition', 'get_advice', 'check_progress', 'meal_suggestion', 'general'
        """

        message_lower = message.lower()

        # Food logging patterns
        food_patterns = [
            r'\b(ate|eat|eating|had|consumed|lunch|dinner|breakfast|meal|snack)\b',
            r'\b(calories|protein|carbs|fat)\b.*\b(how many|how much)\b',
            r'\bjust (ate|had)\b',
            r'\b(log|track|add|record).*\b(food|meal)\b'
        ]

        # Workout logging patterns
        workout_patterns = [
            r'\b(workout|exercise|trained|gym|ran|run|lift|lifted)\b',
            r'\b(jiu jitsu|boxing|swimming|cycling|yoga)\b',
            r'\b(log|track|add|record).*\b(workout|exercise)\b',
            r'\bdid\s+\d+\s+(minutes|min|hours|hr)\b'
        ]

        # Question patterns
        question_patterns = [
            r'\b(what|why|how|when|should|can|is|are)\b',
            r'\?$'
        ]

        # Advice patterns
        advice_patterns = [
            r'\b(help|advice|suggest|recommend|tips)\b',
            r'\bwhat should i\b',
            r'\bhow can i\b'
        ]

        # Progress check patterns
        progress_patterns = [
            r'\b(progress|status|summary|today|week|stats)\b',
            r'\bhow (am i|did i) (do|doing)\b',
            r'\b(remaining|left|still need)\b'
        ]

        # Meal suggestion patterns
        suggestion_patterns = [
            r'\bwhat (should|can) i eat\b',
            r'\bmeal (ideas|suggestions)\b',
            r'\b(hungry|need to eat)\b'
        ]

        # Check patterns in order of specificity
        for pattern in food_patterns:
            if re.search(pattern, message_lower):
                return 'log_food'

        for pattern in workout_patterns:
            if re.search(pattern, message_lower):
                return 'log_workout'

        for pattern in suggestion_patterns:
            if re.search(pattern, message_lower):
                return 'meal_suggestion'

        for pattern in progress_patterns:
            if re.search(pattern, message_lower):
                return 'check_progress'

        for pattern in question_patterns:
            if re.search(pattern, message_lower):
                return 'ask_nutrition'

        for pattern in advice_patterns:
            if re.search(pattern, message_lower):
                return 'get_advice'

        return 'general'

    def _handle_food_logging(self, message: str, context: Optional[Dict]) -> Dict:
        """Handle food logging requests"""

        print("🍽️ Handling food logging request...")

        # Extract food information using AI
        prompt = f"""You are a nutrition AI assistant. Extract food information from the user's message and format it as structured data.

User message: "{message}"

Extract the following information:
1. Food items mentioned
2. Quantities/portions if mentioned
3. Meal type (breakfast, lunch, dinner, snack)
4. Time if mentioned

Respond with JSON:
```json
{{
    "foods": [
        {{
            "name": "food name",
            "quantity": "quantity description",
            "estimated_grams": 150
        }}
    ],
    "meal_type": "lunch",
    "meal_time": "12:30 PM or null",
    "confidence": 0.85,
    "needs_clarification": false,
    "clarification_question": "Did you mean X or Y?"
}}
```
"""

        # Call AI to extract food data
        extracted_data = self._call_ai_for_extraction(prompt)

        # Check if clarification is needed
        if extracted_data.get('needs_clarification'):
            return {
                'intent': 'log_food',
                'status': 'needs_clarification',
                'response': extracted_data.get('clarification_question', 'Could you provide more details about what you ate?'),
                'extracted_data': extracted_data
            }

        # Estimate nutrition (in production, integrate with actual calorie calculator)
        estimated_nutrition = self._estimate_nutrition_from_extracted_data(extracted_data)

        # Build response
        foods_text = ', '.join([f"{food['name']} ({food.get('quantity', 'unknown amount')})" for food in extracted_data.get('foods', [])])

        response = f"Got it! I'll log: {foods_text}\n\n"
        response += f"Estimated nutrition:\n"
        response += f"• Calories: {estimated_nutrition['calories']} cal\n"
        response += f"• Protein: {estimated_nutrition['protein']}g\n"
        response += f"• Carbs: {estimated_nutrition['carbs']}g\n"
        response += f"• Fat: {estimated_nutrition['fat']}g\n\n"

        if context:
            remaining = context.get('remaining', {})
            new_remaining_cals = remaining.get('calories', 0) - estimated_nutrition['calories']
            response += f"Remaining today: {new_remaining_cals} calories\n"

        response += "\nReply 'confirm' to log this, or 'cancel' to discard."

        return {
            'intent': 'log_food',
            'status': 'pending_confirmation',
            'response': response,
            'extracted_data': extracted_data,
            'estimated_nutrition': estimated_nutrition,
            'action_required': 'confirmation'
        }

    def _handle_workout_logging(self, message: str, context: Optional[Dict]) -> Dict:
        """Handle workout logging requests"""

        print("💪 Handling workout logging request...")

        prompt = f"""You are a fitness AI assistant. Extract workout information from the user's message.

User message: "{message}"

Extract:
1. Activity type
2. Duration
3. Intensity
4. Distance if mentioned
5. Additional details

Respond with JSON:
```json
{{
    "activity_type": "Running",
    "duration_minutes": 30,
    "intensity": "moderate",
    "distance_km": 5.0,
    "additional_details": "outdoor, felt good",
    "confidence": 0.9,
    "needs_clarification": false
}}
```
"""

        extracted_data = self._call_ai_for_extraction(prompt)

        # Estimate calories burned (in production, use actual MET calculations)
        estimated_calories = self._estimate_calories_burned(extracted_data, context)

        response = f"Awesome! I'll log your workout:\n\n"
        response += f"• Activity: {extracted_data.get('activity_type', 'Unknown')}\n"
        response += f"• Duration: {extracted_data.get('duration_minutes', 0)} minutes\n"
        response += f"• Intensity: {extracted_data.get('intensity', 'moderate')}\n"
        if extracted_data.get('distance_km'):
            response += f"• Distance: {extracted_data.get('distance_km')} km\n"
        response += f"\nEstimated calories burned: ~{estimated_calories} cal\n"

        if context:
            new_net_cals = context.get('consumed_today', 0) - estimated_calories
            response += f"Net calories today: {new_net_cals} cal\n"

        response += "\nReply 'confirm' to log this workout."

        return {
            'intent': 'log_workout',
            'status': 'pending_confirmation',
            'response': response,
            'extracted_data': extracted_data,
            'estimated_calories': estimated_calories,
            'action_required': 'confirmation'
        }

    def _handle_nutrition_question(self, message: str, context: Optional[Dict]) -> Dict:
        """Handle nutrition-related questions"""

        print("❓ Handling nutrition question...")

        # Build context-aware prompt
        context_str = ""
        if context:
            context_str = f"""
User's current status:
- Consumed today: {context.get('consumed_today', 0)} calories
- Remaining: {context.get('remaining', {}).get('calories', 0)} calories
- Goals: {context.get('goals', {})}
"""

        prompt = f"""You are a professional nutritionist AI. Answer the user's nutrition question accurately and helpfully.

{context_str}

User question: "{message}"

Provide a clear, accurate, and helpful answer. Include specific numbers when relevant.
"""

        response = self._call_ai_simple(prompt)

        return {
            'intent': 'ask_nutrition',
            'status': 'answered',
            'response': response,
            'action_required': None
        }

    def _handle_advice_request(self, message: str, context: Optional[Dict]) -> Dict:
        """Handle requests for nutrition/fitness advice"""

        print("💡 Handling advice request...")

        context_str = self._build_context_string(context)

        prompt = f"""You are a nutrition and fitness coach AI. Provide personalized advice based on the user's request and current progress.

{context_str}

User request: "{message}"

Provide actionable, personalized advice. Be specific and supportive.
"""

        response = self._call_ai_simple(prompt)

        return {
            'intent': 'get_advice',
            'status': 'provided',
            'response': response,
            'action_required': None
        }

    def _handle_progress_check(self, message: str, context: Optional[Dict]) -> Dict:
        """Handle progress check requests"""

        print("📊 Handling progress check...")

        if not context:
            return {
                'intent': 'check_progress',
                'status': 'no_data',
                'response': "I don't have your progress data loaded yet. Let me fetch that for you...",
                'action_required': 'fetch_user_data'
            }

        # Build progress summary
        consumed = context.get('consumed_today', {})
        goals = context.get('goals', {})
        remaining = context.get('remaining', {})

        response = f"📊 **Here's your progress today:**\n\n"
        response += f"**Consumed:**\n"
        response += f"• Calories: {consumed.get('calories', 0)} / {goals.get('calories', 0)} cal\n"
        response += f"• Protein: {consumed.get('protein', 0)} / {goals.get('protein', 0)}g\n"
        response += f"• Carbs: {consumed.get('carbs', 0)} / {goals.get('carbs', 0)}g\n"
        response += f"• Fat: {consumed.get('fat', 0)} / {goals.get('fat', 0)}g\n\n"

        response += f"**Remaining:**\n"
        response += f"• {remaining.get('calories', 0)} calories\n"
        response += f"• {remaining.get('protein', 0)}g protein\n"
        response += f"• {remaining.get('carbs', 0)}g carbs\n"
        response += f"• {remaining.get('fat', 0)}g fat\n\n"

        # Add motivational message based on progress
        if remaining.get('calories', 0) > 500:
            response += "💪 You're doing great! You still have plenty of room for another good meal."
        elif remaining.get('calories', 0) < 100:
            response += "🎯 You're right on track with your calorie goal!"
        else:
            response += "✅ Solid progress today. Keep it up!"

        return {
            'intent': 'check_progress',
            'status': 'provided',
            'response': response,
            'action_required': None
        }

    def _handle_meal_suggestion(self, message: str, context: Optional[Dict]) -> Dict:
        """Handle meal suggestion requests"""

        print("🍽️ Handling meal suggestion request...")

        if not context or not context.get('remaining'):
            return {
                'intent': 'meal_suggestion',
                'status': 'needs_context',
                'response': "Let me check your remaining macros first...",
                'action_required': 'fetch_user_data'
            }

        remaining = context.get('remaining', {})

        prompt = f"""You are a nutrition AI. Suggest a meal that fits the user's remaining macros.

Remaining macros:
- Calories: {remaining.get('calories', 0)} cal
- Protein: {remaining.get('protein', 0)}g
- Carbs: {remaining.get('carbs', 0)}g
- Fat: {remaining.get('fat', 0)}g

User request: "{message}"

Suggest 1-2 specific meal options with:
1. Food items and portions
2. Estimated nutrition
3. Why it's a good fit

Be practical and specific.
"""

        response = self._call_ai_simple(prompt)

        return {
            'intent': 'meal_suggestion',
            'status': 'suggested',
            'response': response,
            'action_required': None
        }

    def _handle_general_conversation(self, message: str, context: Optional[Dict]) -> Dict:
        """Handle general conversation"""

        print("💬 Handling general conversation...")

        prompt = f"""You are a friendly nutrition and fitness coach AI. Respond to the user's message in a helpful and supportive way.

User message: "{message}"

Keep it conversational and encouraging.
"""

        response = self._call_ai_simple(prompt)

        return {
            'intent': 'general',
            'status': 'responded',
            'response': response,
            'action_required': None
        }

    def _call_ai_for_extraction(self, prompt: str) -> Dict:
        """Call AI to extract structured data"""

        try:
            response_text = self._call_ai_simple(prompt)

            # Extract JSON from response
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                json_str = response_text

            data = json.loads(json_str)
            return data

        except Exception as e:
            print(f"❌ Error extracting data: {e}")
            return {'error': str(e), 'needs_clarification': True}

    def _call_ai_simple(self, prompt: str) -> str:
        """Simple AI call that returns text response using Ollama SDK"""

        try:
            # Use Ollama Cloud - simple approach
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )

            content = response['message']['content']
            return content

        except Exception as e:
            print(f"❌ AI API error: {e}")
            return "I'm having trouble processing your request right now. Please try again."

    def _estimate_nutrition_from_extracted_data(self, extracted_data: Dict) -> Dict:
        """Estimate nutrition from extracted food data (placeholder)"""
        # In production, integrate with actual calorie calculator
        return {
            'calories': 500,
            'protein': 30,
            'carbs': 50,
            'fat': 15
        }

    def _estimate_calories_burned(self, extracted_data: Dict, context: Optional[Dict]) -> int:
        """Estimate calories burned from workout (placeholder)"""
        # In production, use actual MET calculations
        duration = extracted_data.get('duration_minutes', 30)
        return int(duration * 8)  # Rough estimate

    def _build_context_string(self, context: Optional[Dict]) -> str:
        """Build context string for AI prompts"""
        if not context:
            return ""

        context_str = "User's current status:\n"
        if 'consumed_today' in context:
            context_str += f"- Consumed: {context['consumed_today'].get('calories', 0)} cal today\n"
        if 'goals' in context:
            context_str += f"- Daily goal: {context['goals'].get('calories', 0)} cal\n"
        if 'remaining' in context:
            context_str += f"- Remaining: {context['remaining'].get('calories', 0)} cal\n"

        return context_str


# Test function
if __name__ == '__main__':
    print("AI Chat Coach System")
    print("=" * 60)

    coach = AIChatCoach()
    print("✅ AI Chat Coach initialized")

    # Test intent detection
    test_messages = [
        "I just ate a chicken sandwich",
        "Did a 30 minute run",
        "What should I eat for dinner?",
        "How am I doing today?",
        "Is protein powder necessary?"
    ]

    print("\n🧪 Testing intent detection:")
    for msg in test_messages:
        intent = coach._detect_intent(msg)
        print(f"   '{msg}' → {intent}")

    print("\n✅ AI Chat Coach ready!")
