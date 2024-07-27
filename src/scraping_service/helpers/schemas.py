from pydantic import BaseModel, HttpUrl

# Scrape API


class ScrapeRequest(BaseModel):

    """Scrape request model."""

    url: HttpUrl


class ScrapeResponse(BaseModel):

    """Scrape response model."""

    url: HttpUrl
    html: str


# Search API


class SearchResult(BaseModel):

    """Model for search result entity."""

    url: str
    title: str
    description: str


class SearchRequest(BaseModel):

    """Search request model."""

    query: str
