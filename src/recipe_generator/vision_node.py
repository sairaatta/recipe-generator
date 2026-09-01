import logging

from .state import RecipeState
from .vision import identify_dish


logger = logging.getLogger(__name__)


def identify_dish_node(state: RecipeState):
    """
    Identify the dish from the single uploaded image.
    """

    if not state.image_path:

        logger.info(
            "No image provided. Skipping vision."
        )

        return {}

    logger.info(
        "Analyzing uploaded image..."
    )

    dish_name = identify_dish(
        state.image_path
    )

    logger.info(
        "Detected dish: %s",
        dish_name,
    )

    if not dish_name or dish_name.lower() == "unknown":

        logger.warning(
            "Vision model could not confidently identify the dish."
        )

        return {
            "image_dish": "unknown",
            "dishes": [],
        }

    return {
        "image_dish": dish_name,
        "dishes": [dish_name],
    }

