"""
Supplement task module.
"""
from crewai import Task, Agent
from app.schemas.supplement import SupplementPlanOutput

def create_supplement_task(agent: Agent, assessment_data: str, nutrition_data: str = "", workout_data: str = "") -> Task:
    """Create a task for the supplement agent."""
    return Task(
        description=f"""Recommend a personalized supplement plan.
- Analyze the user's goals, diet, and training
- Only recommend from: Creatine Monohydrate, Whey Protein, Vitamin D, Omega-3, Multivitamin
- For each, explain why it's recommended, dosage, and timing
- Rate priority: essential, recommended, or optional
- Estimate monthly cost
- Avoid recommending what's unnecessary

Assessment Data:
{assessment_data}

Nutrition Data (Optional):
{nutrition_data}

Workout Data (Optional):
{workout_data}
""",
        expected_output="A JSON object with fields: recommendations (name, dosage, timing, reason, priority), total_monthly_cost_estimate, warnings",
        agent=agent,
        output_pydantic=SupplementPlanOutput,
    )
