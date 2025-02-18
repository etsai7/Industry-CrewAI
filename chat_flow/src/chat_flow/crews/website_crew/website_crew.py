from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.website_search.website_search_tool import WebsiteSearchTool

from chat_flow.tools.website_urls import WebsiteUrls
from chat_flow.states.chat_state import ChatState
from chat_flow.tools.website_scraper import WebsiteScraperUrls
from pydantic import BaseModel

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class URLs(BaseModel):
    urls: list[str]

@CrewBase
class WebsiteCrew:
    """Website Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, chatState: ChatState ):
        self.chatState = chatState

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def website_url_scraper(self):
        return Agent(
            config=self.agents_config['website_url_scraper'],
            verbose=True,
            tools=[WebsiteUrls()],
        )

    @agent
    def website_url_analyst(self):
        return Agent(
            config=self.agents_config['website_url_analyst'],
            verbose=True,
        )

    @agent
    def website_content_analyst(self):
        return Agent(
            config=self.agents_config['website_content_analyst'],
            tools=[WebsiteScraperUrls(urls=self.chatState.website_filtered_subpage_urls)]
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def website_urls_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['website_urls_scraping_task'],
            inputs={"url": "website_url"},
            output_pydantic=URLs,
            callback=self.store_all_urls
        )

    @task
    def website_urls_selection_task(self):
        return Task(
            config=self.tasks_config['website_urls_selection_task'],
            output_pydantic=URLs,
            callback=self.store_filtered_urls
        )

    @task
    def website_content_analysis_task(self):
        return Task(
            config=self.tasks_config['website_content_analysis_task'],
        )

    def store_all_urls(self, urls):
        self.chatState.website_subpage_urls = urls.pydantic.urls

    def store_filtered_urls(self, filtered_urls):
        self.chatState.website_filtered_subpage_urls = filtered_urls.pydantic.urls

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            capture_output=True
        )
