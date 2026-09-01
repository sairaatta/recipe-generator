import logging

from src.recipe_generator.graph import build_recipe_graph
from src.recipe_generator.state import RecipeState


# ------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main():

    print("=" * 60)
    print("STEP 6 - LANGGRAPH GENERIC CHEF FLOW TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------------

    state = RecipeState(
        user_request="Give me recipes for pizza and burger.",
        input_mode="explicit",
    )

    print("\nINITIAL STATE:")
    print(state)

    # --------------------------------------------------------
    # BUILD GRAPH
    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("BUILDING GRAPH")
    print("-" * 60)

    graph = build_recipe_graph()

    print("\nGraph compiled successfully.")

    # --------------------------------------------------------
    # RUN GRAPH
    # --------------------------------------------------------

    print("\n" + "-" * 60)
    print("RUNNING GRAPH")
    print("-" * 60)

    result = graph.invoke(state)

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("GRAPH EXECUTION RESULT")
    print("=" * 60)

    print("\nDISHES:")

    print("\nRECIPES:")
    for i, recipe in enumerate(result["recipes"], start=1):

        print(f"\nRecipe {i}:")
        print(f"Name: {recipe.name}")
        print(
            f"Cooking time: {recipe.cooking_time_minutes} minutes"
        )
        print(f"Servings: {recipe.servings}")

    # --------------------------------------------------------
    # USAGE
    # --------------------------------------------------------

    print("\nCHEF USAGE:")

    for i, usage in enumerate(
        result.get("chef_usage", []),
        start=1,
    ):
        print(
            f"Chef {i}: "
            f"input={usage['input_tokens']} | "
            f"output={usage['output_tokens']} | "
            f"total={usage['total_tokens']}"
        )

    # --------------------------------------------------------
    # COST
    # --------------------------------------------------------

    print("\nCOST ESTIMATES:")
    print(result.get("cost_estimates", {}))

    # --------------------------------------------------------
    # FINAL STATE
    # --------------------------------------------------------

    print("\nFINAL STATE:")
    print(f"Current index: {result['current_dish_index']}")
    print(f"Number of dishes: {len(result['dishes'])}")
    print(f"Number of recipes: {len(result['recipes'])}")
    print(f"Status: {result['status']}")
    print(f"Next step: {result['next_step']}")

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    assert len(result["dishes"]) == 2

    assert len(result["recipes"]) == 2

    assert result["current_dish_index"] == 2

    assert len(result.get("chef_usage", [])) == 2

    assert result["status"] == "completed"

    assert result["next_step"] == "summarizer"

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 6 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()