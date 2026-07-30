from pydantic import BaseModel, Field

class Food(BaseModel):
    name: str
    portion: str
    calories: int
    protein_g: float
    carbs_g: float
    fats_g: float

class Meal(BaseModel):
    meal_name: str = Field(..., description="e.g. 'Breakfast', 'Lunch'")
    time: str = Field(..., description="e.g. '7:00 AM'")
    foods: list[Food]
    total_calories: int
    total_protein_g: float
    total_carbs_g: float
    total_fats_g: float

class NutritionPlanOutput(BaseModel):
    daily_calories: int
    protein_g: float
    carbs_g: float
    fats_g: float
    meals: list[Meal]
    hydration_liters: float = 2.5
    notes: str = ""
