import logging
import re

logger = logging.getLogger(__name__)


# ============================================================
# MOOD KEYWORDS
# ============================================================

MOOD_KEYWORDS = [
    "happy",
    "sad",
    "excited",
    "angry",
    "tired",
    "stressed",
    "relaxed",
    "calm",
    "bored",
    "lonely",
    "comforting",
    "comfortable",
    "comfort",
    "healthy",
    "energetic",
    "lazy",
    "hungry",
    "romantic",
    "adventurous",
    "celebratory",
    "unwell",
    "sick",
    "not feeling good",
    "not feeling well",
    "feeling good",
    "feeling bad",
]


# ============================================================
# RECOMMENDATION KEYWORDS
# ============================================================

RECOMMENDATION_PATTERNS = [
    "suggest me",
    "suggest some",
    "suggest a",
    "recommend me",
    "recommend some",
    "recommend a",
    "what should i eat",
    "what can i eat",
    "give me suggestions",
    "suggest recipes",
    "recommend recipes",
    "surprise me",
    "i feel",
    "i'm feeling",
    "im feeling",
    "i am feeling",
    "i'm excited",
    "im excited",
    "i am excited",
    "i'm hungry",
    "im hungry",
    "i am hungry",
    "i'm sad",
    "im sad",
    "i am sad",
    "i'm tired",
    "im tired",
    "i am tired",
    "i'm happy",
    "im happy",
    "i am happy",
    "i want something",
    "in the mood",
]


# ============================================================
# RECIPE KEYWORDS
# ============================================================

RECIPE_PATTERNS = [
    "recipe",
    "recipes",
    "how to make",
    "how do i make",
    "ingredients",
    "cook",
    "cooking",
    "prepare",
    "preparation",
]


# ============================================================
# MOOD EXTRACTION
# ============================================================

def extract_mood(user_request: str) -> str | None:
    """
    Extract the user's mood from a natural language request.

    Examples:

        "I am feeling sad"
            -> sad

        "I am in Miami and feeling sad"
            -> sad

        "I am in China not feeling good so suggest me dish"
            -> not feeling good

        "I want something comforting"
            -> comforting
    """

    if not user_request:
        return None

    text = user_request.strip()

    lowered = text.lower()

    # --------------------------------------------------------
    # Specific multi-word moods first
    # --------------------------------------------------------

    multi_word_moods = [
        "not feeling good",
        "not feeling well",
        "feeling good",
        "feeling bad",
    ]

    for mood in multi_word_moods:

        if mood in lowered:

            logger.info(
                "Mood detected: %s",
                mood,
            )

            return mood

    # --------------------------------------------------------
    # "feeling X"
    # --------------------------------------------------------

    match = re.search(
        r"\bfeeling\s+([a-zA-Z]+)",
        text,
        re.IGNORECASE,
    )

    if match:

        mood = match.group(1).strip().lower()

        if mood in MOOD_KEYWORDS:

            logger.info(
                "Mood detected: %s",
                mood,
            )

            return mood

    # --------------------------------------------------------
    # "feel X"
    # --------------------------------------------------------

    match = re.search(
        r"\bfeel\s+([a-zA-Z]+)",
        text,
        re.IGNORECASE,
    )

    if match:

        mood = match.group(1).strip().lower()

        if mood in MOOD_KEYWORDS:

            logger.info(
                "Mood detected: %s",
                mood,
            )

            return mood

    # --------------------------------------------------------
    # "I am X"
    # --------------------------------------------------------

    match = re.search(
        r"\b(?:i\s+am|i'm|im)\s+([a-zA-Z]+)",
        text,
        re.IGNORECASE,
    )

    if match:

        mood = match.group(1).strip().lower()

        if mood in MOOD_KEYWORDS:

            logger.info(
                "Mood detected: %s",
                mood,
            )

            return mood

    # --------------------------------------------------------
    # "I want something X"
    # --------------------------------------------------------

    match = re.search(
        r"\bi\s+want\s+something\s+([a-zA-Z]+)",
        text,
        re.IGNORECASE,
    )

    if match:

        mood = match.group(1).strip().lower()

        logger.info(
            "Mood detected: %s",
            mood,
        )

        return mood

    # --------------------------------------------------------
    # Keyword fallback
    # --------------------------------------------------------

    for mood in MOOD_KEYWORDS:

        if mood in lowered:

            logger.info(
                "Mood keyword detected: %s",
                mood,
            )

            return mood

    return None


# ============================================================
# LOCATION EXTRACTION
# ============================================================

