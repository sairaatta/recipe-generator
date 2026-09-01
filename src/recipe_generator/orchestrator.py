import logging
import re

from .state import RecipeState


logger = logging.getLogger(__name__)


# ============================================================
# EXPLICIT RECIPE EXTRACTION
# ============================================================

def extract_dishes(user_request: str) -> list[str]:
    """
    Extract dish names from an explicit recipe request.

    Examples:

        "give me recipes for pizza, pasta and burger"
        ->
        ["pizza", "pasta", "burger"]

        "generate recipe for pizza"
        ->
        ["pizza"]
    """

    text = user_request.strip()

    patterns = [
        r"give me recipes? (?:of|for)\s+",
        r"generate recipes? (?:of|for)\s+",
        r"make recipes? (?:of|for)\s+",
        r"i want recipes? (?:of|for)\s+",
        r"recipes? (?:of|for)\s+",
    ]

    for pattern in patterns:

        new_text = re.sub(
            pattern,
            "",
            text,
            flags=re.IGNORECASE,
        )

        if new_text != text:
            text = new_text
            break

    # Convert:
    #
    # pizza and pasta
    #
    # into:
    #
    # pizza, pasta

    text = re.sub(
        r"\s+and\s+",
        ",",
        text,
        flags=re.IGNORECASE,
    )

    dishes = [
        dish.strip().rstrip(".!?")
        for dish in text.split(",")
        if dish.strip()
    ]

    return dishes


# ============================================================
# ORCHESTRATOR
# ============================================================

def orchestrator(state: RecipeState):
    """
    Determine the dishes that need recipes.

    The orchestrator does NOT assign dishes to fixed chefs.

    The generic chef node handles dishes dynamically.

    Example:

        1 dish
        ->
        dishes = ["pizza"]

        3 dishes
        ->
        dishes = ["pizza", "burger", "pasta"]

        10 dishes
        ->
        dishes = [...]
    """

    logger.info("Orchestrator started")

    logger.info(
        "Input mode: %s",
        state.input_mode,
    )

    # ========================================================
    # 1. IMAGE INPUT
    # ========================================================

    if state.input_mode == "image":

        logger.info(
            "Image mode detected"
        )

        if not state.image_dish:

            logger.error(
                "Image mode detected but image_dish is empty"
            )

            raise ValueError(
                "Could not identify the dish from the image."
            )

        dish_name = state.image_dish.strip()

        if not dish_name:

            raise ValueError(
                "Could not identify a valid dish from the image."
            )

        dishes = [
            dish_name.rstrip(".!?")
        ]

        logger.info(
            "Vision identified dish: %s",
            dishes[0],
        )

    # ========================================================
    # 2. MOOD / RECOMMENDATION INPUT
    # ========================================================

    elif state.input_mode == "recommendation":

        logger.info(
            "Recommendation mode detected"
        )

        dishes = [
            dish.strip().rstrip(".!?")
            for dish in state.dishes
            if dish and dish.strip()
        ]

        logger.info(
            "Using recommendation dishes: %s",
            dishes,
        )

    # ========================================================
    # 3. EXPLICIT RECIPE REQUEST
    # ========================================================

    elif state.input_mode == "explicit":

        logger.info(
            "Explicit recipe request detected"
        )

        dishes = extract_dishes(
            state.user_request
        )

        logger.info(
            "Extracted dishes from user request: %s",
            dishes,
        )

    # ========================================================
    # 4. UNKNOWN INPUT MODE
    # ========================================================

    else:

        logger.error(
            "Unknown input mode: %s",
            state.input_mode,
        )

        raise ValueError(
            f"Unsupported input mode: {state.input_mode}"
        )

    # ========================================================
    # VALIDATION
    # ========================================================

    if not dishes:

        raise ValueError(
            "Please provide at least one dish."
        )

    # Remove duplicates while preserving order.

    dishes = list(
        dict.fromkeys(dishes)
    )

    logger.info(
        "Final dishes: %s",
        dishes,
    )

    logger.info(
        "Number of dishes: %d",
        len(dishes),
    )

    # ========================================================
    # RESET CHEF PROGRESS
    # ========================================================

    return {
        "dishes": dishes,
        "current_dish_index": 0,
        "recipes": [],
        "chef_usage": [],
        "next_step": "chef",
    }

