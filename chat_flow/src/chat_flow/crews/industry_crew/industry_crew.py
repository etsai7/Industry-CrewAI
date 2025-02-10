from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class IndustryCrew:
    """Industry Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"



    @agent
    def industry_analyst(self):
        return Agent(
            config=self.agents_config['industry_analyst'],
            verbose=False
        )



    @task
    def industry_task(self):
        return Task(
            config=self.tasks_config['industry_task'],
            output_file='reports/website_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the IndustryCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False, # Turns off thinking output and results
            capture_output=True # Makes sure the output is still passed along
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )