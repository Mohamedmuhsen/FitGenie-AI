from pydantic import BaseModel, Field

class ShoppingItem(BaseModel):
    name: str
    category: str = Field(..., description="e.g. 'shoes', 'belt', 'gloves'")
    estimated_price: str
    reason: str
    priority: str = Field(..., description="essential, recommended, or optional")

class ShoppingOutput(BaseModel):
    items: list[ShoppingItem]
    total_estimated_budget: str
