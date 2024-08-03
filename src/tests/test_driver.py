from nodriver import Browser

from src.scraping_service.helpers.driver import TimedDriver


async def test_initialize_driver():
    timed_driver = TimedDriver()
    await timed_driver.initialize()
    assert isinstance(timed_driver.browser, Browser)
