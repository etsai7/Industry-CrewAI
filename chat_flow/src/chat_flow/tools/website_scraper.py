from typing import Type
from urllib.parse import urljoin

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
import requests


class WebsiteScraperToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    urls: list[str] = Field(..., description="Website URL")


class WebsiteScraperUrls(BaseTool):
    name: str = "Website URL Scraping Tool"
    description: str = (
        "This tool takes in a website url and identifies all subpage links present on the page"
    )
    args_schema: Type[BaseModel] = WebsiteScraperToolInput

    def _run(self, urls: list[str]) -> dict:
        info = {}
        for url in urls:
            try:
                print(f"Analyzing {url}")
                # Get the HTML content of the page
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=5)
                response.raise_for_status()  # Check if the request was successful

                # Parse the HTML with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Collect text from multiple tags
                text_elements = []
                text_elements += [p.get_text() for p in soup.find_all('p')]
                text_elements += [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
                # text_elements += [li.get_text() for li in soup.find_all('li')]
                # text_elements += [span.get_text() for span in soup.find_all('span')]
                text_elements = [text.strip().replace('\n','').replace('\t','') for text in text_elements if text]

                info[url] = text_elements


            except requests.RequestException as e:
                print(f"Error fetching the webpage: {e}")
                return []

        return info

