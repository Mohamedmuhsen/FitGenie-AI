"""
Restaurant task module.
"""
from crewai import Task, Agent
from app.schemas.restaurant import RestaurantOutput

def create_restaurant_task(agent: Agent, location_data: str) -> Task:
    """Create a task for the restaurant agent."""
    return Task(
        description=f"""Find healthy restaurants nearby.
- Use Google Maps Tool to find healthy restaurants nearby
- Recommend the best options with healthy menu items
- For each restaurant, suggest a specific meal with estimated calories
- Explain why each restaurant fits the user's fitness goals

Location Data:
{location_data}
""",
        expected_output="A JSON object with fields: restaurants (name, cuisine, rating, distance_km, address, recommended_meal, estimated_calories, reason)",
        agent=agent,
        output_pydantic=RestaurantOutput,
    )
