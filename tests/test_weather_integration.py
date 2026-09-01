from src.recipe_generator.graph import build_recipe_graph
from src.recipe_generator.state import RecipeState


def run_test(title: str, user_request: str):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"\nRequest:")
    print(user_request)

    graph = build_recipe_graph()

    state = RecipeState(
        user_request=user_request
    )

    final_state = graph.invoke(state)

    print("\nInput mode:")
    print(final_state["input_mode"])

    print("\nWeather context:")
    print(final_state["weather_context"])

    print("\nDishes:")
    print(final_state["dishes"])

    return final_state


def main():

    print("=" * 60)
    print("PHASE 12 - CONDITIONAL WEATHER INTEGRATION TEST")
    print("=" * 60)

    # ==================================================
    # TEST 1: NO LOCATION
    # ==================================================

    state_1 = run_test(
        "TEST 1 - NO LOCATION",
        "I am feeling sad, suggest me something to eat.",
    )

    assert state_1["input_mode"] == "recommendation"

    assert state_1["weather_context"] is None

    print("\n✓ Test 1 passed")
    print("✓ Recommendation detected")
    print("✓ No location detected")
    print("✓ Weather was skipped")

    # ==================================================
    # TEST 2: LOCATION PRESENT
    # ==================================================

    state_2 = run_test(
        "TEST 2 - LOCATION PRESENT",
        "I am in Miami and feeling sad, suggest me something to eat.",
    )

    assert state_2["input_mode"] == "recommendation"

    assert state_2["weather_context"] is not None

    assert state_2["weather_context"]["location"]

    print("\n✓ Test 2 passed")
    print("✓ Recommendation detected")
    print("✓ Location detected")
    print("✓ Weather context retrieved")

    # ==================================================
    # TEST 3: EXPLICIT RECIPE
    # ==================================================

    state_3 = run_test(
        "TEST 3 - EXPLICIT RECIPE",
        "Give me a simple chicken pasta recipe for two people.",
    )

    assert state_3["input_mode"] == "explicit"

    assert state_3["weather_context"] is None

    print("\n✓ Test 3 passed")
    print("✓ Explicit recipe request detected")
    print("✓ Weather was skipped")

    # ==================================================
    # FINAL
    # ==================================================

    print("\n" + "=" * 60)
    print("✓ PHASE 12 WEATHER INTEGRATION TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()