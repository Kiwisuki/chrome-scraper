# Scraping Service

## Introduction

This project is a scraping service served as an API. It provides two endpoints:
1. **Scrape URL:** Scrapes the content of a given URL.
2. **Search Google:** Performs a Google search and returns the search results.

## Development Environment Setup

### Prerequisites

1. **ChromeDriver Installation:**
   - Download the appropriate ChromeDriver for your system from [here](https://getwebdriver.com/chromedriver#stable).
   - Place the downloaded driver in the `deps` directory.

2. **Environment Configuration:**
   - Copy the `.env.tmpl` file to `.env`.
   - Fill in the required values in the `.env` file.

Note: Make sure your proxy provider does not require username & password authentication
### Setup

1. **Project Setup:**
   - Run the following command to set up the project:
     ```bash
     make env
     ```
   - Activate the environment:
     ```bash
     poetry shell
     ```

## Running the Application

### Docker Setup

1. Ensure Azure VPN is enabled.
2. Build the Docker image:
```bash
   docker compose build
```
3. Run the Docker container:
```bash
    docker compose up
```

## Manually testing the application

For testing application, you can use the following commands:


For scraping a URL:
```bash
curl --location --request GET 'http://0.0.0.0:8000/ai/scrape' \
--header 'Content-Type: application/json' \
--data '{
    "url": "http://www.whatismyproxy.com/"
}
'
```

For performing a Google search:
```bash
curl --location --request GET 'http://0.0.0.0:8000/ai/search' \
--header 'Content-Type: application/json' \
--data '{
    "query":"Are Kiwis good for health?"
}
'
```


## Structure

```bash
.
├── deps                       # Directory for project dependencies (chromedriver)
├── .env.tmpl                  # Template for environment variables
├── docker-compose.yml         # Docker Compose configuration file
├── Dockerfile                 # Docker image definition
├── makefile                   # Makefile for project automation
├── pyproject.toml             # Python project configuration file
├── README.md                  # Project documentation and information
├── requirements.txt           # Python package dependencies
├── src                        # Source code directory
│   ├── scraping_service       # Main scraping service package
│   │   ├── app.py             # Main application file
│   │   ├── helpers            # Helper functions and utilities
│   │   │   ├── driver.py      # Web driver implementation
│   │   │   ├── __init__.py    # Package initializer
│   │   │   ├── lifespan.py    # Lifespan management for the application
│   │   │   └── schemas.py     # Data schemas for the application
│   │   └── __init__.py        # Package initializer
│   └── tests                  # Test directory
│       └── test_driver.py     # Tests for the web driver
└── startup.sh                 # Startup script for the application within Docker

```