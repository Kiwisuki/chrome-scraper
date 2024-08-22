from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from nodriver import Browser

from src.scraping_service.helpers.driver import DriverClient
from src.scraping_service.helpers.schemas import SearchResult

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


@pytest.fixture()
def urls() -> list[str]:
    """Return the URLs of the test files."""
    return ["file://" + str(file_path) for file_path in FILE_PATHS]


@pytest.fixture()
def htmls() -> list[str]:
    """Return the HTML content of the test files."""
    return [file_path.read_text() for file_path in FILE_PATHS]


@pytest.fixture()
async def driver() -> AsyncGenerator[DriverClient, None]:
    """Create a driver client for testing."""
    driver = DriverClient()
    await driver.initialize()
    return driver


async def test_initialize_driver(driver: DriverClient) -> None:
    """Test the initialization of the driver."""
    assert isinstance(driver.browser, Browser)


async def test_get_html(
    driver: DriverClient,
    htmls: list[str],
    urls: list[str],
) -> None:
    """Test the get_html method of the driver."""
    for true_html, url in zip(htmls, urls, strict=True):
        fetched_html = await driver.get_html(url, wait_to_load=1)
        assert fetched_html[:1000] == true_html[:1000]


async def test_parse_google_search(driver: DriverClient, htmls: list[str]) -> None:
    """Test the search_google method of the driver."""
    for html in htmls:
        results = driver._parse_google_search(html)
        for result in results:
            assert isinstance(result, SearchResult)
            assert result.url
            assert result.title
            assert result.description


async def test_search_google(driver: DriverClient, urls: list[str]) -> None:
    """Test the search_google method of the driver."""
    for url in urls:
        results = await driver.search_google(
            "test",
            wait_to_load=1,
            search_query_format=url,
        )
        for result in results:
            assert isinstance(result, SearchResult)
            assert result.url
            assert result.title
            assert result.description
