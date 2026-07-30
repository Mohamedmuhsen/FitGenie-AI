"""
FitGenie AI Comprehensive Validation & Test Suite
"""
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.calculator_service import CalculatorService
from app.services.orchestrator_service import OrchestratorService
from app.tools import (
    CalculatorTool, ExerciseSearchTool, NutritionSearchTool,
    GoogleMapsTool, ShoppingSearchTool, ProgressAnalyticsTool
)
from app.schemas import (
    AssessmentInput, FitnessGoal, ExperienceLevel, Gender, Budget,
    ProgressInput
)
from app.agents import (
    create_orchestrator_agent, create_assessment_agent, create_workout_agent,
    create_nutrition_agent, create_supplement_agent, create_injury_prevention_agent,
    create_progress_agent, create_motivation_agent, create_shopping_agent, create_restaurant_agent
)
from app.tasks import (
    create_assessment_task, create_workout_task, create_nutrition_task,
    create_supplement_task, create_injury_prevention_task, create_progress_task,
    create_motivation_task, create_shopping_task, create_restaurant_task
)
from app.crews import FitnessCrew

client = TestClient(app)

def test_calculator_service():
    print("\n--- Testing Calculator Service ---")
    bmr = CalculatorService.calculate_bmr(75.0, 175.0, 25, "male")
    assert bmr > 1600, f"Expected BMR > 1600, got {bmr}"
    
    tdee = CalculatorService.calculate_tdee(bmr, "moderately_active")
    assert tdee > bmr, f"Expected TDEE > BMR, got {tdee}"
    
    bmi = CalculatorService.calculate_bmi(75.0, 175.0)
    category = CalculatorService.get_bmi_category(bmi)
    assert category == "Normal", f"Expected Normal, got {category}"
    
    calories = CalculatorService.calculate_daily_calories(tdee, "muscle_gain")
    assert calories == int(tdee + 300)
    
    macros = CalculatorService.calculate_macros(calories, "muscle_gain", 75.0)
    assert "protein_g" in macros and "carbs_g" in macros and "fats_g" in macros
    
    progress = CalculatorService.calculate_progress_metrics(74.0, 75.0, 4, 4, "fat_loss")
    assert progress["trend"] == "improving"
    print("[PASS] Calculator Service tests passed!")

def test_tools():
    print("\n--- Testing Tools ---")
    
    calc_tool = CalculatorTool()
    calc_res = json.loads(calc_tool._run(operation="all", weight_kg=75.0, height_cm=175.0, age=25, gender="male"))
    assert "bmr" in calc_res and "tdee" in calc_res and "bmi" in calc_res
    print("[PASS] CalculatorTool passed!")
    
    ex_tool = ExerciseSearchTool()
    ex_res = json.loads(ex_tool._run(query="chest"))
    assert len(ex_res) > 0 and ex_res[0]["muscle_group"] == "chest"
    print("[PASS] ExerciseSearchTool passed!")
    
    nut_tool = NutritionSearchTool()
    nut_res = json.loads(nut_tool._run(query="chicken"))
    assert len(nut_res) > 0
    print("[PASS] NutritionSearchTool passed!")
    
    maps_tool = GoogleMapsTool()
    maps_res = json.loads(maps_tool._run(query="healthy"))
    assert len(maps_res) > 0 and "name" in maps_res[0]
    print("[PASS] GoogleMapsTool passed!")
    
    shop_tool = ShoppingSearchTool()
    shop_res = json.loads(shop_tool._run(query="shoes"))
    assert len(shop_res) > 0 and shop_res[0]["category"] == "shoes"
    print("[PASS] ShoppingSearchTool passed!")
    
    prog_tool = ProgressAnalyticsTool()
    prog_res = json.loads(prog_tool._run(current_weight_kg=74.0, previous_weight_kg=75.0, goal="fat_loss", weeks_active=4, workouts_completed=4, workouts_planned=4))
    assert "metrics" in prog_res and "analysis" in prog_res
    print("[PASS] ProgressAnalyticsTool passed!")

def test_agent_and_task_factories():
    print("\n--- Testing Agent and Task Initialization ---")
    a_orchestrator = create_orchestrator_agent()
    a_assessment = create_assessment_agent()
    a_workout = create_workout_agent()
    a_nutrition = create_nutrition_agent()
    a_supplement = create_supplement_agent()
    a_injury = create_injury_prevention_agent()
    a_progress = create_progress_agent()
    a_motivation = create_motivation_agent()
    a_shopping = create_shopping_agent()
    a_restaurant = create_restaurant_agent()
    
    assert a_orchestrator.role == "Fitness Orchestrator"
    assert len(a_assessment.tools) == 1
    assert len(a_workout.tools) == 2
    assert len(a_nutrition.tools) == 2
    assert len(a_supplement.tools) == 1
    assert len(a_injury.tools) == 1
    assert len(a_progress.tools) == 2
    assert len(a_motivation.tools) == 1
    assert len(a_shopping.tools) == 1
    assert len(a_restaurant.tools) == 1
    
    print("[PASS] All 10 Agents instantiated successfully!")
    
    dummy_input = '{"goal": "muscle_gain"}'
    t_assessment = create_assessment_task(a_assessment, dummy_input)
    t_workout = create_workout_task(a_workout, dummy_input)
    t_nutrition = create_nutrition_task(a_nutrition, dummy_input)
    t_supplement = create_supplement_task(a_supplement, dummy_input)
    t_injury = create_injury_prevention_task(a_injury, dummy_input, dummy_input)
    t_progress = create_progress_task(a_progress, dummy_input)
    t_motivation = create_motivation_task(a_motivation, dummy_input)
    t_shopping = create_shopping_task(a_shopping, dummy_input)
    t_restaurant = create_restaurant_task(a_restaurant, dummy_input)
    
    assert t_assessment.agent == a_assessment
    assert t_workout.agent == a_workout
    assert t_nutrition.agent == a_nutrition
    assert t_supplement.agent == a_supplement
    assert t_injury.agent == a_injury
    assert t_progress.agent == a_progress
    assert t_motivation.agent == a_motivation
    assert t_shopping.agent == a_shopping
    assert t_restaurant.agent == a_restaurant
    
    print("[PASS] All Tasks instantiated successfully!")

def test_crews():
    print("\n--- Testing FitnessCrew Instantiation ---")
    dummy_dict = {"age": 25, "gender": "male", "weight_kg": 75, "height_cm": 175, "goal": "muscle_gain"}
    c_assess = FitnessCrew.assessment_crew(dummy_dict)
    assert len(c_assess.agents) == 1
    
    c_work = FitnessCrew.workout_crew(dummy_dict)
    assert len(c_work.agents) == 1
    
    c_full = FitnessCrew.full_plan_crew(dummy_dict)
    assert len(c_full.agents) == 5
    assert len(c_full.tasks) == 5
    print("[PASS] FitnessCrew static factories passed!")

def test_fastapi_endpoints():
    print("\n--- Testing FastAPI Endpoints ---")
    
    # GET /
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "active"
    
    # GET /health
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
    
    # Validation tests for POST endpoints
    invalid_res = client.post("/assessment", json={"age": 5}) # age < 13
    assert invalid_res.status_code == 422
    
    print("[PASS] FastAPI health, root & input validation passed!")

if __name__ == "__main__":
    test_calculator_service()
    test_tools()
    test_agent_and_task_factories()
    test_crews()
    test_fastapi_endpoints()
    print("\n==========================================")
    print(" ALL MVP VALIDATION TESTS PASSED OK! ")
    print("==========================================")
