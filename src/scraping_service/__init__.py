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
    assert load_dotenv(), "Failed to load .env file, did you create .env file?"
except ImportError:
    LOGGER.warning("Failed to load .env file, expected if running via docker")
