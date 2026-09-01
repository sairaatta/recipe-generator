from src.recipe_generator.logging_config import setup_logging
from src.recipe_generator.recipe_service import (
    generate_recipe_from_state,
)
from src.recipe_generator.state import RecipeState


def main():
    setup_logging()

    state = RecipeState(
        user_request="Give me a simple chicken pasta recipe for two people."
    )

    print("\nInitial state:")
    print(state)

    state = generate_recipe_from_state(state)

    print("\nFinal state:")
    print(state)

    if state.recipe:
        print("\nGenerated recipe:")
        print(f"Name: {state.recipe.name}")
        print(
            f"Cooking time: "
            f"{state.recipe.cooking_time_minutes} minutes"
        )
        print(f"Servings: {state.recipe.servings}")


if __name__ == "__main__":
    main()