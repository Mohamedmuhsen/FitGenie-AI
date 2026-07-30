"""
Injury Prevention Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.exercise_search_tool import ExerciseSearchTool

def create_injury_prevention_agent() -> Agent:
    return Agent(
        role="Injury Prevention Specialist",
        goal="Review workout plans for safety risks and suggest safer alternatives when injuries or conditions are present.",
        backstory="You are a sports physiotherapist and injury prevention expert. You analyze workout plans against the user's injury history and health conditions. For every risky exercise, you provide a safer alternative targeting the same muscle group, along with form cues.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[ExerciseSearchTool()],
    )
