from typing import Type
from urllib.parse import urljoin

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
import requests


class WebsiteUrlsToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    url: str = Field(..., description="Website URL")


class WebsiteUrls(BaseTool):
    name: str = "Website URL Scraping Tool"
    description: str = (
        "This tool takes in a website url and identifies all subpage links present on the page"
    )
    args_schema: Type[BaseModel] = WebsiteUrlsToolInput

    def _run(self, url: str) -> list[str]:
        try:
            print(f"Analyzing {url}")
            # Get the HTML content of the page
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Check if the request was successful

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all <a> tags and extract the href attribute
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Convert relative URLs to absolute URLs
                full_url = urljoin(url, href)
                links.append(full_url)

            return links

        except requests.RequestException as e:
            print(f"Error fetching the webpage: {e}")
            return []

