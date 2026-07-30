from pydantic import BaseModel, Field
from enum import Enum

class FitnessGoal(str, Enum):
    MUSCLE_GAIN = "muscle_gain"
    FAT_LOSS = "fat_loss"
    MAINTENANCE = "maintenance"
    ENDURANCE = "endurance"
    FLEXIBILITY = "flexibility"

class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Budget(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class AssessmentInput(BaseModel):
    """User assessment input — collected during onboarding."""
    age: int = Field(..., ge=13, le=100, description="User age in years")
    gender: Gender
    weight_kg: float = Field(..., gt=20, le=300)
    height_cm: float = Field(..., gt=100, le=250)
    goal: FitnessGoal
    experience_level: ExperienceLevel
    budget: Budget = Budget.MEDIUM
    workout_days_per_week: int = Field(..., ge=1, le=7)
    injuries: list[str] = Field(default_factory=list)
    diseases: list[str] = Field(default_factory=list)

class MacroSplit(BaseModel):
    protein_g: float
    carbs_g: float
    fats_g: float

class AssessmentOutput(BaseModel):
    """Enriched assessment with calculated metrics. All math done by CalculatorService."""
    user_profile: AssessmentInput
    bmr: float = Field(..., description="Basal Metabolic Rate (Mifflin-St Jeor)")
    tdee: float = Field(..., description="Total Daily Energy Expenditure")
    bmi: float
    bmi_category: str
    daily_calories: int
    macros: MacroSplit
    risk_factors: list[str] = Field(default_factory=list)
