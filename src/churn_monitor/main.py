#!/usr/bin/env python

import toon_format as toon

from crewai.flow import Flow, listen, start
from pydantic import BaseModel, Field
from random import randint

from churn_monitor.crews.churn_prevention_email_outreach.crew import ChurnPreventionEmailOutreachCrew
from churn_monitor.crews.churn_risk_classifier.crew import ChurnRiskClassifierCrew
from churn_monitor.crm import Client
from churn_monitor.models import Account, SupportTicket, ChurnReport, OutreachEmail

class ChurnMonitorState(BaseModel):
    accounts: list[Account] = []
    support_tickets: list[SupportTicket] = []
    outreach_emails: list[OutreachEmail] = []
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

    def get_human_feedback(self):
        """
        Gets human feedback on the churn risk classification with additional
        context about the accounts.
        """
        pass

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
        emails as a single HTML page with account, overview, and email.
        """
        import os

        output_dir = "reports"
        os.makedirs(output_dir, exist_ok=True)
        html_path = os.path.join(output_dir, "churn_risk_report.html")

        html = [
            "<html>",
            "<head>",
            "<title>Churn Risk Classification and Outreach Emails</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; }",
            "h1 { color: #1A5276; }",
            "h2 { color: #21618C; border-bottom: 1px solid #aaa; padding-bottom: 2px; }",
            ".account-block { border: 1px solid #dee2e6; border-radius: 5px; background: #f6f9fa; margin: 2em 0; padding: 1.2em 2em; }",
            ".email { background: #fff; border: 1px solid #bbb; border-radius: 4px; margin: 1em 0 0 0; padding: 1em; }",
            ".overview { font-style: italic; color: #444; }",
            ".not-sent { color: #b22222; font-weight: bold; }",
            "</style>",
            "</head>",
            "<body>",
            "<h1>Churn Risk Classification and Outreach Emails</h1>"
        ]

        emails_by_account = {email.account_id: email for email in getattr(self.state, 'outreach_emails', [])}

        for account in getattr(self.state, 'accounts', []):
            churn_report = getattr(account, "churn_report", None)
            email = emails_by_account.get(account.account_id)
            html.append('<div class="account-block">')
            # Account basic info
            html.append(f"<h2>Account: {getattr(account, 'org_name', account.account_id)}</h2>")
            html.append(f"<strong>Account ID:</strong> {account.account_id}<br>")
            if hasattr(account, "industry"):
                html.append(f"<strong>Industry:</strong> {account.industry}<br>")
            if hasattr(account, "owner_name"):
                html.append(f"<strong>Owner:</strong> {account.owner_name}<br>")
            if hasattr(account, "mrr"):
                html.append(f"<strong>MRR:</strong> ${account.mrr:,}<br>")
            # Churn overview and score/classification
            if churn_report:
                html.append("<div class='overview'>")
                html.append(f"<strong>Churn Score:</strong> {churn_report.risk_score} &mdash; ")
                html.append(f"<strong>Classification:</strong> {churn_report.churn_risk_classification.title()}<br>")
                html.append(f"<strong>Overview:</strong> {churn_report.situation_overview}")
                html.append("</div>")
            else:
                html.append("<div class='not-sent'>No churn report available for this account.</div>")

            # Outreach email if sent
            if email:
                html.append("<div class='email'>")
                html.append(f"<strong>Email Subject:</strong> {email.email_subject}<br><br>")
                html.append(f"{email.email_content}")
                html.append("</div>")
            else:
                html.append("<div class='not-sent'>No outreach email sent for this account.</div>")

            html.append("</div>")  # end account-block

        html.append("</body></html>")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))

        print(f"HTML report written to '{html_path}'")



def kickoff():
    churn_monitor_flow = ChurnMonitorFlow()
    churn_monitor_flow.kickoff()


def plot():
    churn_monitor_flow = ChurnMonitorFlow()
    churn_monitor_flow.plot()


if __name__ == "__main__":
    kickoff()
