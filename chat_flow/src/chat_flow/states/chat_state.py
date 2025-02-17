from typing import List

from pydantic import BaseModel

class ChatState(BaseModel):
    business_name: str = ""
    website_url: str = ""
    website_subpage_urls : List[str] = []
    website_filtered_subpage_urls : List[str] = []
    business_description: str = ""
    naics_industry_name: str = ""
    naics_industry_code: str = ""