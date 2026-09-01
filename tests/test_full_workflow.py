
import logging
import time

from src.recipe_generator.graph import build_recipe_graph
from src.recipe_generator.state import RecipeState
from src.recipe_generator.logging_config import setup_logging


def main():

    setup_logging()

    logger = logging.getLogger(__name__)

    print("=" * 60)
    print("FULL RECIPE WORKFLOW TEST")
    print("=" * 60)

    # --------------------------------------------------
    # USER REQUEST
    # --------------------------------------------------

    user_request = (
        "Give me recipes for pizza and burger."
    )

    print("\nUSER REQUEST:")
    print(user_request)

    # --------------------------------------------------
    # INITIAL STATE
    # --------------------------------------------------

    state = RecipeState(
        user_request=user_request,
    )

    print("\nINITIAL STATE:")
    print(state)

    # --------------------------------------------------
    # BUILD GRAPH
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("BUILDING GRAPH")
    print("-" * 60)

    graph = build_recipe_graph()

    print("✓ Graph built successfully")

    # --------------------------------------------------
    # RUN WORKFLOW
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("RUNNING COMPLETE WORKFLOW")
    print("-" * 60)

    start_time = time.perf_counter()

    try:

        final_state = graph.invoke(state)

    except Exception as exc:

        logger.exception(
            "Full workflow failed"
        )

        print("\n❌ WORKFLOW FAILED")
        print(f"Error: {exc}")

        raise

    elapsed = time.perf_counter() - start_time

    # --------------------------------------------------
    # FINAL STATE
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("FINAL STATE")
    print("-" * 60)

    print(f"Status: {final_state.get('status')}")
    print(f"Dishes: {final_state.get('dishes')}")
    print(
        f"Recipes generated: "
        f"{len(final_state.get('recipes', []))}"
    )
    print(
        f"Research results: "
        f"{len(final_state.get('research', []))}"
    )
    print(
        f"Usage records: "
        f"{len(final_state.get('chef_usage', []))}"
    )
    print(
        f"Current dish index: "
        f"{final_state.get('current_dish_index')}"
    )
    print(
        f"Next step: "
        f"{final_state.get('next_step')}"
    )

    # --------------------------------------------------
    # RECIPES
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("GENERATED RECIPES")
    print("-" * 60)

    recipes = final_state.get("recipes", [])

    for index, recipe in enumerate(
        recipes,
        start=1,
    ):

        print(f"\nRecipe {index}")
        print(f"Name: {recipe.name}")
        print(
            f"Cooking time: "
            f"{recipe.cooking_time_minutes} minutes"
        )
        print(
            f"Servings: "
            f"{recipe.servings}"
        )

    # --------------------------------------------------
    # COST
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("COST ESTIMATION")
    print("-" * 60)

    cost_estimates = final_state.get(
        "cost_estimates",
        {},
    )

    if cost_estimates:

        for chef_name, data in cost_estimates.items():

            if chef_name == "total":
                continue

            print(
                f"{chef_name}: "
                f"${data['estimated_cost']:.6f}"
            )

        total = cost_estimates.get("total")

        if total:

            print(
                "\nTotal estimated cost: "
                f"${total['estimated_cost']:.6f}"
            )

    else:

        print("No cost information available.")

    # --------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("PERFORMANCE")
    print("-" * 60)

    print(
        f"Total workflow time: "
        f"{elapsed:.2f} seconds"
    )

    print(
        f"Total workflow time: "
        f"{elapsed / 60:.2f} minutes"
    )

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("VALIDATION")
    print("-" * 60)

    assert final_state.get("status") != "failed"

    assert len(
        final_state.get("recipes", [])
    ) == len(
        final_state.get("dishes", [])
    )

    assert len(
        final_state.get("chef_usage", [])
    ) == len(
        final_state.get("recipes", [])
    )

    assert final_state.get(
        "current_dish_index"
    ) == len(
        final_state.get("dishes", [])
    )

    assert cost_estimates

    print("✓ Workflow completed")
    print("✓ All dishes processed")
    print("✓ All recipes generated")
    print("✓ Chef usage recorded")
    print("✓ Cost estimation completed")
    print("✓ Sequential execution validated")

    print("\n" + "=" * 60)
    print("✓ FULL WORKFLOW TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()

