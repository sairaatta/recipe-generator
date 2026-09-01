import json
import logging

from .llm import get_text_model

logger = logging.getLogger(__name__)


def recommend_dishes(
    user_request: str,
    weather: str,
) -> list[str]:

    logger.info(
        "Generating dishes from mood + weather"
    )

    prompt = f"""
You are a food recommendation assistant.

User request:
{user_request}

Current weather:
{weather}

Suggest exactly 1 to 3 recipes that fit the
user's request, mood and current weather.

Return ONLY a JSON array of recipe names.

Example:

[
    "Chicken Tacos",
    "Loaded Fries",
    "Mango Salsa"
]

Rules:
- Return 1 to 3 recipes.
- Return recipe names only.
- Do not provide ingredients.
- Do not provide instructions.
- Do not explain.
- Return ONLY valid JSON.
"""

    model = get_text_model()

    response = model.invoke(prompt)

    content = response.content

    if not isinstance(content, str):
        raise ValueError(
            "Invalid recommendation response."
        )

    dishes = json.loads(content)

    if not isinstance(dishes, list):
        raise ValueError(
            "Recommendation response must be a list."
        )

    dishes = [
        str(dish).strip()
        for dish in dishes
        if str(dish).strip()
    ]

    if not 1 <= len(dishes) <= 3:
        raise ValueError(
            "Recommendation must contain 1 to 3 dishes."
        )

    logger.info(
        "Recommended dishes: %s",
        dishes,
    )

    return dishes