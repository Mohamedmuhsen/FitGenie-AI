import json
from typing import Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ShoppingSearchInput(BaseModel):
    """Input schema for ShoppingSearchTool."""
    query: str = Field(..., description="Product type or specific product to search for.")
    budget: Optional[str] = Field(None, description="Budget constraint ('low', 'medium', 'high').")
    category: Optional[str] = Field(None, description="Product category ('shoes', 'clothes', 'equipment', 'accessories').")

class ShoppingSearchTool(BaseTool):
    name: str = "Shopping Search Tool"
    description: str = "Searches for fitness-related products like gym gear, clothes, and supplements."
    args_schema: type[BaseModel] = ShoppingSearchInput

    def _run(self, query: str, budget: Optional[str] = None, category: Optional[str] = None, **kwargs) -> str:
        # TODO: Replace with Tavily Search API in production
        
        products = [
            {"name": "Nike Metcon 9", "category": "shoes", "estimated_price": 130, "reason": "Excellent stability for heavy lifting.", "priority": "high"},
            {"name": "Reebok Nano X4", "category": "shoes", "estimated_price": 135, "reason": "Versatile for cross-training.", "priority": "high"},
            {"name": "Adidas Dropset", "category": "shoes", "estimated_price": 110, "reason": "Good value for weightlifting shoes.", "priority": "medium"},
            
            {"name": "RDX Weight Lifting Gloves", "category": "gloves", "estimated_price": 15, "reason": "Affordable basic hand protection.", "priority": "low"},
            {"name": "Harbinger Pro", "category": "gloves", "estimated_price": 22, "reason": "Durable with good wrist support.", "priority": "medium"},
            
            {"name": "Rogue Ohio Belt", "category": "belts", "estimated_price": 80, "reason": "Premium leather belt for serious lifting.", "priority": "high"},
            {"name": "Dark Iron Fitness Belt", "category": "belts", "estimated_price": 35, "reason": "Great budget leather lifting belt.", "priority": "medium"},
            
            {"name": "BlenderBottle Classic", "category": "shakers", "estimated_price": 12, "reason": "The standard reliable protein shaker.", "priority": "medium"},
            {"name": "Helimix Vortex", "category": "shakers", "estimated_price": 22, "reason": "Mixes without a ball, easier to clean.", "priority": "high"},
            
            {"name": "Under Armour Tech Tee", "category": "clothes", "estimated_price": 25, "reason": "Basic, breathable workout shirt.", "priority": "medium"},
            {"name": "Nike Dri-FIT Shorts", "category": "clothes", "estimated_price": 35, "reason": "Comfortable and sweat-wicking.", "priority": "medium"},
            {"name": "Gymshark Seamless", "category": "clothes", "estimated_price": 40, "reason": "Fitted and stretchy for active movement.", "priority": "high"},
        ]
        
        query_lower = query.lower()
        results = [
            p for p in products 
            if query_lower in p["name"].lower() or query_lower in p["category"].lower() or (category and category.lower() == p["category"].lower())
        ]
        
        return json.dumps(results)
