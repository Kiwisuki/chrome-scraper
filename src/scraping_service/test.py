import asyncio
import logging
from typing import Dict, List

import aiohttp

# Set up logging to print to the console
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
SEARCH_SERVICE_URL = "http://0.0.0.0:8000/search"


async def web_search(
    session: aiohttp.ClientSession,
    query: str,
    search_service_url: str = SEARCH_SERVICE_URL,
) -> List[Dict[str, str]]:
    """Search the web for a given query asynchronously."""
    body = {"query": query}
    LOGGER.info(f"Searching the web for: {query}, using service: {search_service_url}")
    async with session.get(search_service_url, json=body) as response:
        return await response.json(content_type=None)


async def perform_searches(queries: List[str]) -> List[List[Dict[str, str]]]:
    """Perform multiple web searches asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [web_search(session, query) for query in queries]
        results = await asyncio.gather(*tasks)
        return results


async def main():
    # Define the search queries
    queries = [
        "Python async web scraping",
        "AI advances in 2024",
        "Latest trends in machine learning",
    ]

    # Perform the searches
    search_results = await perform_searches(queries)

    # Display the search results
    for i, result in enumerate(search_results):
        print(f"\nResults for query '{queries[i]}':")
        for item in result:
            print(item)


# Run the main function in the event loop
if __name__ == "__main__":
    asyncio.run(main())
