import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


def main():

    print("=" * 60)
    print("GROQ CLOUD TEST")
    print("=" * 60)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set in .env"
        )

    print("\nAPI KEY:")
    print("Loaded successfully")

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
        max_tokens=700,
    )

    response = llm.invoke(
        "Give me a simple chicken pasta recipe in 3 sentences."
    )

    print("\nMODEL:")
    print("openai/gpt-oss-20b")

    print("\nRESPONSE:")
    print(response.content)

    print("\nMETADATA:")
    print(response.response_metadata)


if __name__ == "__main__":
    main()