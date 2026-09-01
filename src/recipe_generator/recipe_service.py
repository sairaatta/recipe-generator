import logging

from .generator import generate_recipe
from .state import RecipeState

logger = logging.getLogger(__name__)


def generate_recipe_from_state(state: RecipeState) -> RecipeState:
    logger.info("Starting recipe state processing")
    logger.info(
        "Current state status: %s",
        state.status
    )
    
    try:
        state.status = "generating"
        logger.info(
            "Generating recipe for: %s",
            state.user_request,
        )
        
        recipe = generate_recipe(
            state.user_request
        )
        state.recipe = recipe
        state.status = "completed"
        state.error = None
        
        logger.info(
            "Recipe generation completed: %s",
            recipe.name,
        )
        
    except Exception as exc:
        state.status = "failed"
        state.error = str(exc)
        
        logger.exception(
            "Recipe generation failed"
        )
        
    return state