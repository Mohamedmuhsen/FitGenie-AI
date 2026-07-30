import json
from typing import Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class NutritionSearchInput(BaseModel):
    """Input schema for NutritionSearchTool."""
    query: str = Field(..., description="Food type, meal type, or dietary need to search for.")
    dietary_restrictions: Optional[str] = Field(None, description="Dietary restrictions (e.g., 'vegan', 'gluten-free').")
    calorie_target: Optional[int] = Field(None, description="Target calories for the meal or food.")

class NutritionSearchTool(BaseTool):
    name: str = "Nutrition Search Tool"
    description: str = "Searches for appropriate foods and meals based on query, dietary restrictions, and calorie targets."
    args_schema: type[BaseModel] = NutritionSearchInput

    def _run(self, query: str, dietary_restrictions: Optional[str] = None, calorie_target: Optional[int] = None, **kwargs) -> str:
        # TODO: Replace with ChromaDB vector search in production
        
        # Hardcoded dictionary of foods organized by category
        foods = [
            {"name": "chicken breast", "category": "proteins", "calories_per_100g": 165, "protein_g": 31, "carbs_g": 0, "fats_g": 3.6, "serving_size": "100g"},
            {"name": "salmon", "category": "proteins", "calories_per_100g": 208, "protein_g": 20, "carbs_g": 0, "fats_g": 13, "serving_size": "100g"},
            {"name": "eggs", "category": "proteins", "calories_per_100g": 155, "protein_g": 13, "carbs_g": 1.1, "fats_g": 11, "serving_size": "100g (approx 2 eggs)"},
            {"name": "Greek yogurt", "category": "proteins", "calories_per_100g": 59, "protein_g": 10, "carbs_g": 3.6, "fats_g": 0.4, "serving_size": "150g"},
            {"name": "tofu", "category": "proteins", "calories_per_100g": 144, "protein_g": 16, "carbs_g": 2.8, "fats_g": 8.7, "serving_size": "100g"},
            {"name": "lean beef", "category": "proteins", "calories_per_100g": 250, "protein_g": 26, "carbs_g": 0, "fats_g": 15, "serving_size": "100g"},
            {"name": "turkey", "category": "proteins", "calories_per_100g": 189, "protein_g": 29, "carbs_g": 0, "fats_g": 7, "serving_size": "100g"},
            
            {"name": "brown rice", "category": "carbs", "calories_per_100g": 111, "protein_g": 2.6, "carbs_g": 23, "fats_g": 0.9, "serving_size": "100g (cooked)"},
            {"name": "oats", "category": "carbs", "calories_per_100g": 389, "protein_g": 16.9, "carbs_g": 66.3, "fats_g": 6.9, "serving_size": "50g (dry)"},
            {"name": "sweet potato", "category": "carbs", "calories_per_100g": 86, "protein_g": 1.6, "carbs_g": 20.1, "fats_g": 0.1, "serving_size": "100g"},
            {"name": "quinoa", "category": "carbs", "calories_per_100g": 120, "protein_g": 4.4, "carbs_g": 21.3, "fats_g": 1.9, "serving_size": "100g (cooked)"},
            {"name": "whole wheat bread", "category": "carbs", "calories_per_100g": 247, "protein_g": 13, "carbs_g": 41, "fats_g": 3.4, "serving_size": "1 slice (~30g)"},
            {"name": "pasta", "category": "carbs", "calories_per_100g": 131, "protein_g": 5, "carbs_g": 25, "fats_g": 1.1, "serving_size": "100g (cooked)"},
            
            {"name": "avocado", "category": "fats", "calories_per_100g": 160, "protein_g": 2, "carbs_g": 8.5, "fats_g": 14.7, "serving_size": "50g"},
            {"name": "olive oil", "category": "fats", "calories_per_100g": 884, "protein_g": 0, "carbs_g": 0, "fats_g": 100, "serving_size": "1 tbsp (14g)"},
            {"name": "almonds", "category": "fats", "calories_per_100g": 579, "protein_g": 21.2, "carbs_g": 21.6, "fats_g": 49.9, "serving_size": "30g"},
            {"name": "peanut butter", "category": "fats", "calories_per_100g": 588, "protein_g": 25, "carbs_g": 20, "fats_g": 50, "serving_size": "2 tbsp (32g)"},
            {"name": "walnuts", "category": "fats", "calories_per_100g": 654, "protein_g": 15.2, "carbs_g": 13.7, "fats_g": 65.2, "serving_size": "30g"},
            
            {"name": "broccoli", "category": "vegetables", "calories_per_100g": 34, "protein_g": 2.8, "carbs_g": 6.6, "fats_g": 0.4, "serving_size": "100g"},
            {"name": "spinach", "category": "vegetables", "calories_per_100g": 23, "protein_g": 2.9, "carbs_g": 3.6, "fats_g": 0.4, "serving_size": "100g"},
            {"name": "kale", "category": "vegetables", "calories_per_100g": 49, "protein_g": 4.3, "carbs_g": 8.8, "fats_g": 0.9, "serving_size": "100g"},
            {"name": "bell peppers", "category": "vegetables", "calories_per_100g": 31, "protein_g": 1, "carbs_g": 6, "fats_g": 0.3, "serving_size": "100g"},
            {"name": "asparagus", "category": "vegetables", "calories_per_100g": 20, "protein_g": 2.2, "carbs_g": 3.9, "fats_g": 0.1, "serving_size": "100g"},
            
            {"name": "banana", "category": "fruits", "calories_per_100g": 89, "protein_g": 1.1, "carbs_g": 22.8, "fats_g": 0.3, "serving_size": "1 medium (118g)"},
            {"name": "blueberries", "category": "fruits", "calories_per_100g": 57, "protein_g": 0.7, "carbs_g": 14.5, "fats_g": 0.3, "serving_size": "100g"},
            {"name": "apple", "category": "fruits", "calories_per_100g": 52, "protein_g": 0.3, "carbs_g": 13.8, "fats_g": 0.2, "serving_size": "1 medium (182g)"},
            {"name": "orange", "category": "fruits", "calories_per_100g": 47, "protein_g": 0.9, "carbs_g": 11.8, "fats_g": 0.1, "serving_size": "1 medium (131g)"},
            {"name": "strawberries", "category": "fruits", "calories_per_100g": 32, "protein_g": 0.7, "carbs_g": 7.7, "fats_g": 0.3, "serving_size": "100g"}
        ]
        
        query_lower = query.lower()
        results = [
            food for food in foods 
            if query_lower in food["name"].lower() or query_lower in food["category"].lower()
        ]
        
        return json.dumps(results)
