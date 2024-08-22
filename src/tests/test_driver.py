from pathlib import Path

import pytest
from nodriver import Browser

from src.scraping_service.helpers.driver import DriverClient

TEST_PATH = Path(__file__).parent
TEST_DATA_PATH = TEST_PATH / "test_data"
TEST_FILENAMES = [
    "search_AI.html",
    "search_Docker.html",
    "search_Kubernetes.html",
    "search_ML.html",
    "search_Python.html",
    "search_Rust.html",
]
FILE_PATHS = [TEST_DATA_PATH / filename for filename in TEST_FILENAMES]


@pytest.fixture
def htmls():
    return [file_path.read_text() for file_path in FILE_PATHS]


@pytest.fixture
async def driver():
    driver = DriverClient()
    await driver.initialize()
    yield driver
    await driver.close()


@pytest.mark.asyncio
async def test_initialize_driver(driver):
    assert isinstance(driver.browser, Browser)


@pytest.mark.asyncio
async def test_get_html(driver, htmls):
    for original_html, path in zip(htmls, FILE_PATHS):
        # use file htmls to fetch through driver
        fetched_html = await driver.get_html("file://" + str(path))
        assert (
            fetched_html[:1000] == original_html[:1000]
        )  # Not comparing the whole due to dynamic content
