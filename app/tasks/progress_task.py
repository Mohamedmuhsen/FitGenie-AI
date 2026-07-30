"""
Progress task module.
"""
from crewai import Task, Agent
from app.schemas.progress import ProgressOutput

def create_progress_task(agent: Agent, progress_data: str) -> Task:
    """Create a task for the progress tracking agent."""
    return Task(
        description=f"""Analyze fitness progress.
- Analyze the progress metrics (weight change, consistency)
- Use Progress Analytics Tool to calculate precise metrics
- Interpret the trend (improving, stalling, declining)
- Generate a weekly summary
- Suggest adjustments based on the data

Progress Data:
{progress_data}
""",
        expected_output="A JSON object with fields: weight_change_kg, weight_change_pct, consistency_pct, trend, summary, adjustments",
        agent=agent,
        output_pydantic=ProgressOutput,
    )
