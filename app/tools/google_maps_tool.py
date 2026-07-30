import json
from typing import Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class GoogleMapsInput(BaseModel):
    """Input schema for GoogleMapsTool."""
    query: str = Field(..., description="Query to search for (e.g. 'healthy restaurants near me').")
    location: str = Field('New York, NY', description="Location to search in.")
    radius_km: float = Field(5.0, description="Radius in kilometers to search within.")

class GoogleMapsTool(BaseTool):
    name: str = "Google Maps Tool"
    description: str = "Searches for places like healthy restaurants using Google Maps."
    args_schema: type[BaseModel] = GoogleMapsInput

    def _run(self, query: str, location: str = 'New York, NY', radius_km: float = 5.0, **kwargs) -> str:
        # TODO: Replace with actual Google Maps Places API in production
        
        restaurants = [
            {
                "name": "Green Bowl Kitchen", 
                "cuisine": "Salad/Bowl bar", 
                "rating": 4.7, 
                "distance_km": 1.2, 
                "address": "123 Green St, New York, NY", 
                "recommended_meal": "Grilled Chicken Power Bowl", 
                "estimated_calories": 520, 
                "reason": "High protein and fiber, locally sourced ingredients."
            },
            {
                "name": "Protein House", 
                "cuisine": "Fitness meals", 
                "rating": 4.5, 
                "distance_km": 2.1, 
                "address": "456 Muscle Ave, New York, NY", 
                "recommended_meal": "High Protein Steak & Veggies", 
                "estimated_calories": 680, 
                "reason": "Excellent macro balance for muscle building."
            },
            {
                "name": "Fresh & Fit Café", 
                "cuisine": "Healthy café", 
                "rating": 4.6, 
                "distance_km": 0.8, 
                "address": "789 Fit Blvd, New York, NY", 
                "recommended_meal": "Salmon Quinoa Plate", 
                "estimated_calories": 580, 
                "reason": "Rich in omega-3s and complex carbs."
            },
            {
                "name": "Muscle Meals Prep", 
                "cuisine": "Meal prep", 
                "rating": 4.4, 
                "distance_km": 3.5, 
                "address": "101 Prep Rd, New York, NY", 
                "recommended_meal": "Lean Turkey Wrap", 
                "estimated_calories": 450, 
                "reason": "Convenient, low-fat option for cutting."
            },
            {
                "name": "The Clean Plate", 
                "cuisine": "Farm to table", 
                "rating": 4.8, 
                "distance_km": 1.9, 
                "address": "202 Organic Ln, New York, NY", 
                "recommended_meal": "Organic Grilled Chicken Salad", 
                "estimated_calories": 380, 
                "reason": "Very clean, minimal processed ingredients."
            }
        ]
        
        return json.dumps(restaurants)
