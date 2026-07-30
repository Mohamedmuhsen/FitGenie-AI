"""
Shopping task module.
"""
from crewai import Task, Agent
from app.schemas.shopping import ShoppingOutput

def create_shopping_task(agent: Agent, user_preferences: str) -> Task:
    """Create a task for the shopping agent."""
    return Task(
        description=f"""Recommend gym gear based on user preferences.
- Use Shopping Search Tool to find gym gear
- Consider the user's training type, experience, and budget
- Recommend items across categories: shoes, clothes, accessories, equipment
- Prioritize: essential > recommended > optional
- Include estimated price and reason for each item

User Preferences:
{user_preferences}
""",
        expected_output="A JSON object with fields: items (name, category, estimated_price, reason, priority), total_estimated_budget",
        agent=agent,
        output_pydantic=ShoppingOutput,
    )
