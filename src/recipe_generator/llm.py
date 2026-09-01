import logging
from functools import lru_cache

from langchain_groq import ChatGroq

from .config import GROQ_API_KEY, TEXT_MODEL


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_text_model():

    logger.info(
        "Creating Groq text model: %s",
        TEXT_MODEL,
    )

    return ChatGroq(
        model=TEXT_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.2,
        max_tokens=700,
    )