"""
Assessment task module.
"""
from crewai import Task, Agent
from app.schemas.assessment import AssessmentOutput

def create_assessment_task(agent: Agent, input_data: str) -> Task:
    """Create a task for the assessment agent."""
    return Task(
        description=f"""Analyze the user's fitness profile.
- Parse the user profile data from the input
- Use the Calculator Tool to compute BMR, TDEE, BMI, and daily calories
- Calculate macros based on the user's goal
- Identify risk factors based on injuries, diseases, BMI
- Return a comprehensive assessment output

Input Data:
{input_data}
""",
        expected_output="A JSON object with fields: user_profile, bmr, tdee, bmi, bmi_category, daily_calories, macros (protein_g, carbs_g, fats_g), risk_factors",
        agent=agent,
        output_pydantic=AssessmentOutput,
    )
