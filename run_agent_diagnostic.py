"""
Diagnostic Script to trace Agent & LLM Execution
"""
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.config.settings import get_settings
from app.crews.fitness_crew import FitnessCrew

def test_kickoff():
    print("\n==========================================")
    print("RUNNING AGENT KICKOFF DIAGNOSTIC")
    print("==========================================")
    settings = get_settings()
    print(f"LLM_MODEL: {settings.LLM_MODEL}")
    print(f"OPENROUTER_API_KEY in env: {os.environ.get('OPENROUTER_API_KEY')}")

    user_profile = {
        "age": 25,
        "gender": "male",
        "weight_kg": 75.0,
        "height_cm": 175.0,
        "goal": "muscle_gain",
        "experience_level": "intermediate",
        "workout_days_per_week": 4,
        "injuries": ["shoulder"]
    }

    print("\n--- 1. Testing Assessment Crew Kickoff ---")
    try:
        crew = FitnessCrew.assessment_crew(user_profile)
        print("Crew initialized successfully. Calling crew.kickoff()...")
        res = crew.kickoff()
        print(f"SUCCESS! Output:\n{res}")
    except Exception as e:
        print(f"CRASH / FAILURE: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_kickoff()