def extract_location(user_request: str) -> str | None:
    """
    Extract ONLY the location from the user request.

    Examples:

        "I am in Miami and feeling sad"
            -> Miami

        "I am in China not feeling good so suggest me dish"
            -> China

        "I'm in Lahore, feeling happy"
            -> Lahore

        "I am feeling sad"
            -> None
    """

    if not user_request:
        return None

    text = user_request.strip()

    # ========================================================
    # PATTERN 1
    # "I am in Miami and feeling sad"
    # ========================================================

    patterns = [

        r"\b(?:i\s+am|i'm|im)\s+in\s+"
        r"([A-Za-z][A-Za-z\s-]*?)"
        r"(?=\s+(?:and|but|while)\b"
        r"|\s+(?:feeling|feel)\b"
        r"|\s+(?:not\s+feeling)\b"
        r"|\s+so\s+(?:suggest|recommend|give)\b"
        r"|[,!.?]|$)",

        # "I am from Lahore and..."
        r"\b(?:i\s+am|i'm|im)\s+from\s+"
        r"([A-Za-z][A-Za-z\s-]*?)"
        r"(?=\s+(?:and|but|while)\b"
        r"|\s+(?:feeling|feel)\b"
        r"|\s+(?:not\s+feeling)\b"
        r"|\s+so\s+(?:suggest|recommend|give)\b"
        r"|[,!.?]|$)",

        # "weather in Lahore"
        r"\bweather\s+in\s+"
        r"([A-Za-z][A-Za-z\s-]*?)"
        r"(?=\s+(?:and|but|while)\b"
        r"|\s+(?:feeling|feel)\b"
        r"|[,!.?]|$)",

        # "location is Lahore"
        r"\blocation\s+(?:is|:)\s*"
        r"([A-Za-z][A-Za-z\s-]*?)"
        r"(?=\s+(?:and|but|while)\b"
        r"|\s+(?:feeling|feel)\b"
        r"|[,!.?]|$)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            continue

        location = match.group(1).strip()

        # ----------------------------------------------------
        # Remove trailing filler words
        # ----------------------------------------------------

        location = re.sub(
            r"\s+(?:and|but|so|then)$",
            "",
            location,
            flags=re.IGNORECASE,
        )

        location = location.strip(
            " .,!?-"
        )

        if not location:
            continue

        # ----------------------------------------------------
        # Important validation
        # ----------------------------------------------------

        # A location should not contain obvious mood/request
        # phrases.
        invalid_phrases = [
            "feeling",
            "feel",
            "suggest",
            "recommend",
            "recipe",
            "recipes",
            "dish",
            "dishes",
            "eat",
            "hungry",
            "happy",
            "sad",
            "excited",
            "tired",
            "comforting",
        ]

        lowered_location = location.lower()

        if any(
            phrase in lowered_location
            for phrase in invalid_phrases
        ):

            logger.warning(
                "Rejected invalid location extraction: %s",
                location,
            )

            continue

        logger.info(
            "Location detected from request: %s",
            location,
        )

        return location

    logger.info(
        "No location detected in recommendation request"
    )

    return None


# ============================================================
# INPUT MODE DETECTION
# ============================================================

def detect_input_mode(
    user_request: str,
) -> dict:
    """
    Determine whether the request is:

        explicit recipe
        recommendation

    Also extract:

        location
        mood
    """

    if not user_request:

        return {
            "mode": "explicit",
            "location": None,
            "mood": None,
        }

    text = user_request.strip()

    lowered = text.lower()

    # ========================================================
    # EXTRACT MOOD
    # ========================================================

    mood = extract_mood(
        text
    )

    # ========================================================
    # EXTRACT LOCATION
    # ========================================================

    location = extract_location(
        text
    )

    # ========================================================
    # CHECK RECOMMENDATION
    # ========================================================

    is_recommendation = any(
        pattern in lowered
        for pattern in RECOMMENDATION_PATTERNS
    )

    # Mood automatically means recommendation.
    if mood:

        is_recommendation = True

    # ========================================================
    # CHECK EXPLICIT RECIPE
    # ========================================================

    is_explicit_recipe = any(
        pattern in lowered
        for pattern in RECIPE_PATTERNS
    )

    # ========================================================
    # DECIDE MODE
    # ========================================================

    if is_recommendation:

        mode = "recommendation"

        logger.info(
            "Input decision: recommendation request"
        )

    elif is_explicit_recipe:

        mode = "explicit"

        logger.info(
            "Input decision: explicit recipe request"
        )

    else:

        # ----------------------------------------------------
        # Unknown/general text.
        #
        # Keep existing behavior as explicit recipe rather
        # than sending arbitrary text to weather.
        # ----------------------------------------------------

        mode = "explicit"

        logger.info(
            "Input decision: defaulting to explicit recipe"
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    result = {
        "mode": mode,
        "location": location,
        "mood": mood,
    }

    logger.info(
        "Input detection result: %s",
        result,
    )

    return result