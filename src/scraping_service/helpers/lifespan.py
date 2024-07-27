import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.scraping_service.helpers.driver import TimedDriver

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage resources during the lifespan of the application."""
    # Set up
    LOGGER.info("Setting up the driver.")
    app.timed_driver = TimedDriver()
    yield
    # Clean up
    LOGGER.info("Quitting the driver.")
    app.timed_driver.driver.quit()
    del app.timed_driver
