import os

from dotenv import load_dotenv


load_dotenv()


# ============================================================
# GROQ
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TEXT_MODEL = os.getenv(
    "TEXT_MODEL",
    "openai/gpt-oss-20b",
)


# ============================================================
# OLLAMA
# ============================================================

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

VISION_MODEL = os.getenv(
    "VISION_MODEL",
    "moondream",
)


# ============================================================
# VALIDATION
# ============================================================

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set."
    )