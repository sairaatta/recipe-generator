import logging
import sys
from pathlib import Path


# Make sure the project root is available when running
# the test directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.recipe_generator.config import TEXT_MODEL
from src.recipe_generator.generator import generate_recipe


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)


def main():

    print("=" * 60)
    print("STEP 3 - GENERATOR + OPENROUTER TEST")
    print("=" * 60)

    print()
    print("MODEL:")
    print(TEXT_MODEL)

    print()
    print("Generating recipe...")
    print()

    recipe, usage = generate_recipe(
        dish="chicken pasta",
        chef_name="Chef Test",
        chef_style=(
            "classic, practical, simple home cooking"
        ),
        research=(
            "Chicken pasta commonly uses pasta, chicken, "
            "garlic, olive oil, herbs, and a simple sauce."
        ),
    )

    print()
    print("=" * 60)
    print("RECIPE GENERATED SUCCESSFULLY")
    print("=" * 60)

    print()
    print("NAME:")
    print(recipe.name)

    print()
    print("DESCRIPTION:")
    print(recipe.description)

    print()
    print("INGREDIENTS:")

    for ingredient in recipe.ingredients:
        print(
            f"- {ingredient.quantity} "
            f"{ingredient.name}"
        )

    print()
    print("INSTRUCTIONS:")

    for index, instruction in enumerate(
        recipe.instructions,
        start=1,
    ):
        print(
            f"{index}. {instruction}"
        )

    print()
    print("COOKING TIME:")
    print(
        f"{recipe.cooking_time_minutes} minutes"
    )

    print()
    print("SERVINGS:")
    print(recipe.servings)

    print()
    print("=" * 60)
    print("TOKEN USAGE")
    print("=" * 60)

    print(
        f"Input tokens:  "
        f"{usage['input_tokens']}"
    )

    print(
        f"Output tokens: "
        f"{usage['output_tokens']}"
    )

    print(
        f"Total tokens:  "
        f"{usage['total_tokens']}"
    )

    print()
    print("=" * 60)
    print("STEP 3 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()