from pathlib import Path

from src.recipe_generator.vision import identify_dish


image_path = Path("tests/images/Bulgogi-bibimbap-recipe.jpg")

if not image_path.exists():
    raise FileNotFoundError(
        f"Test image not found: {image_path.resolve()}"
    )

print("=" * 60)
print("VISION TEST")
print("=" * 60)
print(f"Testing image: {image_path.resolve()}")

result = identify_dish(str(image_path))

print(f"\nIdentified dish: {result}")