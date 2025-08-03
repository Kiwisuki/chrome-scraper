import logging
import os
import time

import zendriver as uc
from retry import retry

LOGGER = logging.getLogger(__name__)
PROXY_ADDRESS = os.getenv("PROXY_ADDRESS", None)
BYPASS_LIST = [
    "edgedl.me.gvt1.com",
    "optimizationguide-pa.googleapis.com",
    "accounts.google.com",
    "https://example.com/",
]
SEARCH_QUERY_FORMAT = "https://www.google.com/search?q={query}"


class DriverClient:
    """A class to manage the browser driver and perform web scraping."""

    def __init__(
        self,
        *,
        proxy_address: str | None = PROXY_ADDRESS,
        bypass_list: list[str] = BYPASS_LIST,
        wait_to_load: int = 5,
    ) -> None:
        """Initialize the driver with a refresh rate and timer."""
        self.last_refresh = time.time()
        self.proxy_address = proxy_address
        self.bypass_list = bypass_list
        self.wait_to_load = wait_to_load

    async def initialize(self) -> None:
        """Initialize the browser."""
        options = self._get_options()
        self.browser = await uc.start(browser_args=options)

    async def close(self) -> None:
        """Close the browser."""
        await self.browser.stop()

    def _get_options(self) -> list[str]:
        """Get the options for the chromedriver."""
        options = [
            "--blink-settings=imagesEnabled=false",
            "--disable-background-networking",
            "--disable-blink-features=AutomationControlled",
            "--disable-component-extensions-with-background-pages",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-dev-shm-usage",
            "--disable-extensions",
            "--disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints",
            "--disable-gpu",
            "--disable-sync",
            "--ignore-certificate-errors",
            "--incognito",
            "--proxy-bypass-list=" + ",".join(self.bypass_list),
            "--remote-allow-origins=*",
            "--start-maximized",
        ]
        if self.proxy_address:
            options.append(f"--proxy-server={self.proxy_address}")
        return options

    @retry(Exception, tries=3, delay=2, backoff=2, logger=LOGGER)
    async def get_html(self, url: str, wait_to_load: int | None = None) -> str:
        """Get the html content from the url."""
        tab = await self.browser.get(url, new_tab=True, new_window=True)
        await tab.wait(wait_to_load or self.wait_to_load)
        html_content = await tab.get_content()
        await tab.close()
        return html_content
