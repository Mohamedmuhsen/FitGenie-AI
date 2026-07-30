"""
Motivation task module.
"""
from crewai import Task, Agent

def create_motivation_task(agent: Agent, progress_data: str) -> Task:
    """Create a task for the motivation agent."""
    return Task(
        description=f"""Generate personalized motivation.
- Analyze the user's progress data and journey
- Generate a PERSONALIZED motivational message (NOT generic quotes)
- Reference specific achievements or challenges from the data
- Adapt tone: celebratory if improving, supportive if stalling, encouraging if declining
- Include actionable next steps

Progress Data:
{progress_data}
""",
        expected_output="A personalized motivational message with specific references to the user's journey, acknowledging their progress, and suggesting concrete next steps.",
        agent=agent,
    )
