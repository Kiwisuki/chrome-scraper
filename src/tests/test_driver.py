import pytest
from undetected_chromedriver import Chrome

from src.scraping_service.helpers.driver import TimedDriver


def test_initialize_driver():
    timed_driver = TimedDriver()
    assert isinstance(timed_driver.driver, Chrome)


@pytest.fixture()
def timed_driver():
    # Mocking the selenium driver, to avoid the need of a webdriver.
    class MockSeleniumDriver:
        def __init__(self, *args, **kwargs):
            pass

        def get(self, *args, **kwargs):  # noqa: ARG002
            self.page_source = "<html></html>"

        def quit(self):  # noqa: A003
            pass

    class MockTimedDriver(TimedDriver):
        def _initialize_chromedriver(self):
            self.driver = MockSeleniumDriver()

    return MockTimedDriver()


def test_get_html(timed_driver):
    # We will only test whether the method returns the html content
    # Since this is the main functionality we care about, and we might
    # change the wrapper logic later for better bot detection avoidance.
    assert timed_driver.get_html("https://www.google.com") == "<html></html>"
