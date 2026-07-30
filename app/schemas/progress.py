from pydantic import BaseModel, Field

class ProgressInput(BaseModel):
    current_weight_kg: float = Field(..., gt=0)
    previous_weight_kg: float = Field(..., gt=0)
    goal: str
    weeks_active: int = Field(..., ge=0)
    workouts_completed: int = Field(..., ge=0)
    workouts_planned: int = Field(..., ge=1)

class ProgressOutput(BaseModel):
    weight_change_kg: float
    weight_change_pct: float
    consistency_pct: float
    trend: str = Field(..., description="improving, stalling, or declining")
    summary: str
    adjustments: list[str] = Field(default_factory=list)
