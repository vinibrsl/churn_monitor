import json
from datetime import datetime
from churn_monitor.models import Account, SupportTicket

class Client:
    def list_accounts(self) -> list[Account]:
        with open('src/churn_monitor/fixtures/accounts.json', encoding='utf-8') as file:
            data = json.load(file)
        return [Account.model_validate(attrs) for attrs in data]

    def list_support_tickets(self, account_id: str) -> list[SupportTicket]:
        with open('src/churn_monitor/fixtures/support_interactions.json', encoding='utf-8') as file:
            data = json.load(file)
        tickets = [
            SupportTicket.model_validate(attrs)
            for attrs in data
            if attrs.get('account_id') == account_id
        ]
        return sorted(tickets, key=lambda t: t.created_at)