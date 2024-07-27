import logging

from dotenv import load_dotenv

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - <%(name)s> - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

if load_dotenv():
    LOGGER.info(f"Loaded .env file")
else:
    LOGGER.warning("No .env file found, this is expected if running via Docker.")
