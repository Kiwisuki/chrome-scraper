import logging
import os
import time
from typing import List, Optional

import nodriver as uc
from bs4 import BeautifulSoup
from retry import retry

from src.scraping_service.helpers.schemas import SearchResult

LOGGER = logging.getLogger(__name__)
PROXY_ADDRESS = os.getenv("PROXY_ADDRESS", None)


class TimedDriver:

    """Driver that resets itself after a certain amount of actions or time passed."""

    def __init__(
        self,
        *,
        proxy_address: Optional[str] = PROXY_ADDRESS,
        refresh_rate: int = 1_000,
        refresh_timer: int = 3_600,
        wait_to_load: int = 5,
    ):
        """Initialize the driver with a refresh rate and timer."""
        self.actions = 0
        self.last_refresh = time.time()
        self.refresh_rate = refresh_rate
        self.refresh_timer = refresh_timer
        self.wait_to_load = wait_to_load
        self.proxy_address = proxy_address

    async def initialize(self):
        """Initialize the browser."""
        await self._initialize_browser()

    def _get_options(self):
        """Get the options for the chromedriver."""
        options = [
            "--blink-settings=imagesEnabled=false",
            "--disable-background-networking",
            "--disable-blink-features=AutomationControlled",
            "--disable-component-extensions-with-background-pages",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints",
            "--disable-sync",
            "--ignore-certificate-errors",
            "--incognito",
            "--remote-allow-origins=*",
            "--start-maximized",
        ]
        if self.proxy_address:
            options.append(f"--proxy-server={self.proxy_address}")
        return options

    async def _initialize_browser(self):
        """Initialize the chromedriver."""
        options = self._get_options()
        self.browser = await uc.start(browser_args=options)

    async def _refresh(self):
        """Refresh the chromedriver."""
        self.browser.stop()
        await self._initialize_browser()
        self.last_refresh = time.time()

    def _increment(self):
        """Increments the actions and refreshes if needed."""
        self.actions += 1
        if (self.actions % self.refresh_rate == 0) or (
            time.time() - self.last_refresh > self.refresh_timer
        ):
            self._refresh()

    @retry(Exception, tries=3, delay=2, backoff=2, logger=LOGGER)
    async def get_html(self, url: str) -> str:
        """Get the html content from the url."""
        page = await self.browser.get(url)
        time.sleep(self.wait_to_load)
        html_content = await page.get_content()
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

    async def search_google(self, query: str) -> List[SearchResult]:
        """Search Google and return a list of SearchResult objects."""
        LOGGER.info(f"Searching Google for '{query[:20]}'...")
        search_results = await self.get_html(f"https://www.google.com/search?q={query}")
        return self._parse_google_search(search_results)
