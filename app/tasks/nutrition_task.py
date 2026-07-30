"""
Nutrition task module.
"""
from crewai import Task, Agent
from app.schemas.nutrition import NutritionPlanOutput

def create_nutrition_task(agent: Agent, assessment_data: str, workout_data: str = "") -> Task:
    """Create a task for the nutrition agent."""
    return Task(
        description=f"""Design a personalized nutrition plan.
- Parse assessment data for calorie/macro targets
- Use Nutrition Search Tool to find appropriate foods
- Design a daily meal plan with 4-5 meals
- Each meal should have foods with portions and macros
- Total daily macros must match the targets from assessment
- Respect dietary restrictions
- Include hydration recommendation

Assessment Data:
{assessment_data}

Workout Data (Optional):
{workout_data}
""",
        expected_output="A JSON object with fields: daily_calories, protein_g, carbs_g, fats_g, meals (each with meal_name, time, foods with name/portion/calories/macros, totals), hydration_liters, notes",
        agent=agent,
        output_pydantic=NutritionPlanOutput,
    )
