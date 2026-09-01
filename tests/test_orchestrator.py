
from src.recipe_generator.orchestrator import (
    orchestrator,
)
from src.recipe_generator.state import RecipeState


def test_explicit_multiple_dishes():

    state = RecipeState(
        user_request=(
            "Give me recipes for "
            "pizza, burger and pasta."
        ),
        input_mode="explicit",
    )

    result = orchestrator(state)

    print("\n" + "=" * 60)
    print("STEP 7 - DYNAMIC ORCHESTRATOR TEST")
    print("=" * 60)

    print("\nINPUT:")
    print(state.user_request)

    print("\nEXTRACTED DISHES:")

    for i, dish in enumerate(
        result["dishes"],
        start=1,
    ):
        print(f"{i}. {dish}")

    print("\nCURRENT INDEX:")
    print(
        result["current_dish_index"]
    )

    print("\nRECIPES:")
    print(
        result["recipes"]
    )

    print("\nCHEF USAGE:")
    print(
        result["chef_usage"]
    )

    print("\nNEXT STEP:")
    print(
        result["next_step"]
    )

    # --------------------------------------------------
    # Assertions
    # --------------------------------------------------

    assert result["dishes"] == [
        "pizza",
        "burger",
        "pasta",
    ]

    assert result["current_dish_index"] == 0

    assert result["recipes"] == []

    assert result["chef_usage"] == []

    assert result["next_step"] == "chef"

    print("\n" + "=" * 60)
    print("STEP 7 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_explicit_multiple_dishes()

