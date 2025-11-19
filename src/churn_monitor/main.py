#!/usr/bin/env python

import toon_format as toon

from crewai.flow import Flow, listen, start
from pydantic import BaseModel
from typing import Literal

from churn_monitor.crews.churn_prevention_email_outreach.crew import ChurnPreventionEmailOutreachCrew
from churn_monitor.crews.churn_risk_classifier.crew import ChurnRiskClassifierCrew
from churn_monitor.crm import Client
from churn_monitor.models import Account, SupportTicket, ChurnReport, OutreachEmail
from churn_monitor.report import generate_html_report, generate_json_report, write_report_to_file

class ChurnMonitorState(BaseModel):
    accounts: list[Account] = []
    support_tickets: list[SupportTicket] = []
    outreach_emails: list[OutreachEmail] = []
    output_format: Literal["html", "json"] = "html"
    limit: int = 1


class ChurnMonitorFlow(Flow[ChurnMonitorState]):
    @start()
    def load_accounts(self):
        """
        Load accounts from the CRM.
        """
        self.state.accounts = Client().list_accounts()[:self.state.limit]

    @listen(load_accounts)
    def classify_churn_risk(self):
        """
        Classifies each account into high, medium, or low churn risk.
        """
        for account in self.state.accounts:
            support_tickets = Client().list_support_tickets(account.account_id)
            support_tickets_data = [ticket.model_dump() for ticket in support_tickets]

            inputs = {
                "account_id": account.account_id,
                "support_tickets_data": toon.encode(support_tickets_data),
                "additional_data": "N/A",
                "account_data": toon.encode(account.model_dump())
            }
            result = ChurnRiskClassifierCrew().crew().kickoff(inputs=inputs)
            account.churn_report = result.pydantic

    @listen(classify_churn_risk)
    def outreach_accounts(self):
        """
        Outreach accounts that are at high risk of churn with a personalized
        email.
        """
        for account in self.state.accounts:
            if account.churn_report.churn_risk_classification in ["medium", "high"]:
                inputs = {
                    "account_information": toon.encode(account.model_dump()),
                    "churn_report": toon.encode(account.churn_report.model_dump()),
                }
                result = ChurnPreventionEmailOutreachCrew().crew().kickoff(inputs=inputs)
                self.state.outreach_emails.append(result.pydantic)

    @listen(outreach_accounts)
    def write_final_report(self):
        """
        Writes a final report with the churn risk classification and outreach
        emails as HTML or JSON.
        """
        emails_by_account = {email.account_id: email for email in self.state.outreach_emails}
        accounts = self.state.accounts

        if self.state.output_format == "html":
            content = generate_html_report(accounts, emails_by_account)
        elif self.state.output_format == "json":
            content = generate_json_report(accounts, emails_by_account)

        write_report_to_file(content, self.state.output_format)
        return content

def kickoff():
    churn_monitor_flow = ChurnMonitorFlow()
    churn_monitor_flow.kickoff()


def plot():
    churn_monitor_flow = ChurnMonitorFlow()
    churn_monitor_flow.plot()


if __name__ == "__main__":
    kickoff()
