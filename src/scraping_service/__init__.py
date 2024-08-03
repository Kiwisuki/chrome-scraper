import logging

from dotenv import load_dotenv

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - <%(name)s> - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

try:
    from dotenv import load_dotenv

    if load_dotenv():
        LOGGER.info(f"Loaded .env file")
    else:
        LOGGER.warning(f"Failed to load .env file")
except ImportError:
    LOGGER.warning("Failed to load .env file, expected if running via docker")
