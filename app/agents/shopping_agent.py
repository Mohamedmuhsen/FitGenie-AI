"""
Shopping Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.shopping_search_tool import ShoppingSearchTool

def create_shopping_agent() -> Agent:
    return Agent(
        role="Fitness Shopping Advisor",
        goal="Recommend the best gym equipment, clothes, and accessories for the user's needs and budget.",
        backstory="You are a fitness gear specialist who tests and reviews gym equipment, workout clothing, and accessories. You recommend products based on training style, experience level, and budget.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[ShoppingSearchTool()],
    )
