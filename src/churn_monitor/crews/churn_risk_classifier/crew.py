import os
import json
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ScrapeWebsiteTool,
	SerperDevTool
)


from pydantic import BaseModel
from jambo import SchemaConverter

from churn_monitor.models import ChurnReport

if os.getenv("ANTHROPIC_API_KEY"):
    llm = LLM(model="anthropic/claude-sonnet-4-5", temperature=0.7)
else:
    llm = LLM(model="openai/gpt-4o", temperature=0.7)

@CrewBase
class ChurnRiskClassifierCrew:
    """ChurnRiskClassifier crew"""


    @agent
    def support_ticket_data_analyst(self) -> Agent:

        return Agent(
            config=self.agents_config["support_ticket_data_analyst"],


            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,

            max_execution_time=None,
            llm=llm,

        )

    @agent
    def account_profile_analyzer(self) -> Agent:

        if os.getenv("SERPER_API_KEY"):
            tools = [ScrapeWebsiteTool(), SerperDevTool()]
        else:
            tools = [ScrapeWebsiteTool()]

        return Agent(
            config=self.agents_config["account_profile_analyzer"],


            tools=tools,
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,

            max_execution_time=None,
            llm=llm,

        )

    @agent
    def churn_risk_classifier(self) -> Agent:

        return Agent(
            config=self.agents_config["churn_risk_classifier"],


            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,

            max_execution_time=None,
            llm=llm,

        )



    @task
    def analyze_support_tickets(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_support_tickets"],
            markdown=False,


        )

    @task
    def analyze_account_profile(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_account_profile"],
            markdown=False,


        )

    @task
    def classify_churn_risk(self) -> Task:
        return Task(
            config=self.tasks_config["classify_churn_risk"],
            markdown=False,
            output_pydantic=ChurnReport,
        )


    @crew
    def crew(self) -> Crew:
        """Creates the ChurnRiskClassifier crew"""
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
