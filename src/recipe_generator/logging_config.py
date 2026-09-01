import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "recipe_generator.log")


def setup_logging() -> None:
    """
    Configure application-wide logging.

    All project modules write to:
        logs/recipe_generator.log

    Logs are also displayed in the terminal.
    """

    os.makedirs(LOG_DIR, exist_ok=True)

    root_logger = logging.getLogger()

    # Prevent duplicate handlers when Streamlit reruns the app
    if root_logger.handlers:
        return

    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    # ========================================================
    # FILE HANDLER
    # ========================================================

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # ========================================================
    # CONSOLE HANDLER
    # ========================================================

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ========================================================
    # REGISTER HANDLERS
    # ========================================================

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.getLogger(__name__).info(
        "Logging initialized. Log file: %s",
        os.path.abspath(LOG_FILE),
    )