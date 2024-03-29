import logging
from logging.handlers import RotatingFileHandler

from app.core.constants import BASE_DIR, LOG_DT_FORMAT, LOG_MSG_FORMAT


def configure_logging():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "marketplace.log"

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10**6, backupCount=5
    )
    logging.basicConfig(
        datefmt=LOG_DT_FORMAT,
        format=LOG_MSG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler()),
    )
