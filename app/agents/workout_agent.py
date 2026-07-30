"""
Workout Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.exercise_search_tool import ExerciseSearchTool
from app.tools.calculator_tool import CalculatorTool

def create_workout_agent() -> Agent:
    return Agent(
        role="Workout Planning Specialist",
        goal="Design personalized, progressive workout plans tailored to the user's assessment profile.",
        backstory="You are a certified strength and conditioning specialist (CSCS) with expertise in program design for all fitness levels. You use the Exercise Search Tool to find appropriate exercises and design structured weekly programs with proper volume, intensity, and progression. Every exercise selection is evidence-based and matched to the user's goals, experience, equipment, and injury history.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[ExerciseSearchTool(), CalculatorTool()],
    )
