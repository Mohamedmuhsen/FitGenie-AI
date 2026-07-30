import json
from typing import Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from app.services.calculator_service import CalculatorService

class CalculatorInput(BaseModel):
    """Input schema for CalculatorTool."""
    operation: str = Field(..., description="One of: 'bmr', 'tdee', 'bmi', 'macros', 'daily_calories', or 'all' to calculate all metrics.")
    weight_kg: float = Field(..., description="User's weight in kilograms.")
    height_cm: float = Field(170.0, description="User's height in centimeters.")
    age: int = Field(30, description="User's age in years.")
    gender: str = Field('male', description="User's gender ('male' or 'female').")
    activity_level: str = Field('moderately_active', description="Activity level (e.g., 'sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active').")
    goal: str = Field('maintenance', description="Fitness goal (e.g., 'cut', 'maintenance', 'bulk').")

class CalculatorTool(BaseTool):
    name: str = "Calculator Tool"
    description: str = "Calculates BMR, TDEE, BMI, macronutrient targets, and daily calorie needs based on user stats."
    args_schema: type[BaseModel] = CalculatorInput

    def _run(self, operation: str, weight_kg: float, height_cm: float = 170.0, age: int = 30, gender: str = 'male', activity_level: str = 'moderately_active', goal: str = 'maintenance', **kwargs) -> str:
        try:
            results = {}
            if operation in ('bmr', 'all'):
                results['bmr'] = CalculatorService.calculate_bmr(weight_kg, height_cm, age, gender)
            if operation in ('tdee', 'all'):
                bmr = results.get('bmr') or CalculatorService.calculate_bmr(weight_kg, height_cm, age, gender)
                results['tdee'] = CalculatorService.calculate_tdee(bmr, activity_level)
            if operation in ('bmi', 'all'):
                results['bmi'] = CalculatorService.calculate_bmi(weight_kg, height_cm)
            if operation in ('daily_calories', 'all'):
                tdee = results.get('tdee') or CalculatorService.calculate_tdee(CalculatorService.calculate_bmr(weight_kg, height_cm, age, gender), activity_level)
                results['daily_calories'] = CalculatorService.calculate_daily_calories(tdee, goal)
            if operation in ('macros', 'all'):
                calories = results.get('daily_calories') or CalculatorService.calculate_daily_calories(
                    CalculatorService.calculate_tdee(CalculatorService.calculate_bmr(weight_kg, height_cm, age, gender), activity_level), goal)
                results['macros'] = CalculatorService.calculate_macros(calories, goal, weight_kg)
            
            return json.dumps(results)
        except Exception as e:
            return json.dumps({"error": str(e)})
