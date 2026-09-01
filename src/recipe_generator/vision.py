import base64
import io
import logging
import time

import requests
from PIL import Image, ImageOps

from .config import OLLAMA_BASE_URL, VISION_MODEL


logger = logging.getLogger(__name__)


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image_path: str) -> str:
    """
    Prepare uploaded image for Qwen3-VL.

    - Fix EXIF orientation
    - Convert RGBA/P/etc. to RGB
    - Resize only if very large
    - Convert to JPEG
    - Return base64
    """

    image = Image.open(image_path)

    logger.info(
        "Original image | format=%s | size=%s | mode=%s",
        image.format,
        image.size,
        image.mode,
    )

    # Fix phone-camera orientation
    image = ImageOps.exif_transpose(image)

    # Handle transparency correctly
    if image.mode != "RGB":

        if "A" in image.getbands():

            background = Image.new(
                "RGB",
                image.size,
                "white",
            )

            background.paste(
                image,
                mask=image.getchannel("A"),
            )

            image = background

        else:
            image = image.convert("RGB")

    # Don't enlarge small images
    max_size = 512

    if max(image.size) > max_size:

        image.thumbnail(
            (max_size, max_size),
            Image.Resampling.LANCZOS,
        )

    # Convert to JPEG
    buffer = io.BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=95,
    )

    image_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    logger.info(
        "Preprocessed image | size=%s",
        image.size,
    )

    return image_base64


# ============================================================
# QWEN3-VL DIRECT OLLAMA CALL
# ============================================================

def describe_food_image(image_path: str) -> str:

    logger.info(
        "Starting %s food description: %s",
        VISION_MODEL,
        image_path,
    )

    image_base64 = preprocess_image(
        image_path
    )

    prompt = """
        Look at this image.
        
        Identify the main food or dish.
        
        Return ONLY the common dish name.
        
        Examples:
        biryani
        pizza
        burger
        pasta
        fried rice
        sandwich
        salad
        
        Do not explain.
        """

    payload = {
        "model": VISION_MODEL,

        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [
                    image_base64
                ],
            }
        ],

        "stream": False,

        # Important:
        # Give Qwen enough output space.
        "options": {
            "temperature": 0,
            "num_predict": 20,
        },
    }

    start_time = time.perf_counter()

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    elapsed = (
        time.perf_counter()
        - start_time
    )

    logger.info(
        "%s response completed in %.2f seconds",
        VISION_MODEL,
        elapsed,
    )

    # --------------------------------------------------------
    # IMPORTANT
    # --------------------------------------------------------

    content = (
        data
        .get("message", {})
        .get("content", "")
    )

    content = content.strip()

    logger.info(
        "%s raw description: %s",
        VISION_MODEL,
        content,
    )

    if not content:

        logger.warning(
            "%s returned empty content. "
            "Full response: %s",
            VISION_MODEL,
            data,
        )

        return "unknown"

    return content


# ============================================================
# DISH NAME EXTRACTION
# ============================================================

def extract_dish_name(description: str) -> str:

    """
    Convert the visual description into a short dish name.

    This uses the same text model used by the recipe generator.
    """

    if not description:
        return "unknown"

    # --------------------------------------------------------
    # IMPORTANT
    #
    # For the first test, don't use another LLM here.
    #
    # Qwen3-VL's description itself should be inspected first.
    # --------------------------------------------------------

    logger.info(
        "Using visual description for dish identification: %s",
        description,
    )

    return description


# ============================================================
# MAIN FUNCTION
# ============================================================

def identify_dish(image_path: str) -> str:

    logger.info(
        "Starting food image identification: %s",
        image_path,
    )

    start_time = time.perf_counter()

    description = describe_food_image(
        image_path
    )

    # --------------------------------------------------------
    # TEMPORARY:
    #
    # Return Qwen's actual description.
    #
    # Once this works correctly, we can add a text-model
    # normalization step to convert:
    #
    # "The image shows a bowl of rice..."
    #
    # into:
    #
    # "chicken biryani"
    # --------------------------------------------------------

    result = description.strip()

    if not result:

        result = "unknown"

    elapsed = (
        time.perf_counter()
        - start_time
    )

    logger.info(
        "Vision identification completed in %.2f seconds",
        elapsed,
    )

    logger.info(
        "Vision result: %s",
        result,
    )

    return result
