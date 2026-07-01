# Project Intelligence Dashboard — Demo

A Streamlit demo of the Power BI dashboard for the **Hybrid Copilot Studio + Azure AI Foundry** AI Agent solution.

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)

## Features

- 📊 **Portfolio Overview** — programme rollup KPIs, budget variance, schedule trend
- 📁 **Project Detail** — per-project KPIs, budget trend, completion gauge, action items
- ⚠️ **Risk Intelligence** — heatmap, ML prediction probabilities, risk register
- 📋 **WSR Reports** — auto-generated weekly status report summaries
- 📝 **Meeting Minutes** — auto-extracted decisions, risks, and action items from Teams
- 💬 **Ask the Agent** — AI chat interface (simulates Azure AI Foundry + Copilot Studio)
- 🔧 **Admin Panel** — agent configuration, RBAC matrix, observability, audit log

## Role-Based Access Control (RBAC) Demo

Switch between these login identities using the sidebar:

| User | Role | What They See |
|------|------|---------------|
| Priya Sharma (Project Manager) | PM | Single project, full detail |
| Karan Verma (Delivery Head) | Executive | All projects, read-only rollup |
| IT Admin | Admin | Everything + config + audit |
| Riya Patel (Viewer - Finance) | Viewer | 2 assigned projects, KPI tiles only |

## Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your forked repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

## Local Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Production Architecture

In production this dashboard is replaced by **Power BI Embedded** connected to:
- **Azure AI Foundry** (4 AI agents)
- **Azure SQL Database** (shared data store)
- **Azure Entra ID** (real RBAC / Row-Level Security)
- **Copilot Studio** (Teams chat front door)

This Streamlit demo simulates the same UX with dummy data for demonstration purposes.
