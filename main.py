import logging
import os

from src.recipe_generator.logging_config import setup_logging
from src.recipe_generator.graph import build_recipe_graph
from src.recipe_generator.state import RecipeState


setup_logging()

logger = logging.getLogger(__name__)


def get_optional_image_path() -> str | None:
    """
    Prompts the user for an optional image path.
    Returns a validated path, or None if the user skips it
    or provides an invalid path.
    """

    image_path = input(
        "Add an image for reference (optional, press Enter to skip): "
    ).strip()

    if not image_path:
        logger.info("No image provided by user")
        return None

    if not os.path.isfile(image_path):
        logger.warning(
            "Provided image path does not exist, skipping: %s",
            image_path,
        )
        print(
            f"Warning: could not find '{image_path}'. "
            "Continuing without an image."
        )
        return None

    logger.info("Received image path: %s", image_path)
    return image_path


def main():

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    logger = logging.getLogger(__name__)

    logger.info("Application started")

    user_request = input(
        "What recipe would you like: "
    ).strip()

    logger.info(
        "Received user request: %s",
        user_request,
    )

    image_path = get_optional_image_path()

    logger.info("Building recipe graph")

    graph = build_recipe_graph()

    logger.info("Starting recipe workflow")

    initial_state = RecipeState(
        user_request=user_request,
        image_path=image_path,
    )

    final_state = graph.invoke(
        initial_state
    )

    logger.info(
        "Recipe workflow completed"
    )

    # ==================================================
    # DISPLAY RECIPES
    # ==================================================

    print()
    print("=" * 70)
    print("                         CHEF RECIPES")
    print("=" * 70)

    recipes = [
        (
            "Chef Classic",
            final_state.get("chef_a_recipe"),
        ),
        (
            "Chef Healthy",
            final_state.get("chef_b_recipe"),
        ),
        (
            "Chef Creative",
            final_state.get("chef_c_recipe"),
        ),
    ]

    for chef_name, recipe in recipes:

        if recipe is None:
            continue

        print()
        print("=" * 70)
        print(
            f"{chef_name}: {recipe.name}"
        )
        print("=" * 70)

        print()
        print(recipe.description)

        print()
        print(
            f"Servings: {recipe.servings}"
        )

        print(
            f"Cook time: "
            f"{recipe.cooking_time_minutes} minutes"
        )

        print()
        print("Ingredients:")

        for ingredient in recipe.ingredients:
            print(
                f" - "
                f"{ingredient.quantity} "
                f"{ingredient.name}"
            )

        print()
        print("Instructions:")

        for index, instruction in enumerate(
            recipe.instructions,
            start=1,
        ):
            print(
                f"{index}. {instruction}"
            )

    # ==================================================
    # TOKEN COST ESTIMATES
    # ==================================================

    print()
    print("=" * 70)
    print("                    TOKEN COST ESTIMATES")
    print("=" * 70)

    cost_estimates = final_state.get(
        "cost_estimates",
        {},
    )

    for chef_name, data in cost_estimates.items():

        print()
        print(f"{chef_name}:")

        print(
            f"  Input tokens:  "
            f"{data['input_tokens']}"
        )

        print(
            f"  Output tokens: "
            f"{data['output_tokens']}"
        )

        print(
            f"  Total tokens:  "
            f"{data['total_tokens']}"
        )

        print(
            f"  Estimated cost: "
            f"${data['estimated_cost']:.6f}"
        )

    logger.info(
        "Application complete successfully."
    )


if __name__ == "__main__":
    main()