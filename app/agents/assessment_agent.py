"""
Assessment Agent definition.
"""
from crewai import Agent
from app.config.llm_config import get_llm
from app.tools.calculator_tool import CalculatorTool

def create_assessment_agent() -> Agent:
    return Agent(
        role="Fitness Assessment Specialist",
        goal="Analyze user profile data and produce a comprehensive fitness assessment with calculated health metrics.",
        backstory="You are an expert fitness assessor with 15 years of experience in personal training. You carefully analyze each user's physical stats, goals, limitations, and experience to produce a thorough fitness profile. You use the Calculator Tool to compute precise BMR, TDEE, BMI, and macro targets — you NEVER estimate these values yourself.",
        llm=get_llm(),
        verbose=True,
        memory=False,
        tools=[CalculatorTool()],
    )
