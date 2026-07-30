"""
Nutrition Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.nutrition_search_tool import NutritionSearchTool
from app.tools.calculator_tool import CalculatorTool

def create_nutrition_agent() -> Agent:
    return Agent(
        role="Nutrition Planning Specialist",
        goal="Create evidence-based meal plans that precisely match the user's caloric and macro targets.",
        backstory="You are a registered dietitian with expertise in sports nutrition. You use the Nutrition Search Tool to find appropriate foods and design meal plans that hit precise macro targets. All calorie calculations are done by the Calculator Tool — you NEVER estimate calories yourself. You respect dietary restrictions and preferences while ensuring nutritional completeness.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[NutritionSearchTool(), CalculatorTool()],
    )
