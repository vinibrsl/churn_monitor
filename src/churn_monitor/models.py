from typing import Literal, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class OutreachEmail(BaseModel):
    account_id: str
    email_subject: str
    email_content: str
    commitments: list[str] = Field(
        ...,
        description="Specific commitments or promises made in the email that the sender must fulfill (e.g., 'Schedule engineer call by Thursday', 'Provide root cause analysis within 48 hours').",
    )

class ChurnReport(BaseModel):
    risk_score: int = Field(
        ...,
        description="Risk score (0-10) for this account; higher values indicate higher risk of churn.",
        ge=0,
        le=10
    )
    success_metrics: list[str] = Field(
        ...,
        description="The customer's primary goals, KPIs, or outcomes for using the product.",
    )
    supporting_evidence: list[str] = Field(
        ...,
        description="Facts, observations, or interactions used to justify the assigned risk score.",
    )
    churn_risk_classification: Literal["low", "medium", "high"] = Field(
        ...,
        description="Overall risk category for churn, based on analysis.",
    )
    situation_overview: str = Field(
        ...,
        description="Brief narrative summary explaining the current account context and risk factors. CRITICAL: This is CUSTOMER-FACING text. Focus on THEIR business impact and technical issues. NEVER include our internal revenue figures, financial exposure, or amounts 'at risk' for our company.",
    )

class Account(BaseModel):
    account_id: str
    org_name: str
    domain: str
    org_bio: str
    industry: str
    mrr: int
    renewal_date: str
    owner_name: str
    owner_email: str
    churn_report: Optional[ChurnReport] = None

class SupportTicket(BaseModel):
    ticket_id: str
    account_id: str
    created_at: datetime
    sender: Literal["customer", "agent"]
    message: str
