from src.recipe_generator.llm import get_text_model


def main():

    print("=" * 60)
    print("OPENROUTER LANGCHAIN TEST")
    print("=" * 60)

    llm = get_text_model()

    response = llm.invoke(
        """
Return ONLY valid JSON.

Create a simple chicken pasta recipe for two people.

Use this exact structure:

{
    "name": "string",
    "description": "string",
    "ingredients": [],
    "instructions": [],
    "cooking_time_minutes": 30,
    "servings": 2
}
"""
    )

    print()
    print("MODEL:")
    print(response.response_metadata.get("model"))

    print()
    print("CONTENT:")
    print(response.content)

    print()
    print("METADATA:")
    print(response.response_metadata)


if __name__ == "__main__":
    main()