"""
Workout task module.
"""
from crewai import Task, Agent
from app.schemas.workout import WorkoutPlanOutput

def create_workout_task(agent: Agent, assessment_data: str) -> Task:
    """Create a task for the workout agent."""
    return Task(
        description=f"""Design a personalized workout plan.
- Parse the assessment data
- Use Exercise Search Tool to find appropriate exercises
- Design a weekly workout plan matching the user's goal, experience, available days
- Include proper warmup and cooldown
- Include progression strategy
- Consider injuries when selecting exercises

Assessment Data:
{assessment_data}
""",
        expected_output="A JSON object with fields: plan_name, goal, experience_level, days_per_week, weeks, workout_days (each with day, focus, exercises with name/sets/reps/rest/muscle_group), warmup, cooldown, progression_notes",
        agent=agent,
        output_pydantic=WorkoutPlanOutput,
    )
