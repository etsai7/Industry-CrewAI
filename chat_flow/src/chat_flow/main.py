#!/usr/bin/env python

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from chat_flow.crews.website_crew.website_crew import WebsiteCrew
from chat_flow.crews.industry_crew.industry_crew import IndustryCrew

class ChatState(BaseModel):
    business_name: str = ""
    website_url: str = ""
    business_description: str = ""
    naics_industry_name: str = ""
    naics_industry_code: str = ""

class ChatFlow(Flow[ChatState]):
    @start()
    def get_business_name(self):
        print("Agent: Welcome to Business Business Agent. Please enter your business name: ")
        self.state.business_name = input("User: ")
        return self.state.business_name

    @listen(get_business_name)
    def get_website_url(self, business_name):
        print(f'Agent: {business_name} is one of the business names of all times.\n\t\tPlease enter your website url:')
        url = self.state.website_url = input("User: ")
        results = WebsiteCrew().crew().kickoff(inputs = {"website_url": url})
        self.state.business_description = results

    @listen(get_website_url)
    def get_naics_industry(self):
        results = IndustryCrew().crew().kickoff(inputs = {"business_description": str(self.state.business_description)})
        print(f"Agent Great! This is what we found about your website:\n{results}")
        # print()
        # print(self.state.model_dump_json(indent=4))


def kickoff():
    chat_flow = ChatFlow()
    chat_flow.kickoff()


def plot():
    chat_flow = ChatFlow()
    chat_flow.plot()


if __name__ == "__main__":
    kickoff()
