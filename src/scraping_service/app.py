from typing import List, Dict

from fastapi import FastAPI, HTTPException

from src.scraping_service.helpers.lifespan import lifespan
from src.scraping_service.helpers.schemas import (
    ScrapeRequest,
    ScrapeResponse,
    SearchRequest,
    SearchResult,
)

app = FastAPI(lifespan=lifespan)


@app.get("/scrape", response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest):
    """Scrape the given URL and return the HTML content."""
    try:
        html = await app.timed_driver.get_html(str(request.url))
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ScrapeResponse(url=request.url, html=html)


@app.get("/search", response_model=List[SearchResult])
async def search(request: SearchRequest):
    """Search the given query on Google and return the search results."""
    try:
        results = await app.timed_driver.search_google(request.query)
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return results

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint to determine if the service is running."""
    return {"STATUS": "OK", "MESSAGE": "Service is running."}

