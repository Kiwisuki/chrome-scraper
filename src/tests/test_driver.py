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


# function to load all the test files
@pytest.fixture
def htmls():
    file_paths = [TEST_DATA_PATH / filename for filename in TEST_FILENAMES]
    return [file_path.read_text() for file_path in file_paths]


async def test_initialize_driver():
    timed_driver = DriverClient()
    await timed_driver.initialize()
    assert isinstance(timed_driver.browser, Browser)
