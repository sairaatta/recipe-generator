import base64
from langchain_ollama import get_text_model


IMAGE_PATH = (
    r"C:\Users\PMLS\OneDrive\TkXel_internship"
    r"\Agentic_AI\recipe-generator\tests\images\image2.jpg"
)


def main():

    with open(IMAGE_PATH, "rb") as f:
        image_base64 = base64.b64encode(
            f.read()
        ).decode("utf-8")

    model = get_text_model(
        model="qwen3-vl:2b",
        base_url="http://localhost:11434",
        temperature=0,
        num_predict=100,
        reasoning=False,
    )

    response = model.invoke(
        [
            {
                "role": "user",
                "content": (
                    "Look carefully at this image. "
                    "What food or dish is shown? "
                    "Describe it briefly."
                ),
                "images": [image_base64],
            }
        ]
    )

    print("\n==============================")
    print("RAW RESPONSE")
    print("==============================")
    print(repr(response))

    print("\n==============================")
    print("CONTENT")
    print("==============================")
    print(repr(response.content))


if __name__ == "__main__":
    main()