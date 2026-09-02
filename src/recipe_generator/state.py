from typing import Optional

from pydantic import BaseModel, Field

from .recipe import Recipe


class Ingredient(BaseModel):
    name: str
    quantity: str


class RecipeState(BaseModel):

    # --------------------------------------------------
    # USER INPUT
    # --------------------------------------------------

    user_request: str = ""

    # --------------------------------------------------
    # INPUT DECISION / ORCHESTRATOR
    # --------------------------------------------------

    dishes: list[str] = Field(default_factory=list)

    input_mode: str = "unknown"

    mood: str | None = None

    # --------------------------------------------------
    # WEATHER
    # --------------------------------------------------

    weather_context: Optional[dict] = None

    # --------------------------------------------------
    # IMAGE / VISION
    # --------------------------------------------------

    image_path: Optional[str] = None

    image_dish: Optional[str] = None

    # --------------------------------------------------
    # MCP RESEARCH
    # --------------------------------------------------

    research: list = Field(default_factory=list)

    # --------------------------------------------------
    # GENERATED RECIPES
    # --------------------------------------------------

    # Dynamic list of recipes.
    #
    # OLD:
    # chef_a_recipe
    # chef_b_recipe
    # chef_c_recipe
    #
    # NEW:
    # recipes = [recipe1, recipe2, recipe3, ...]
    recipes: list[Recipe] = Field(default_factory=list)

    # --------------------------------------------------
    # SEQUENTIAL CHEF EXECUTION
    # --------------------------------------------------

    current_dish_index: int = 0

    # --------------------------------------------------
    # LLM TOKEN USAGE
    # --------------------------------------------------

    # One usage record for each generated recipe.
    #
    # Example:
    # [
    #     {"input": 300, "output": 500, "total": 800},
    #     {"input": 280, "output": 520, "total": 800},
    # ]
    chef_usage: list[dict[str, int]] = Field(default_factory=list)

    # --------------------------------------------------
    # COST ESTIMATION
    # --------------------------------------------------

    cost_estimates: dict = Field(
        default_factory=dict
    )

    # --------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------

    recipe_summary: str | None = None
    # --------------------------------------------------
    # WORKFLOW CONTROL
    # --------------------------------------------------

    status: str = "pending"

    error: Optional[str] = None

    next_step: Optional[str] = None