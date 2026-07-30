"""
End-to-End Test Suite for All 7 FitGenie AI Scenarios
"""
import json
import logging
from fastapi.testclient import TestClient
from app.main import app

logging.basicConfig(level=logging.INFO)
client = TestClient(app)

def run_tests():
    print("\n========================================================")
    print("      FITGENIE AI END-TO-END SCENARIO VALIDATION        ")
    print("========================================================")

    # 1. GET / & GET /health
    r = client.get("/health")
    assert r.status_code == 200
    print("[PASS] GET /health -> 200 OK")

    r = client.get("/api")
    assert r.status_code == 200
    print(f"[PASS] GET /api -> {r.json()['message']} (API Key Status: {r.json()['api_key_configured']})")

    # Scenario 1: Workout Plan
    print("\n--- Scenario 1: Workout Plan (/workout) ---")
    payload_workout = {
        "goal": "muscle_gain",
        "experience_level": "intermediate",
        "workout_days_per_week": 4
    }
    r = client.post("/workout", json=payload_workout)
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "success"
    assert "🏋️" in res["response"] or "Workout" in res["response"]
    assert "workout_days" in res["data"]
    print("[PASS] Workout Plan scenario produced formatted presentation text & internal structured data!")

    # Scenario 2: Nutrition Plan
    print("\n--- Scenario 2: Nutrition Plan (/nutrition) ---")
    payload_nutrition = {
        "daily_calories": 2600,
        "goal": "muscle_gain"
    }
    r = client.post("/nutrition", json=payload_nutrition)
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "success"
    assert "🥗" in res["response"] or "Nutrition" in res["response"]
    assert "meals" in res["data"]
    print("[PASS] Nutrition Plan scenario produced formatted presentation text & internal structured data!")

    # Scenario 3: Supplements
    print("\n--- Scenario 3: Supplements (/supplements) ---")
    payload_supps = {
        "assessment": {"goal": "muscle_gain"}
    }
    r = client.post("/supplements", json=payload_supps)
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "success"
    assert "💊" in res["response"] or "Supplement" in res["response"]
    assert "recommendations" in res["data"]
    print("[PASS] Supplements scenario produced formatted presentation text & internal structured data!")

    # Scenario 4: Gym Shopping
    print("\n--- Scenario 4: Gym Shopping (/shopping) ---")
    payload_shop = {"query": "shoes", "budget": "medium"}
    r = client.post("/shopping", json=payload_shop)
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "success"
    assert "🛍️" in res["response"] or "Shopping" in res["response"]
    assert "items" in res["data"]
    print("[PASS] Gym Shopping scenario produced formatted presentation text & internal structured data!")

    # Scenario 5: Healthy Restaurants
    print("\n--- Scenario 5: Healthy Restaurants (/restaurants) ---")
    payload_rest = {"location": "New York, NY", "query": "healthy"}
    r = client.post("/restaurants", json=payload_rest)
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "success"
    assert "🍽️" in res["response"] or "Restaurants" in res["response"]
    assert "restaurants" in res["data"]
    print("[PASS] Healthy Restaurants scenario produced formatted presentation text & internal structured data!")

    # Scenario 6: Progress Tracking
    print("\n--- Scenario 6: Progress Tracking (/progress) ---")
    payload_prog = {
        "current_weight_kg": 74.0,
        "previous_weight_kg": 75.0,
        "goal": "fat_loss",
        "weeks_active": 4,
        "workouts_completed": 12,
        "workouts_planned": 16
    }
    r = client.post("/progress", json=payload_prog)
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "success"
    assert "📈" in res["response"] or "Progress" in res["response"]
    assert "trend" in res["data"] or "weight_change_kg" in res["data"]
    print("[PASS] Progress Tracking scenario produced formatted presentation text & internal structured data!")

    # Scenario 7: Motivation (via Chat / Motivation intent)
    print("\n--- Scenario 7: Motivation (/chat) ---")
    payload_chat = {"message": "Encourage me to keep hitting the gym every day!"}
    r = client.post("/chat", json=payload_chat)
    assert r.status_code == 200
    res = r.json()
    assert len(res["response"]) > 0
    assert not res["response"].startswith("{")  # Must be formatted presentation text, not raw JSON
    print(f"[PASS] Motivation scenario produced formatted response via Orchestrator! Agents used: {res['agents_used']}")

    print("\n========================================================")
    print(" ALL 7 SCENARIO END-TO-END TESTS PASSED SUCCESSFULLY!   ")
    print("========================================================")

if __name__ == "__main__":
    run_tests()
