from pathlib import Path
from typing import Literal
import json
import jinja2
import churn_monitor.models

def generate_html_report(
    accounts: list[churn_monitor.models.Account],
    emails_by_account: dict[str, churn_monitor.models.OutreachEmail]
) -> str:
    template_dir = Path(__file__).parent / "templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template("churn_risk_report.html")
    return template.render(accounts=accounts, emails_by_account=emails_by_account)

def generate_json_report(
    accounts: list[churn_monitor.models.Account],
    emails_by_account: dict[str, churn_monitor.models.OutreachEmail]
) -> str:
    output = {
        "accounts": [account.model_dump() for account in accounts],
        "emails_by_account": {k: v.model_dump() for k, v in emails_by_account.items()},
    }
    return json.dumps(output, indent=2)

def write_report_to_file(content: str, fmt: Literal["json", "html"]) -> str:
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"churn_risk_report.{fmt}"
    path.write_text(content, encoding="utf-8")
    return str(path)