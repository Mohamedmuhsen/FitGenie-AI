"""
Progress Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.progress_analytics_tool import ProgressAnalyticsTool
from app.tools.calculator_tool import CalculatorTool

def create_progress_agent() -> Agent:
    return Agent(
        role="Progress Analyst",
        goal="Analyze user fitness progress data and provide actionable insights for plan adjustments.",
        backstory="You are a data-driven fitness analyst who tracks body metrics, workout consistency, and goal progress. You use the Progress Analytics Tool for precise calculations and then interpret the trends, identifying plateaus early.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[ProgressAnalyticsTool(), CalculatorTool()],
    )
