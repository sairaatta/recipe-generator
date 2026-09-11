import logging

from .state import RecipeState
from .vision import identify_dish

logger = logging.getLogger(__name__)


def image_input(state: RecipeState):

    if not state.image_path:
        logger.info("No image provided")
        return {}

    logger.info(
        "Analyzing uploaded image: %s",
        state.image_path,
    )

    dish_name = identify_dish(
        state.image_path
    )

    logger.info(
        "FINAL VISION DISH: %s",
        dish_name,
    )

    if not dish_name:
        return {
            "image_dish": "unknown",
            "dishes": [],
        }

    return {
        "image_dish": dish_name,
        "dishes": [dish_name],
    }