from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str = Field(description="Name of the ingredient")
    quantity: str = Field(description="Amount needed, including unit")


class Recipe(BaseModel):
    name: str = Field(description="Name of the recipe")
    description: str = Field(description="Short description of the recipe")
    ingredients: list[Ingredient] = Field(
        description="List of ingredients required"
    )
    instructions: list[str] = Field(
        description="Step-by-step cooking instructions"
    )
    cooking_time_minutes: int = Field(
        description="Estimated total cooking time in minutes"
    )
    servings: int = Field(
        description="Number of servings"
    )