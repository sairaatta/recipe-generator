from src.recipe_generator.chefs import chef_node
from src.recipe_generator.state import RecipeState


def main():

    print("=" * 60)
    print("STEP 5 - GENERIC CHEF NODE TEST")
    print("=" * 60)

    # --------------------------------------------------
    # CREATE STATE
    # --------------------------------------------------

    state = RecipeState(
        user_request=(
            "Give me recipes for pizza and burger."
        )
    )

    state.dishes = [
        "pizza",
        "burger",
    ]

    print("\nINITIAL STATE:")
    print(state)

    # --------------------------------------------------
    # CHEF 1
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("RUNNING CHEF 1")
    print("-" * 60)

    state = chef_node(state)

    print("\nAFTER CHEF 1:")

    print(
        "Current index:",
        state.current_dish_index,
    )

    print(
        "Recipes:",
        len(state.recipes),
    )

    print(
        "Usage records:",
        len(state.chef_usage),
    )

    print(
        "Next step:",
        state.next_step,
    )

    assert len(state.recipes) == 1

    assert len(state.chef_usage) == 1

    assert state.current_dish_index == 1

    assert state.next_step == "chef"

    assert state.status == "in_progress"

    # --------------------------------------------------
    # CHEF 2
    # --------------------------------------------------

    print("\n" + "-" * 60)
    print("RUNNING CHEF 2")
    print("-" * 60)

    state = chef_node(state)

    print("\nAFTER CHEF 2:")

    print(
        "Current index:",
        state.current_dish_index,
    )

    print(
        "Recipes:",
        len(state.recipes),
    )

    print(
        "Usage records:",
        len(state.chef_usage),
    )

    print(
        "Next step:",
        state.next_step,
    )

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    assert len(state.recipes) == 2

    assert len(state.chef_usage) == 2

    assert state.current_dish_index == 2

    assert state.next_step == "summarizer"

    assert state.status == "in_progress"

    assert state.error is None

    # --------------------------------------------------
    # DISPLAY RECIPES
    # --------------------------------------------------

    print("\nGENERATED RECIPES:")

    for index, recipe in enumerate(
        state.recipes,
        start=1,
    ):

        print(f"\nRecipe {index}:")
        print(f"Name: {recipe.name}")
        print(
            f"Cooking time: "
            f"{recipe.cooking_time_minutes} minutes"
        )
        print(f"Servings: {recipe.servings}")

    # --------------------------------------------------
    # DISPLAY USAGE
    # --------------------------------------------------

    print("\nTOKEN USAGE:")

    for index, usage in enumerate(
        state.chef_usage,
        start=1,
    ):

        print(
            f"Chef {index}: "
            f"input={usage['input_tokens']} | "
            f"output={usage['output_tokens']} | "
            f"total={usage['total_tokens']}"
        )

    # --------------------------------------------------
    # FINAL
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 5 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()