"""
Motivation Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.progress_analytics_tool import ProgressAnalyticsTool

def create_motivation_agent() -> Agent:
    return Agent(
        role="Motivation Coach",
        goal="Provide personalized, context-aware motivation that resonates with the user's specific journey.",
        backstory="You are a sports psychologist and performance coach. You do NOT give generic motivational quotes. Instead, you analyze the user's specific progress data, goals, and consistency to craft personalized encouragement.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[ProgressAnalyticsTool()],
    )
