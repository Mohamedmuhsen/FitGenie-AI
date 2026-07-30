"""
Injury prevention task module.
"""
from crewai import Task, Agent

def create_injury_prevention_task(agent: Agent, assessment_data: str, workout_data: str) -> Task:
    """Create a task for the injury prevention agent."""
    return Task(
        description=f"""Analyze the workout plan for safety.
- Analyze the workout plan against the user's injuries and conditions
- Identify any exercises that are risky given the user's specific injuries
- For each risky exercise, suggest a safer alternative targeting the same muscle
- Add form cues and safety warnings
- Return the modified/validated workout plan

Assessment Data:
{assessment_data}

Workout Data:
{workout_data}
""",
        expected_output="A JSON object with fields: original_exercises_flagged (list of risky exercises with reason), safe_alternatives (list with original, replacement, reason), safety_warnings (list), modified_workout_plan_notes (str)",
        agent=agent,
    )
