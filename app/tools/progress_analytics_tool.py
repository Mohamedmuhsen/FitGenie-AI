import json
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from app.services.calculator_service import CalculatorService

class ProgressAnalyticsInput(BaseModel):
    """Input schema for ProgressAnalyticsTool."""
    current_weight_kg: float = Field(..., description="User's current weight in kg.")
    previous_weight_kg: float = Field(..., description="User's previous weight in kg.")
    goal: str = Field(..., description="User's fitness goal ('cut', 'maintenance', 'bulk').")
    weeks_active: int = Field(..., description="Number of weeks active.")
    workouts_completed: int = Field(..., description="Number of workouts completed.")
    workouts_planned: int = Field(..., description="Number of workouts planned.")

class ProgressAnalyticsTool(BaseTool):
    name: str = "Progress Analytics Tool"
    description: str = "Analyzes fitness progress data and metrics over time."
    args_schema: type[BaseModel] = ProgressAnalyticsInput

    def _run(self, current_weight_kg: float, previous_weight_kg: float, goal: str, weeks_active: int, workouts_completed: int, workouts_planned: int, **kwargs) -> str:
        # TODO: Replace with PostgreSQL queries and time-series analysis in production
        try:
            metrics = CalculatorService.calculate_progress_metrics(
                current_weight_kg, previous_weight_kg, workouts_completed, workouts_planned, goal
            )
            
            weight_diff = current_weight_kg - previous_weight_kg
            trend_analysis = "Weight is stable."
            if weight_diff > 0:
                trend_analysis = f"Gained {weight_diff:.1f} kg." if goal == 'bulk' else f"Unexpectedly gained {weight_diff:.1f} kg. Consider reviewing diet."
            elif weight_diff < 0:
                trend_analysis = f"Lost {abs(weight_diff):.1f} kg." if goal == 'cut' else f"Unexpectedly lost {abs(weight_diff):.1f} kg. Consider increasing intake."

            response = {
                "metrics": metrics,
                "analysis": trend_analysis
            }
            
            return json.dumps(response)
        except Exception as e:
            return json.dumps({"error": str(e)})
