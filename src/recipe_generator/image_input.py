import logging

from .vision import describe_food_image

logger = logging.getLogger(__name__)


def image_input(state):
    """
    Phase 12:
    Analyze the optional image using qwen3-vl:2b.
    """

    image_path = state.image_path

    if not image_path:
        logger.info(
            "Phase 12: No image provided"
        )

        return {}

    logger.info(
        "Phase 12: Image provided: %s",
        image_path,
    )

    description = describe_food_image(
        image_path
    )

    logger.info(
        "Phase 12: Image analysis completed"
    )

    logger.info(
        "Phase 12: Image description: %s",
        description,
    )

    return {
        "image_description": description,
    }