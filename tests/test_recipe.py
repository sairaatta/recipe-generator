from src.recipe_generator.generator import stream_recipe


def main():
    user_request = (
        "Give me a simple chicken pasta recipe "
        "for two people."
    )

    recipe = stream_recipe(user_request)

    print("=" * 60)
    print("PARSED PYDANTIC RECIPE")
    print("=" * 60)

    print(f"\nName: {recipe.name}")

    print(f"\nDescription: {recipe.description}")

    print("\nIngredients:")

    for ingredient in recipe.ingredients:
        print(
            f"- {ingredient.quantity} "
            f"{ingredient.name}"
        )

    print("\nInstructions:")

    for index, instruction in enumerate(
        recipe.instructions,
        start=1,
    ):
        print(f"{index}. {instruction}")

    print(
        f"\nCooking time: "
        f"{recipe.cooking_time_minutes} minutes"
    )

    print(f"Servings: {recipe.servings}")


if __name__ == "__main__":
    main()