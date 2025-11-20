#!/usr/bin/env python

import toon_format as toon

from crewai.flow import Flow, listen, start
from pydantic import BaseModel
from typing import Literal

from churn_monitor.crews.churn_prevention_email_outreach.crew import ChurnPreventionEmailOutreachCrew
from churn_monitor.crews.churn_risk_classifier.crew import ChurnRiskClassifierCrew
from churn_monitor.crm import Client
from churn_monitor.models import Account, SupportTicket, OutreachEmail
from churn_monitor.report import generate_html_report, generate_json_report, write_report_to_file

class ChurnMonitorState(BaseModel):
    pass

class ChurnMonitorFlow(Flow[ChurnMonitorState]):
    @start()
    def load_accounts(self):
        """
        Load accounts from the CRM.
        """
        pass

    @listen(load_accounts)
    def classify_churn_risk(self):
        """
        Classifies each account into high, medium, or low churn risk.
        """
        pass

    @listen(classify_churn_risk)
    def outreach_accounts(self):
        """
        Outreach accounts that are at high risk of churn with a personalized
        email.
        """
        pass

    @listen(outreach_accounts)
    def write_final_report(self):
        """
        Writes a final report with the churn risk classification and outreach
        emails.
        """
        pass

def kickoff():
    churn_monitor_flow = ChurnMonitorFlow()
    churn_monitor_flow.kickoff()


def plot():
    churn_monitor_flow = ChurnMonitorFlow()
    churn_monitor_flow.plot()


if __name__ == "__main__":
    kickoff()
