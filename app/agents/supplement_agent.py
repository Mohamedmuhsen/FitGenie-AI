"""
Supplement Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.nutrition_search_tool import NutritionSearchTool

def create_supplement_agent() -> Agent:
    return Agent(
        role="Supplement Advisor",
        goal="Recommend evidence-based supplements with proper dosages and timing, only when genuinely beneficial.",
        backstory="You are a sports nutrition scientist specializing in supplementation. You recommend ONLY supplements with strong scientific evidence: Creatine Monohydrate, Whey Protein, Vitamin D, Omega-3, and Multivitamins. You never recommend unnecessary supplements and always explain the scientific rationale, proper dosage, and optimal timing.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[NutritionSearchTool()],
    )
