from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    name: str
    quantity: str
    
class Recipe(BaseModel):
    recipe_name : str
    description : str = ""
    servings: int = Field(default=2, ge=1)
    
    prep_time_minutes: int = Field(default=10, ge=0)
    cook_time_minutes: int = Field(default=20, ge=0)
    
    ingredients: list[Ingredient]
    
    instructions: list[str]
    
    chef: str = ""
    model: str = ""
    