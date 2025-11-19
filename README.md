# Churn Monitor

A CrewAI Flow demo for identifying and preventing customer churn through AI-powered analysis and automated email outreach.

Demoed at [CrewAI Signal 2025 - Complex Event-based Agentic Workflows Workshop](https://docs.google.com/presentation/d/1BwrIBhyLJkmfgl16ePSH_dQP4GS7DWh4HOm8QEXQIHg/edit?usp=sharing).

<img height="500" alt="image" src="https://github.com/user-attachments/assets/a6779dc6-c8dc-4499-a229-1553b1e4e296" />

## Overview

This project demonstrates an agentic system that:

- **Analyzes customer data** - Reviews account information and support interactions
- **Classifies churn risk** - Identifies customers at high, medium, or low risk of churning
- **Generates personalized emails** - Creates targeted outreach to prevent churn
- **Produces reports** - Outputs an HTML report with findings and recommendations

> **Note:** All data used in this project is fictional and generated for demonstration purposes only.

## Quick Start

### Prerequisites

- Python >=3.10 <3.14
- [UV](https://docs.astral.sh/uv/) package manager
- [CrewAI](https://docs.crewai.com/en/installation)
- Anthropic API key

### Installation

```bash
# Install UV
pip install uv

# Install dependencies
crewai install
```

Create a `.env` file in the project root:

```bash
ANTHROPIC_API_KEY=your_key_here
```

### Running

```bash
crewai flow kickoff
```

The flow will analyze the data and generate a churn risk report at `reports/churn_risk_report.html`.

## Questions?

Feel free to reach out at vini[at]hey[dot]com 🙃
