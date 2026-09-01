import logging
import time

from .input_router import detect_input_mode
from .weather import get_weather
from .recommendation import recommend_dishes
from .state import RecipeState
from .vision import identify_dish


logger = logging.getLogger(__name__)


def input_decision(state: RecipeState):

    logger.info(
        "Phase 12: Input decision started"
    )

    # ==========================================================
    # OPTION 1: SINGLE IMAGE INPUT
    # ==========================================================

    if state.image_path:

        logger.info(
            "Image input detected"
        )

        start_time = time.perf_counter()

        try:

            dish_name = identify_dish(
                state.image_path
            )

        except Exception:

            logger.exception(
                "Vision dish identification failed"
            )

            raise

        elapsed = (
            time.perf_counter()
            - start_time
        )

        logger.info(
            "Vision dish identification completed "
            "in %.2f seconds",
            elapsed,
        )

        logger.info(
            "Identified dish: %s",
            dish_name,
        )

        if (
            not dish_name
            or dish_name.lower().strip() == "unknown"
        ):

            logger.warning(
                "Vision model could not identify "
                "the uploaded food image."
            )

            return {
                "input_mode": "image",
                "image_dish": "unknown",
                "dishes": [],
            }

        return {
            "input_mode": "image",
            "image_dish": dish_name,
            "dishes": [dish_name],
        }

    # ==========================================================
    # TEXT INPUT
    # ==========================================================

    user_request = state.user_request.strip()

    if not user_request:

        raise ValueError(
            "Please provide a recipe request, mood, "
            "or food image."
        )

    # ==========================================================
    # DETECT INPUT
    # ==========================================================

    result = detect_input_mode(
        user_request
    )

    mode = result.get(
        "mode",
        "explicit",
    )

    location = result.get(
        "location"
    )

    mood = result.get(
        "mood"
    )

    logger.info(
        "Input detection result: %s",
        result,
    )

    # ==========================================================
    # EXPLICIT RECIPE REQUEST
    # ==========================================================

    if mode == "explicit":

        logger.info(
            "Explicit recipe request detected"
        )

        logger.info(
            "Weather tool skipped for explicit request"
        )

        return {
            "input_mode": "explicit",
            "weather_context": None,
        }

    # ==========================================================
    # MOOD / RECOMMENDATION REQUEST
    # ==========================================================

    logger.info(
        "Mood/recommendation request detected"
    )

    logger.info(
        "Mood detected: %s",
        mood,
    )

    logger.info(
        "Location detected: %s",
        location,
    )

    weather = None

    # ==========================================================
    # CONDITIONAL WEATHER
    # ==========================================================

    if location:

        logger.info(
            "Location detected: %s",
            location,
        )

        logger.info(
            "Calling weather tool for location: %s",
            location,
        )

        try:

            weather = get_weather(
                location
            )

            logger.info(
                "Weather context retrieved: %s",
                weather,
            )

        except Exception as exc:

            # ==================================================
            # IMPORTANT
            #
            # Weather failure should NOT stop recipe generation.
            # ==================================================

            logger.warning(
                "Weather lookup failed for '%s': %s",
                location,
                exc,
            )

            weather = None

            logger.info(
                "Continuing recommendation workflow "
                "without weather context."
            )

    else:

        logger.info(
            "No location detected. "
            "Skipping weather tool."
        )

    # ==========================================================
    # RECOMMEND DISHES
    # ==========================================================

    dishes = recommend_dishes(
        user_request=user_request,
        weather=weather,
    )

    logger.info(
        "Recommended dishes: %s",
        dishes,
    )

    # ==========================================================
    # RETURN
    # ==========================================================

    return {
        "input_mode": "recommendation",
        "weather_context": weather,
        "dishes": dishes,
    }