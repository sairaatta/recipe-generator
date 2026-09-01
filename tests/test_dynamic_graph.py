import logging

from src.recipe_generator.graph import (
    build_recipe_graph,
)
from src.recipe_generator.state import RecipeState


def setup_logging():

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

    setup_logging()

    print("=" * 60)
    print("STEP 8 - N-DISH GRAPH TEST")
    print("=" * 60)

    state = RecipeState(
        user_request=(
            "Give me recipes for "
            "pizza, burger, pasta, tacos and noodles."
        ),
        input_mode="explicit",
    )

    print("\nINITIAL STATE:")
    print(state)

    print("\n" + "-" * 60)
    print("BUILDING GRAPH")
    print("-" * 60)

    graph = build_recipe_graph()

    print("\nGraph compiled successfully.")

    print("\n" + "-" * 60)
    print("RUNNING GRAPH")
    print("-" * 60)

    final_state = graph.invoke(state)

    print("\n" + "=" * 60)
    print("GRAPH EXECUTION RESULT")
    print("=" * 60)

    print("\nDISHES:")

    for i, dish in enumerate(
        final_state["dishes"],
        start=1,
    ):
        print(f"{i}. {dish}")

    print("\nRECIPES:")

    for i, recipe in enumerate(
        final_state["recipes"],
        start=1,
    ):
        print(f"\nRecipe {i}:")
        print(f"Name: {recipe.name}")
        print(
            f"Cooking time: "
            f"{recipe.cooking_time_minutes} minutes"
        )
        print(
            f"Servings: "
            f"{recipe.servings}"
        )

    print("\nCHEF USAGE:")

    for i, usage in enumerate(
        final_state["chef_usage"],
        start=1,
    ):
        print(
            f"Chef {i}: "
            f"input={usage.get('input_tokens', usage.get('input', 0))} | "
            f"output={usage.get('output_tokens', usage.get('output', 0))} | "
            f"total={usage.get('total_tokens', usage.get('total', 0))}"
        )

    print("\nCURRENT INDEX:")
    print(
        final_state["current_dish_index"]
    )

    print("\nSTATUS:")
    print(
        final_state["status"]
    )

    print("\nCOST ESTIMATES:")
    print(
        final_state["cost_estimates"]
    )

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert len(final_state["dishes"]) == 5

    assert len(final_state["recipes"]) == 5

    assert len(final_state["chef_usage"]) == 5

    assert (
        final_state["current_dish_index"]
        == 5
    )

    assert (
        final_state["status"]
        == "recipes_generated"
    )

    assert (
        final_state["cost_estimates"]
    )

    print("\n" + "=" * 60)
    print("STEP 8 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()

