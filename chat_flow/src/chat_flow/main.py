#!/usr/bin/env python
from typing import List


from crewai.flow import Flow, listen, start

from chat_flow.crews.website_crew.website_crew import WebsiteCrew
from chat_flow.crews.industry_crew.industry_crew import IndustryCrew

from chat_flow.states.chat_state import ChatState


class ChatFlow(Flow[ChatState]):
    @start()
    def get_business_name(self):
        print("Agent: Welcome to Business Business Agent. Please enter your business name: ")
        self.state.business_name = input("User: ")
        return self.state.business_name

    @listen(get_business_name)
    def get_website_urls(self, business_name):
        print(f'Agent: {business_name} is one of the business names of all times.\n\t\tPlease enter your website url:')
        url = self.state.website_url = input("User: ")
        sub_links = WebsiteCrew(self.state).crew().kickoff(inputs = {"website_url": url})
        print(f'Type for subpage: {type(self.state.website_subpage_urls)}')
        print(f'All Website URLs:')
        print("\n".join(self.state.website_subpage_urls))
        print(f'Filtered Website URLs:')
        print("\n".join(self.state.website_filtered_subpage_urls))
        return sub_links


    # @listen(get_website_url)
    # def get_naics_industry(self):
    #     results = IndustryCrew().crew().kickoff(inputs = {"business_description": str(self.state.business_description)})
    #     print(f"Agent Great! This is what we found about your website:\n{results}")
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
