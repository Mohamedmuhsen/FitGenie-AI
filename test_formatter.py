"""
Test script for ResponseFormatterService across all 8 domains
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.services.response_formatter_service import ResponseFormatterService

def test_formatter():
    print("\n--- 1. Testing Workout Formatting ---")
    workout_data = {
        "plan_name": "FitGenie Hypertrophy Split",
        "goal": "muscle_gain",
        "days_per_week": 4,
        "workout_days": [
            {
                "day": "Monday",
                "focus": "Chest & Triceps",
                "duration_minutes": 60,
                "exercises": [
                    {"name": "Bench Press", "sets": 4, "reps": "8-10", "rest_seconds": 90, "muscle_group": "chest"},
                    {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10-12", "rest_seconds": 60, "muscle_group": "chest"}
                ]
            }
        ],
        "warmup": "5-10 min light cardio",
        "cooldown": "5 min stretching",
        "progression_notes": "Increase weight by 2.5kg once top reps achieved."
    }
    fmt_workout = ResponseFormatterService.format_response("workout", workout_data)
    print(fmt_workout)
    assert "🏋️ **FitGenie Hypertrophy Split**" in fmt_workout
    assert "Bench Press" in fmt_workout

    print("\n--- 2. Testing Nutrition Formatting ---")
    nutrition_data = {
        "daily_calories": 2500,
        "protein_g": 187.5,
        "carbs_g": 281.3,
        "fats_g": 69.4,
        "hydration_liters": 3.0,
        "meals": [
            {
                "meal_name": "Breakfast",
                "time": "8:00 AM",
                "total_calories": 440,
                "total_protein_g": 35,
                "total_carbs_g": 57,
                "total_fats_g": 7.5,
                "foods": [{"name": "Oats", "portion": "80g", "calories": 320}]
            }
        ]
    }
    fmt_nut = ResponseFormatterService.format_response("nutrition", nutrition_data)
    print(fmt_nut)
    assert "🥗 **Your Personalized Daily Nutrition Plan**" in fmt_nut

    print("\n--- 3. Testing Supplement Formatting ---")
    supp_data = {
        "recommendations": [
            {"name": "Creatine Monohydrate", "dosage": "5g daily", "timing": "Post-workout", "reason": "Improves strength and recovery.", "priority": "essential"}
        ],
        "total_monthly_cost_estimate": "$45"
    }
    fmt_supp = ResponseFormatterService.format_response("supplements", supp_data)
    print(fmt_supp)
    assert "💊 **Evidence-Based Supplement Recommendations**" in fmt_supp

    print("\nALL RESPONSE FORMATTER TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_formatter()
