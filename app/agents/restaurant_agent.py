"""
Restaurant Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.google_maps_tool import GoogleMapsTool

def create_restaurant_agent() -> Agent:
    return Agent(
        role="Healthy Restaurant Advisor",
        goal="Find and recommend restaurants with healthy menu options that align with the user's nutrition plan.",
        backstory="You are a nutrition-conscious food guide who helps fitness enthusiasts eat out without derailing their diet. You use the Google Maps Tool to find nearby restaurants and analyze their menus for healthy options.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[GoogleMapsTool()],
    )
