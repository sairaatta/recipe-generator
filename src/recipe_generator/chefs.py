import logging
import time

from .generator import generate_recipe
from .state import RecipeState


logger = logging.getLogger(__name__)


def generate_chef_recipe(
    state: RecipeState,
    dish: str,
    chef_name: str,
    chef_style: str,
):
    """
    Generate one recipe and capture its token usage.

    The research for the current dish is retrieved from
    state.research using current_dish_index.
    """

    start_time = time.perf_counter()

    logger.info(
        "%s started for dish: %s",
        chef_name,
        dish,
    )

    if not dish or not dish.strip():
        raise ValueError(
            f"{chef_name}: dish cannot be empty."
        )

    # ============================================================
    # GET RESEARCH FOR CURRENT DISH
    # ============================================================

    research = None

    if state.current_dish_index < len(state.research):
        research = state.research[
            state.current_dish_index
        ]

        logger.info(
            "%s using research for dish: %s",
            chef_name,
            dish,
        )
    else:
        logger.warning(
            "%s: no research available for dish: %s",
            chef_name,
            dish,
        )

    # ============================================================
    # GENERATE RECIPE
    # ============================================================

    recipe, usage = generate_recipe(
        dish=dish,
        chef_name=chef_name,
        chef_style=chef_style,
        research=research,
    )

    elapsed = time.perf_counter() - start_time

    logger.info(
        "%s finished: %s in %.2f seconds",
        chef_name,
        recipe.name,
        elapsed,
    )

    logger.info(
        "%s token usage | input=%d | output=%d | total=%d",
        chef_name,
        usage["input_tokens"],
        usage["output_tokens"],
        usage["total_tokens"],
    )

    return recipe, usage


def chef_node(state: RecipeState) -> RecipeState:
    """
    Generic sequential chef node.

    Processes exactly one dish per call.

    Example:

        dishes = ["pizza", "burger"]

        First call:
            Chef 1 -> pizza

        Second call:
            Chef 2 -> burger
    """

    # ============================================================
    # CHECK WHETHER ALL DISHES ARE PROCESSED
    # ============================================================

    if state.current_dish_index >= len(state.dishes):

        logger.info(
            "All dishes have already been processed. "
            "Total dishes: %d",
            len(state.dishes),
        )

        state.next_step = "summarizer"

        return state

    # ============================================================
    # GET CURRENT DISH
    # ============================================================

    dish = state.dishes[
        state.current_dish_index
    ]

    chef_number = (
        state.current_dish_index + 1
    )

    chef_name = f"Chef {chef_number}"

    # ============================================================
    # CHEF STYLE
    # ============================================================

    chef_style = (
        "Professional, practical and delicious cooking. "
        "Create a clear and reliable recipe that matches "
        "the user's requested dish."
    )

    logger.info(
        "%s processing dish %d/%d: %s",
        chef_name,
        state.current_dish_index + 1,
        len(state.dishes),
        dish,
    )

    # ============================================================
    # GENERATE RECIPE
    # ============================================================

    try:

        recipe, usage = generate_chef_recipe(
            state=state,
            dish=dish,
            chef_name=chef_name,
            chef_style=chef_style,
        )

    except Exception as exc:

        logger.exception(
            "%s failed while generating recipe for: %s",
            chef_name,
            dish,
        )

        state.status = "failed"

        state.error = (
            f"{chef_name} failed for "
            f"'{dish}': {exc}"
        )

        state.next_step = None

        return state

    # ============================================================
    # STORE RECIPE
    # ============================================================

    state.recipes.append(recipe)

    logger.info(
        "%s recipe stored: %s",
        chef_name,
        recipe.name,
    )

    # ============================================================
    # STORE TOKEN USAGE
    # ============================================================

    state.chef_usage.append(usage)

    logger.info(
        "%s usage stored. Total usage records: %d",
        chef_name,
        len(state.chef_usage),
    )

    # ============================================================
    # MOVE TO NEXT DISH
    # ============================================================

    state.current_dish_index += 1

    logger.info(
        "Chef progress: %d/%d dishes completed",
        state.current_dish_index,
        len(state.dishes),
    )

    # ============================================================
    # DETERMINE NEXT STEP
    # ============================================================

    if (
        state.current_dish_index
        < len(state.dishes)
    ):

        state.next_step = "chef"

        logger.info(
            "More dishes remain. "
            "Next dish: %s",
            state.dishes[
                state.current_dish_index
            ],
        )

    else:

        state.next_step = "summarizer"

        logger.info(
            "All dishes completed. "
            "Moving to summarizer.",
        )

    state.status = "in_progress"

    return state

