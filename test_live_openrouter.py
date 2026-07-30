"""
Live OpenRouter Agent Verification Script
"""
import sys
import logging
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logging.basicConfig(level=logging.INFO)

from app.config.settings import get_settings
from app.config.llm_config import get_llm
from app.crews.fitness_crew import FitnessCrew

def verify_live_agents():
    print("\n=======================================================")
    print("        VERIFYING LIVE OPENROUTER AGENT EXECUTION        ")
    print("=======================================================")
    
    settings = get_settings()
    print(f"Loaded Key Masked: {settings.get_masked_api_key()}")
    print(f"Model: {settings.LLM_MODEL}")
    print(f"Base URL: {settings.LLM_BASE_URL}")
    print(f"Has Valid API Key: {settings.has_valid_api_key()}")

    assert settings.has_valid_api_key(), "API key validation failed!"

    # Instantiate LLM instance
    llm = get_llm()
    print(f"[OK] Instantiated CrewAI LLM: {llm.model}")

    # Test Assessment Agent Crew live kickoff
    user_payload = {
        "age": 25,
        "gender": "male",
        "weight_kg": 75,
        "height_cm": 175,
        "goal": "muscle_gain",
        "experience_level": "intermediate",
        "workout_days_per_week": 4
    }

    print("\n--- Testing Live Assessment Crew Kickoff ---")
    crew = FitnessCrew.assessment_crew(user_payload)
    print("Calling crew.kickoff()...")
    res = crew.kickoff()
    print("\n[SUCCESS] Live OpenRouter Agent Response Received!")
    print(f"Response snippet:\n{str(res)[:300]}...")

if __name__ == "__main__":
    verify_live_agents()
