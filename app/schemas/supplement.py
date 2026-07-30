from pydantic import BaseModel, Field

class SupplementRecommendation(BaseModel):
    name: str
    dosage: str
    timing: str
    reason: str
    priority: str = Field(..., description="essential, recommended, or optional")

class SupplementPlanOutput(BaseModel):
    recommendations: list[SupplementRecommendation]
    total_monthly_cost_estimate: str
    warnings: list[str] = Field(default_factory=list)
