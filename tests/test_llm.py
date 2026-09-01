from src.recipe_generator.config import TEXT_MODEL
from src.recipe_generator.llm import get_text_model


def main():

    print("=" * 60)
    print("LLM FACTORY TEST")
    print("=" * 60)

    print("\nMODEL:")
    print(TEXT_MODEL)

    llm = get_text_model()

    print("\nLLM:")
    print(type(llm).__name__)

    response = llm.invoke(
        "Return only this JSON: "
        '{"message": "Groq is working"}'
    )

    print("\nCONTENT:")
    print(response.content)

    print("\nMETADATA:")
    print(response.response_metadata)


if __name__ == "__main__":
    main()