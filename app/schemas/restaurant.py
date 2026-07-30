from pydantic import BaseModel, Field

class RestaurantRecommendation(BaseModel):
    name: str
    cuisine: str
    rating: float = Field(..., ge=0, le=5)
    distance_km: float
    address: str
    recommended_meal: str
    estimated_calories: int
    reason: str

class RestaurantOutput(BaseModel):
    restaurants: list[RestaurantRecommendation]
