import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


from churn_monitor.models import OutreachEmail



@CrewBase
class ChurnPreventionEmailOutreachCrew:
    """ChurnPreventionEmailOutreach crew"""


    @agent
    def email_outreach_specialist(self) -> Agent:

        return Agent(
            config=self.agents_config["email_outreach_specialist"],


            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,

            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o",
                temperature=0.7,
            ),

        )

    @agent
    def customer_retention_strategist(self) -> Agent:

        return Agent(
            config=self.agents_config["customer_retention_strategist"],


            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,

            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o",
                temperature=0.7,
            ),

        )



    @task
    def develop_retention_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["develop_retention_strategy"],
            markdown=False,


        )

    @task
    def draft_personalized_outreach_email(self) -> Task:
        return Task(
            config=self.tasks_config["draft_personalized_outreach_email"],
            markdown=False,
            output_pydantic=OutreachEmail,
        )


    @crew
    def crew(self) -> Crew:
        """Creates the ChurnPreventionEmailOutreach crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
