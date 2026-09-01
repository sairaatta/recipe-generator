import logging
import time
import json

from .config import TEXT_MODEL
from .llm import get_text_model
from .recipe import Recipe


logger = logging.getLogger(__name__)


def _build_prompt(
    recipe_input: str,
    chef_name: str,
    chef_style: str,
    research: str | None,
    image_mode: bool = False,
) -> str:
    """
    Build a compact prompt for fast recipe generation.

    The prompt is intentionally kept small because the project
    uses sequential LLM execution and max_tokens=700.
    """

    # ============================================================
    # SOURCE SECTION
    # ============================================================

    if image_mode:

        source_section = f"""
IMAGE ANALYSIS:
{recipe_input}

IMPORTANT IMAGE RECIPE RULES:
- Identify the complete dish from the image analysis.
- Generate a recipe for THAT dish.
- Preserve visible ingredients when reasonably possible.
- Do not replace the dish with one of its ingredients.
- Do not generate a completely different dish.
"""

    else:

        source_section = f"""
ASSIGNED DISH:
{recipe_input}
"""

    # ============================================================
    # LIMIT MCP RESEARCH
    # ============================================================

    research_text = (
        research[:1500]
        if research
        else "No research available."
    )

    # ============================================================
    # FINAL PROMPT
    # ============================================================

    return f"""
You are {chef_name}, a professional recipe generator.

STYLE:
{chef_style}

{source_section}

RESEARCH:
{research_text}

Create ONE realistic recipe.

Requirements:
- Create ONE realistic recipe.
- Use exactly 5 ingredients.
- Use exactly 5 short instructions.
- Description must be under 12 words.
- cooking_time_minutes must be an integer.
- servings must be an integer.
- Do not create another dish.
- Do not add explanations.
- Do not use markdown.

Return ONLY valid JSON:

{{
  "name": "string",
  "description": "string",
  "ingredients": [
    {{"name": "string", "quantity": "string"}},
    {{"name": "string", "quantity": "string"}},
    {{"name": "string", "quantity": "string"}},
    {{"name": "string", "quantity": "string"}},
    {{"name": "string", "quantity": "string"}}
  ],
  "instructions": [
    "short step",
    "short step",
    "short step",
    "short step",
    "short step"
  ],
  "cooking_time_minutes": 30,
  "servings": 2
}}

IMPORTANT:
- Return the COMPLETE JSON object.
- End the response with }}.
- No text before or after the JSON.
"""


def _extract_token_usage(
    response: object,
) -> dict[str, int]:
    """
    Extract token usage from the LangChain ChatGroq response.
    """

    metadata = (
        getattr(
            response,
            "response_metadata",
            None,
        )
        or {}
    )

    logger.info(
        "Response metadata | model=%s | provider=%s",
        metadata.get(
            "model_name",
            TEXT_MODEL,
        ),
        metadata.get(
            "model_provider",
            "unknown",
        ),
    )

    token_usage = (
        metadata.get(
            "token_usage",
            {},
        )
        or {}
    )

    input_tokens = int(
        token_usage.get(
            "prompt_tokens",
            0,
        )
        or 0
    )

    output_tokens = int(
        token_usage.get(
            "completion_tokens",
            0,
        )
        or 0
    )

    total_tokens = int(
        token_usage.get(
            "total_tokens",
            0,
        )
        or (
            input_tokens
            + output_tokens
        )
    )

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def _clean_json_response(
    content: str,
) -> str:
    """
    Clean common formatting issues from model output.

    Handles:
    - Markdown code fences
    - Extra text before/after JSON
    """

    content = content.strip()

    if not content:
        return content

    # ============================================================
    # REMOVE MARKDOWN CODE FENCES
    # ============================================================

    if content.startswith("```"):

        lines = content.splitlines()

        if (
            lines
            and lines[0].startswith("```")
        ):
            lines = lines[1:]

        if (
            lines
            and lines[-1].strip() == "```"
        ):
            lines = lines[:-1]

        content = "\n".join(
            lines
        ).strip()

    # ============================================================
    # EXTRACT JSON OBJECT
    # ============================================================

    start = content.find("{")
    end = content.rfind("}")

    if (
        start != -1
        and end != -1
        and end > start
    ):
        content = content[
            start : end + 1
        ]

    return content.strip()


def generate_recipe(
    dish: str,
    chef_name: str,
    chef_style: str,
    research: str | None,
    image_mode: bool = False,
) -> tuple[
    Recipe,
    dict[str, int],
]:
    """
    Generate one structured recipe using the configured
    Groq model.
    """

    logger.info(
        "%s generating recipe for: %s",
        chef_name,
        dish,
    )

    # ============================================================
    # VALIDATE DISH
    # ============================================================

    if not dish or not dish.strip():

        raise ValueError(
            "Dish cannot be empty."
        )

    # ============================================================
    # GET MODEL
    # ============================================================

    model = get_text_model()

    logger.info(
        "%s using model: %s",
        chef_name,
        TEXT_MODEL,
    )

    # ============================================================
    # BUILD PROMPT
    # ============================================================

    prompt = _build_prompt(
        recipe_input=dish,
        chef_name=chef_name,
        chef_style=chef_style,
        research=research,
        image_mode=image_mode,
    )

    logger.info(
        "%s prompt size: %d characters",
        chef_name,
        len(prompt),
    )

    # ============================================================
    # MODEL CALL
    # ============================================================

    start_time = time.perf_counter()

    try:

        response = model.invoke(
            prompt
        )

    except Exception:

        elapsed = (
            time.perf_counter()
            - start_time
        )

        logger.exception(
            "%s model generation failed "
            "after %.2f seconds",
            chef_name,
            elapsed,
        )

        raise

    elapsed = (
        time.perf_counter()
        - start_time
    )

    logger.info(
        "%s generation completed in %.2f "
        "seconds using %s",
        chef_name,
        elapsed,
        TEXT_MODEL,
    )

    # ============================================================
    # TOKEN USAGE
    # ============================================================

    usage = _extract_token_usage(
        response
    )

    logger.info(
        "%s token usage | input=%d | output=%d | total=%d",
        chef_name,
        usage["input_tokens"],
        usage["output_tokens"],
        usage["total_tokens"],
    )

    # ============================================================
    # RESPONSE CONTENT
    # ============================================================

    content = getattr(
        response,
        "content",
        None,
    )

    if not isinstance(
        content,
        str,
    ):

        raise ValueError(
            f"{chef_name} returned "
            "unexpected content format."
        )

    content = content.strip()

    logger.info(
        "%s response size: %d characters",
        chef_name,
        len(content),
    )

    if not content:

        raise ValueError(
            f"{chef_name} returned "
            "an empty response."
        )

    logger.info(
        "%s raw response:\n%s",
        chef_name,
        content,
    )

    # ============================================================
    # CLEAN JSON
    # ============================================================

    content = _clean_json_response(
        content
    )

    logger.info(
        "%s cleaned JSON size: %d characters",
        chef_name,
        len(content),
    )

    # ============================================================
    # JSON VALIDATION
    # ============================================================

    try:

        json.loads(
            content
        )

    except json.JSONDecodeError as exc:

        logger.error(
            "%s returned invalid JSON.",
            chef_name,
        )

        logger.error(
            "Raw model response:\n%s",
            content,
        )

        raise ValueError(
            f"{chef_name} generated "
            "invalid JSON."
        ) from exc

    # ============================================================
    # RECIPE VALIDATION
    # ============================================================

    try:

        recipe = (
            Recipe.model_validate_json(
                content
            )
        )

    except Exception as exc:

        logger.error(
            "%s JSON does not match "
            "Recipe schema.",
            chef_name,
        )

        logger.error(
            "JSON response:\n%s",
            content,
        )

        raise ValueError(
            f"{chef_name} generated JSON "
            "that does not match the "
            "Recipe schema."
        ) from exc

    logger.info(
        "%s validation successful: %s",
        chef_name,
        recipe.name,
    )

    return (
        recipe,
        usage,
    )

