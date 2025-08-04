import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from scraping_service.helpers.driver import DriverClient

LOGGER = logging.getLogger(__name__)
RESTART_TIMER = 30 * 60  # 30 minutes in seconds


async def restart_driver_periodically(app: FastAPI) -> None:
    while True:
        LOGGER.info("Restarting driver client...")
        try:
            await app.driver_client.close()
            LOGGER.info("Old driver client closed.")
        except Exception:
            LOGGER.exception("Error closing driver client")
        app.driver_client = DriverClient()
        await app.driver_client.initialize()
        LOGGER.info("New driver client initialized.")
        await asyncio.sleep(30 * 60)  # wait 30 minutes


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Manage resources during the lifespan of the application."""
    task = asyncio.create_task(restart_driver_periodically())
    try:
        yield
    finally:
        # Cancel the background task on shutdown
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
        app.driver_client.close()
        LOGGER.info("Driver quit.")
