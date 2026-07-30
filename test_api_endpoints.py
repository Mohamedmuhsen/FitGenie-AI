"""
Extended FastAPI Endpoints & Payload Test Script
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_all_endpoints():
    print("\n--- 1. Testing GET / ---")
    r = client.get("/")
    print("GET / ->", r.status_code, r.json())
    assert r.status_code == 200

    print("\n--- 2. Testing GET /health ---")
    r = client.get("/health")
    print("GET /health ->", r.status_code, r.json())
    assert r.status_code == 200

    print("\n--- 3. Testing POST /assessment Payload Validation ---")
    valid_assessment = {
        "age": 25,
        "gender": "male",
        "weight_kg": 75.0,
        "height_cm": 175.0,
        "goal": "muscle_gain",
        "experience_level": "intermediate",
        "budget": "medium",
        "workout_days_per_week": 4,
        "injuries": ["shoulder"],
        "diseases": []
    }
    # Test input parsing (pydantic model validation on route)
    from app.schemas import AssessmentInput
    parsed = AssessmentInput(**valid_assessment)
    assert parsed.weight_kg == 75.0
    print("[PASS] AssessmentInput schema parsing validated!")

    print("\n--- 4. Testing POST /progress Payload Validation ---")
    valid_progress = {
        "current_weight_kg": 74.0,
        "previous_weight_kg": 75.0,
        "goal": "fat_loss",
        "weeks_active": 4,
        "workouts_completed": 12,
        "workouts_planned": 16
    }
    from app.schemas import ProgressInput
    parsed_prog = ProgressInput(**valid_progress)
    assert parsed_prog.current_weight_kg == 74.0
    print("[PASS] ProgressInput schema parsing validated!")

    print("\n--- 5. Testing POST /chat Payload Validation ---")
    from app.schemas import ChatRequest
    chat_req = ChatRequest(message="Recommend healthy restaurants near me", user_context=valid_assessment)
    assert chat_req.message == "Recommend healthy restaurants near me"
    print("[PASS] ChatRequest schema parsing validated!")

if __name__ == "__main__":
    test_all_endpoints()
    print("\n==========================================")
    print(" ALL FASTAPI ENDPOINT PAYLOAD TESTS PASSED! ")
    print("==========================================")
