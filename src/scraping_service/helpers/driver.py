import logging
import os
import time
from typing import List

from bs4 import BeautifulSoup
from retry import retry
from undetected_chromedriver import Chrome, ChromeOptions

from src.scraping_service.helpers.schemas import SearchResult

LOGGER = logging.getLogger(__name__)
DRIVER_EXECUTABLE_PATH = os.environ["DRIVER_EXECUTABLE_PATH"]
PROXY_ADDRESS = os.environ["PROXY_ADDRESS"]


class TimedDriver:

    """Driver that resets itself after a certain amount of actions or time passed."""

    def __init__(
        self,
        *,
        driver_executable_path: str = DRIVER_EXECUTABLE_PATH,
        proxy_address: str = PROXY_ADDRESS,
        refresh_rate: int = 10,
        refresh_timer: int = 60,
        wait_to_load: int = 3,
        headless: bool = False,
    ):
        """Initialize the driver with a refresh rate and timer."""
        self.actions = 0
        self.last_refresh = time.time()
        self.refresh_rate = refresh_rate
        self.refresh_timer = refresh_timer
        self.wait_to_load = wait_to_load
        self.headless = headless
        self.proxy_address = proxy_address
        self.driver_executable_path = driver_executable_path
        self._initialize_chromedriver()

    def _get_options(self):
        """Get the options for the chromedriver."""
        options = ChromeOptions()

        options.add_argument(f"--proxy-server={self.proxy_address}")

        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-component-extensions-with-background-pages")
        options.add_argument("--disable-component-update")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-extensions")
        options.add_argument(
            "--disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints"
        )
        options.add_argument("--disable-sync")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--start-maximized")

        options.add_experimental_option("prefs", {"download_restrictions": 3})

        return options

    def _initialize_chromedriver(self):
        """Initialize the chromedriver."""
        self.driver = Chrome(
            options=self._get_options(),
            headless=self.headless,
            use_subprocess=False,
            driver_executable_path=self.driver_executable_path,
        )
        self.driver.execute_cdp_cmd(
            "Network.setBlockedURLs",
            {
                "urls": [
                    "www.gstatic.com",
                    "www.google.com",
                    "optimizationguide-pa.googleapis.com",
                    "edgedl.me.gvt1.com",
                    "*://*.edgedl.me.gvt1.com/*",
                ]
            },
        )
        self.driver.execute_cdp_cmd("Network.enable", {})

    def _refresh(self):
        """Refresh the chromedriver."""
        self.driver.quit()
        self._initialize_chromedriver()
        self.last_refresh = time.time()

    def _increment(self):
        """Increments the actions and refreshes if needed."""
        self.actions += 1
        if (self.actions % self.refresh_rate == 0) or (
            time.time() - self.last_refresh > self.refresh_timer
        ):
            self._refresh()

    @retry(Exception, tries=3, delay=2, backoff=2, logger=LOGGER)
    def get_html(self, url: str) -> str:
        """Get the html content from the url."""
        self.driver.get(url)
        time.sleep(self.wait_to_load)
        html_content = self.driver.page_source
        self._increment()
        return html_content

    @staticmethod
    def _parse_google_search(html_content: str) -> List[SearchResult]:
        """Parse HTML content and return a list of SearchResult objects."""
        results = []
        soup = BeautifulSoup(html_content, "html.parser")
        result_soup = soup.find(
            "div", attrs={"id": "res"}
        )  # Filter out Sponsored results
        result_blocks = result_soup.find_all("div", attrs={"class": "g"})

        for result in result_blocks:
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find("div", {"style": "-webkit-line-clamp:2"})

            if link and title and description_box:
                url = link["href"]
                title_text = title.text
                description = description_box.text
                results.append(
                    SearchResult(url=url, title=title_text, description=description)
                )

        return results

    def search_google(self, query: str) -> List[SearchResult]:
        """Search Google and return a list of SearchResult objects."""
        LOGGER.info(f"Searching Google for '{query}'...")
        search_results = self.get_html(f"https://www.google.com/search?q={query}")
        return self._parse_google_search(search_results)
