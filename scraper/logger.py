import logging
from pathlib import Path
from .core.config import SCRAPER_LOG, LOG_LEVEL


def configure_logger() -> logging.Logger:
    logger = logging.getLogger("hospital_career_monitor")
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        SCRAPER_LOG.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(SCRAPER_LOG, encoding="utf-8")
        file_handler.setLevel(LOG_LEVEL)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(LOG_LEVEL)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
