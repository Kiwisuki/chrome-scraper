from nodriver import Browser

from src.scraping_service.helpers.driver import DriverClient


async def test_initialize_driver():
    timed_driver = DriverClient()
    await timed_driver.initialize()
    assert isinstance(timed_driver.browser, Browser)
