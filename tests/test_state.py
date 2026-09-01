from src.recipe_generator.state import RecipeState


def main():

    print("=" * 60)
    print("STEP 4 - RECIPE STATE TEST")
    print("=" * 60)

    state = RecipeState(
        user_request="Give me recipes for pizza, burger and pasta."
    )

    print("\nINITIAL STATE:")
    print(state)

    # --------------------------------------------------
    # TEST DYNAMIC DISHES
    # --------------------------------------------------

    state.dishes = [
        "pizza",
        "burger",
        "pasta",
    ]

    print("\nDISHES:")
    print(state.dishes)

    # --------------------------------------------------
    # TEST RECIPE LIST
    # --------------------------------------------------

    print("\nRECIPES:")
    print(state.recipes)

    # --------------------------------------------------
    # TEST INDEX
    # --------------------------------------------------

    print("\nCURRENT DISH INDEX:")
    print(state.current_dish_index)

    # --------------------------------------------------
    # TEST TOKEN USAGE
    # --------------------------------------------------

    state.chef_usage.append(
        {
            "input": 300,
            "output": 500,
            "total": 800,
        }
    )

    print("\nCHEF USAGE:")
    print(state.chef_usage)

    # --------------------------------------------------
    # TEST FINAL SUMMARY
    # --------------------------------------------------

    print("\nFINAL SUMMARY:")
    print(state.final_summary)

    # --------------------------------------------------
    # ASSERTIONS
    # --------------------------------------------------

    assert state.user_request == (
        "Give me recipes for pizza, burger and pasta."
    )

    assert len(state.dishes) == 3

    assert state.dishes[0] == "pizza"
    assert state.dishes[1] == "burger"
    assert state.dishes[2] == "pasta"

    assert state.recipes == []

    assert state.current_dish_index == 0

    assert len(state.chef_usage) == 1

    assert state.chef_usage[0]["total"] == 800

    assert state.final_summary is None

    assert state.status == "pending"

    print("\n" + "=" * 60)
    print("STEP 4 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()