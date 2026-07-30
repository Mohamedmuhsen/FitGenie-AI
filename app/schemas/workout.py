from pydantic import BaseModel, Field

class Exercise(BaseModel):
    name: str
    sets: int = Field(..., ge=1)
    reps: str = Field(..., description="e.g. '8-12' or '30 seconds'")
    rest_seconds: int = Field(default=60)
    muscle_group: str
    notes: str = ""

class WorkoutDay(BaseModel):
    day: str = Field(..., description="e.g. 'Monday' or 'Day 1'")
    focus: str = Field(..., description="e.g. 'Chest & Triceps'")
    exercises: list[Exercise]
    duration_minutes: int

class WorkoutPlanOutput(BaseModel):
    plan_name: str
    goal: str
    experience_level: str
    days_per_week: int
    weeks: int = 4
    workout_days: list[WorkoutDay]
    warmup: str
    cooldown: str
    progression_notes: str
