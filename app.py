import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Project Intelligence Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
[data-testid="stAppViewContainer"] { background: #F4F6FA; }
[data-testid="stSidebar"] { background: #1F3864; }
[data-testid="stSidebar"] * { color: #E8EEF7 !important; }
[data-testid="stSidebar"] .stRadio > label { color: #E8EEF7 !important; font-weight: 600; }
[data-testid="stSidebar"] hr { border-color: #2E75B6; }

/* Fix: dropdown widgets have a white background, so their text must stay dark */
[data-testid="stSidebar"] [data-baseweb="select"] { background: white; border-radius: 6px; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #1F3864 !important; }
[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #1F3864 !important; }
/* Dropdown menu list is rendered in a portal outside the sidebar */
[data-baseweb="popover"] [data-baseweb="menu"] { background: white !important; }
[data-baseweb="popover"] [data-baseweb="menu"] li,
[data-baseweb="popover"] [data-baseweb="menu"] li * { color: #1F3864 !important; }
[data-baseweb="popover"] [data-baseweb="menu"] li:hover { background: #E8EEF7 !important; }

/* Sidebar logo */
.sidebar-logo {
    text-align: center; font-size: 20px; font-weight: 800;
    letter-spacing: 3px; color: #FFFFFF; background: #2E75B6;
    border-radius: 8px; padding: 8px 0; margin-bottom: 14px;
}

/* Top header bar */
.top-bar {
    background: linear-gradient(90deg, #1F3864, #2E75B6);
    padding: 16px 28px; border-radius: 10px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px; color: white;
}
.top-bar h1 { margin: 0; font-size: 22px; font-weight: 700; }
.top-bar span { font-size: 13px; opacity: 0.85; }

/* KPI cards */
.kpi-card {
    background: white; border-radius: 10px; padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07); border-left: 5px solid #2E75B6;
    margin-bottom: 10px;
}
.kpi-card.green  { border-left-color: #3D8B37; }
.kpi-card.amber  { border-left-color: #D4870A; }
.kpi-card.red    { border-left-color: #C0392B; }
.kpi-card.blue   { border-left-color: #2E75B6; }
.kpi-label { font-size: 12px; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 4px; }
.kpi-value { font-size: 28px; font-weight: 800; color: #1F3864; line-height: 1; }
.kpi-sub   { font-size: 12px; color: #888; margin-top: 4px; }

/* Section headers */
.section-title {
    font-size: 15px; font-weight: 700; color: #1F3864;
    border-bottom: 2px solid #2E75B6; padding-bottom: 6px;
    margin: 18px 0 12px 0;
}

/* Role badge */
.role-badge {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 11px; font-weight: 700; color: white;
}
.role-Admin    { background: #1F3864; }
.role-PM       { background: #2E75B6; }
.role-Executive { background: #7B3F99; }
.role-Viewer   { background: #3D8B37; }

/* Risk badge */
.risk-high   { background: #FADBD8; color: #922B21; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }
.risk-medium { background: #FDEBD0; color: #935116; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }
.risk-low    { background: #D5F5E3; color: #1E8449; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; }

/* Chat area */
.chat-container {
    background: white; border-radius: 10px; padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07); height: 300px;
    overflow-y: auto;
}
.chat-msg-user { background: #E8EEF7; border-radius: 10px 10px 0 10px; padding: 8px 14px; margin: 6px 0; display: inline-block; max-width: 80%; float: right; clear: both; font-size: 13px; }
.chat-msg-ai   { background: #1F3864; color: white; border-radius: 10px 10px 10px 0; padding: 8px 14px; margin: 6px 0; display: inline-block; max-width: 85%; float: left; clear: both; font-size: 13px; }
.clearfix { clear: both; }

/* Health dot */
.dot-green  { color: #3D8B37; font-size: 16px; }
.dot-amber  { color: #D4870A; font-size: 16px; }
.dot-red    { color: #C0392B; font-size: 16px; }

/* Table styles */
.styled-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.styled-table th { background: #1F3864; color: white; padding: 8px 12px; text-align: left; }
.styled-table td { padding: 8px 12px; border-bottom: 1px solid #eee; }
.styled-table tr:nth-child(even) td { background: #F8F9FC; }

/* WSR summary box */
.wsr-box { background: white; border-radius: 10px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.07); font-size: 13px; line-height: 1.7; }
.wsr-box strong { color: #1F3864; }

/* Action items */
.action-item { display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px; }
.action-done { text-decoration: line-through; color: #aaa; }
</style>
""", unsafe_allow_html=True)

# ── DUMMY DATA ─────────────────────────────────────────────────────────────
PROJECTS = ["Alpha Migration", "Beta Platform Rebuild", "Gamma Data Lake", "Delta CRM Integration", "Epsilon Cloud Migration"]

ROLES = {
    "Priya Sharma (Project Manager)": "PM",
    "Karan Verma (Delivery Head)": "Executive",
    "IT Admin": "Admin",
    "Riya Patel (Viewer - Finance)": "Viewer",
}

PROJECT_ACCESS = {
    "PM": ["Alpha Migration", "Delta CRM Integration"],
    "Executive": ["Alpha Migration", "Beta Platform Rebuild", "Gamma Data Lake", "Delta CRM Integration", "Epsilon Cloud Migration"],
    "Admin": ["Alpha Migration", "Beta Platform Rebuild", "Gamma Data Lake", "Delta CRM Integration", "Epsilon Cloud Migration"],
    "Viewer": ["Alpha Migration", "Beta Platform Rebuild"],
}

PROJECT_DATA = {
    "Alpha Migration": {
        "health": "Amber", "budget_plan": 780000, "budget_actual": 828360,
        "schedule_days": -4, "utilisation": 87, "team_size": 11,
        "pm": "Priya Sharma", "phase": "Development",
        "completion": 62,
    },
    "Beta Platform Rebuild": {
        "health": "Green", "budget_plan": 950000, "budget_actual": 939550,
        "schedule_days": 0, "utilisation": 91, "team_size": 14,
        "pm": "Arjun Lee", "phase": "Testing",
        "completion": 78,
    },
    "Gamma Data Lake": {
        "health": "Red", "budget_plan": 620000, "budget_actual": 709900,
        "schedule_days": -11, "utilisation": 95, "team_size": 9,
        "pm": "Sara Khan", "phase": "Development",
        "completion": 45,
    },
    "Delta CRM Integration": {
        "health": "Green", "budget_plan": 430000, "budget_actual": 431720,
        "schedule_days": 0, "utilisation": 82, "team_size": 7,
        "pm": "Rohan Mehta", "phase": "UAT",
        "completion": 88,
    },
    "Epsilon Cloud Migration": {
        "health": "Green", "budget_plan": 550000, "budget_actual": 537350,
        "schedule_days": 2, "utilisation": 78, "team_size": 10,
        "pm": "Arjun Lee", "phase": "Deployment",
        "completion": 93,
    },
}

RISKS = {
    "Alpha Migration": [
        {"id": "R001", "description": "Vendor API integration delayed by 5 days", "severity": "High", "probability": 82, "owner": "Rohan Mehta", "due": "2026-07-05", "status": "Open"},
        {"id": "R002", "description": "UAT resource availability gap in week 4", "severity": "High", "probability": 74, "owner": "Priya Sharma", "due": "2026-07-08", "status": "Open"},
        {"id": "R003", "description": "Module 3 scope creep risk identified in meeting", "severity": "Medium", "probability": 58, "owner": "Arjun Lee", "due": "2026-07-10", "status": "In Progress"},
        {"id": "R004", "description": "Cloud compute costs trending above baseline", "severity": "Medium", "probability": 63, "owner": "Priya Sharma", "due": "2026-07-04", "status": "Open"},
        {"id": "R005", "description": "Stakeholder sign-off delay on design docs", "severity": "Low", "probability": 35, "owner": "Sara Khan", "due": "2026-07-12", "status": "Open"},
    ],
    "Beta Platform Rebuild": [
        {"id": "R006", "description": "Third-party auth library deprecation", "severity": "Medium", "probability": 48, "owner": "Arjun Lee", "due": "2026-07-15", "status": "Open"},
        {"id": "R007", "description": "Load test environment provisioning pending", "severity": "Low", "probability": 30, "owner": "Rohan Mehta", "due": "2026-07-06", "status": "In Progress"},
    ],
    "Gamma Data Lake": [
        {"id": "R008", "description": "Pipeline ingestion failure on legacy source system", "severity": "High", "probability": 88, "owner": "Sara Khan", "due": "2026-07-03", "status": "Open"},
        {"id": "R009", "description": "Data quality issues causing downstream failures", "severity": "High", "probability": 79, "owner": "Sara Khan", "due": "2026-07-04", "status": "Open"},
        {"id": "R010", "description": "Budget overrun likely to exceed 15% threshold", "severity": "High", "probability": 91, "owner": "Karan Verma", "due": "2026-07-05", "status": "Open"},
    ],
    "Delta CRM Integration": [
        {"id": "R011", "description": "Minor API response latency from CRM vendor", "severity": "Low", "probability": 28, "owner": "Rohan Mehta", "due": "2026-07-20", "status": "Open"},
    ],
    "Epsilon Cloud Migration": [],
}

ACTIONS = {
    "Alpha Migration": [
        {"task": "Vendor escalation call — confirm API delivery date", "owner": "Rohan Mehta", "due": "2026-07-03", "done": False, "source": "Jun 27 sprint review"},
        {"task": "Finalise module 3 scope doc and send for sign-off", "owner": "Arjun Lee", "due": "2026-07-05", "done": False, "source": "Jun 27 sprint review"},
        {"task": "UAT plan circulated to QA team", "owner": "Sara Khan", "due": "2026-06-28", "done": True, "source": "Jun 25 planning meeting"},
        {"task": "Cost variance review with finance", "owner": "Priya Sharma", "due": "2026-07-04", "done": False, "source": "Jun 27 sprint review"},
        {"task": "Re-baseline schedule after vendor delay confirmed", "owner": "Priya Sharma", "due": "2026-07-08", "done": False, "source": "Jun 27 sprint review"},
    ],
    "Beta Platform Rebuild": [
        {"task": "Auth library replacement evaluation", "owner": "Arjun Lee", "due": "2026-07-07", "done": False, "source": "Jun 26 tech review"},
        {"task": "Load test plan approved", "owner": "Rohan Mehta", "due": "2026-06-30", "done": True, "source": "Jun 26 tech review"},
    ],
    "Gamma Data Lake": [
        {"task": "Emergency call with legacy system vendor", "owner": "Sara Khan", "due": "2026-07-02", "done": False, "source": "Jun 28 incident review"},
        {"task": "Data quality remediation sprint planned", "owner": "Sara Khan", "due": "2026-07-03", "done": False, "source": "Jun 28 incident review"},
        {"task": "Escalate budget overrun to steering committee", "owner": "Karan Verma", "due": "2026-07-04", "done": False, "source": "Jun 28 incident review"},
    ],
    "Delta CRM Integration": [
        {"task": "UAT sign-off document submitted", "owner": "Rohan Mehta", "due": "2026-07-01", "done": True, "source": "Jun 25 UAT meeting"},
    ],
    "Epsilon Cloud Migration": [
        {"task": "Deployment runbook review", "owner": "Arjun Lee", "due": "2026-07-01", "done": True, "source": "Jun 26 deployment planning"},
    ],
}

WSR_SUMMARIES = {
    "Alpha Migration": """**Overall health: 🟡 Amber.** Module 3 development is 4 days behind plan due to a delayed vendor API integration. The team is working on a mitigation path including a parallel code stub approach. UAT environment was provisioned on June 25 and testing is on track to begin July 2. Budget tracking 6.2% over baseline, primarily driven by extended cloud compute usage during development. Stakeholder sign-off on design documents is pending and is flagged as a potential future risk if not resolved by July 5.""",
    "Beta Platform Rebuild": """**Overall health: 🟢 Green.** All development milestones completed on schedule. Integration testing began June 27 and is progressing well with 68% of test cases passed. A minor risk has been identified around a third-party authentication library that may need replacement before go-live. No budget concerns at this time — tracking 1.1% under baseline.""",
    "Gamma Data Lake": """**Overall health: 🔴 Red.** Significant issues this week. A legacy source system is producing malformed data, causing pipeline failures across 3 downstream consumers. This has pushed the schedule out by 11 days and is the primary driver of the 14.5% budget overrun. An emergency vendor call is scheduled. Steering committee review has been requested.""",
    "Delta CRM Integration": """**Overall health: 🟢 Green.** UAT completed with all critical test cases passing. Client sign-off document submitted July 1. Deployment is scheduled for July 14. Team utilisation is healthy at 82%. No open high-severity risks.""",
    "Epsilon Cloud Migration": """**Overall health: 🟢 Green.** Final deployment phase underway. 93% of workloads migrated successfully. Remaining tasks are non-critical reference data migration and post-migration validation. Project is 2 days ahead of schedule and tracking 2.3% under budget. Decommission of legacy infrastructure scheduled for July 20.""",
}

BUDGET_WEEKLY = {
    "Alpha Migration": [62000,65000,68000,71000,73000,76000,80000,84000,88000,90000],
    "Beta Platform Rebuild": [80000,82000,84000,83000,82000,81000,80000,79000,79000,80000],
    "Gamma Data Lake": [45000,48000,52000,60000,68000,75000,80000,85000,90000,92000],
    "Delta CRM Integration": [35000,37000,36000,37000,38000,38000,37000,36000,35000,36000],
    "Epsilon Cloud Migration": [42000,43000,45000,44000,44000,43000,42000,41000,40000,41000],
}

SCHEDULE_WEEKLY = {
    "Alpha Migration": [0,0,0,-1,-1,-2,-2,-3,-4,-4],
    "Beta Platform Rebuild": [0,1,1,1,0,0,0,0,0,0],
    "Gamma Data Lake": [0,-1,-2,-3,-5,-7,-8,-9,-11,-11],
    "Delta CRM Integration": [0,0,0,0,1,1,0,0,0,0],
    "Epsilon Cloud Migration": [1,1,2,2,2,2,2,2,2,2],
}

WEEKS = [f"W{i+1}" for i in range(10)]

AGENT_RUNS = [
    {"agent": "WSR Agent", "trigger": "Weekly (Mon 6am)", "last_run": "Jun 28, 06:02", "status": "Healthy", "duration": "2m 14s"},
    {"agent": "Portfolio Insights Agent", "trigger": "Daily (6am)", "last_run": "Jun 30, 06:00", "status": "Healthy", "duration": "3m 41s"},
    {"agent": "Risk Intelligence Agent", "trigger": "Daily (7am)", "last_run": "Jun 30, 07:01", "status": "Degraded", "duration": "5m 08s"},
    {"agent": "Meeting Intelligence Agent", "trigger": "On meeting end", "last_run": "Jun 30, 11:42", "status": "Healthy", "duration": "1m 22s"},
]

AUDIT_LOG = [
    {"time": "Jun 30, 09:10", "user": "Arjun Lee (PM)", "action": "Updated WSR template for Beta Platform Rebuild"},
    {"time": "Jun 30, 08:45", "user": "Admin", "action": "Added Priya Sharma to PM-ProjectAlpha group"},
    {"time": "Jun 29, 17:22", "user": "Karan Verma (Executive)", "action": "Viewed Gamma Data Lake risk summary"},
    {"time": "Jun 29, 14:03", "user": "Admin", "action": "Rotated Key Vault secret for ADO connector"},
    {"time": "Jun 28, 11:30", "user": "Sara Khan (PM)", "action": "Approved meeting minutes — Jun 27 sprint review"},
    {"time": "Jun 28, 08:15", "user": "Risk Agent", "action": "Flagged 3 new high-severity risks on Gamma Data Lake"},
]

MEETING_NOTES = {
    "Alpha Migration": {
        "date": "Jun 27, 2026 — Sprint Review",
        "attendees": "Priya Sharma, Arjun Lee, Rohan Mehta, Sara Khan, 4 others",
        "decisions": [
            "Vendor API stub approach approved as contingency — parallel development to begin July 1",
            "Module 3 scope freeze effective immediately — no new requests until July 15",
            "Budget review meeting to be held with Finance team before July 5",
        ],
        "risks_flagged": [
            "Vendor API delay (High) — escalation call to be organised by Rohan Mehta",
            "UAT staffing gap in Week 4 identified — Priya to arrange backup resources",
        ],
    }
}

# ── AI CHAT RESPONSES ───────────────────────────────────────────────────────
CHAT_RESPONSES = {
    "default": "I can answer questions about your projects, risks, budget, and schedule. Try asking things like 'Why is budget over on Alpha?' or 'What are the top risks this week?'",
    "budget": {
        "Alpha Migration": "Alpha Migration's budget is 6.2% over baseline ($48,360 over plan). The primary driver is extended cloud compute usage during the delayed vendor API integration phase. A finance review is scheduled for July 4.",
        "Gamma Data Lake": "Gamma Data Lake has a critical budget overrun of 14.5% ($89,900 over plan). This is driven by emergency remediation efforts on the legacy source system failure and the 11-day schedule extension. Steering committee escalation is recommended immediately.",
        "default": "Budget variance is being monitored across all projects. Use the project switcher to view a specific project's detail."
    },
    "risk": "The top 3 high-severity risks this week are: (1) Gamma Data Lake pipeline failure — 88% probability, owner: Sara Khan; (2) Gamma budget overrun exceeding 15% — 91% probability, owner: Karan Verma; (3) Alpha vendor API delay — 82% probability, owner: Rohan Mehta.",
    "schedule": "Two projects are behind schedule: Alpha Migration (4 days) and Gamma Data Lake (11 days). Beta, Delta, and Epsilon are on track or ahead. The Risk Agent predicts Gamma's delay is likely to extend further without vendor intervention.",
    "status": "Portfolio health: 3 Green, 1 Amber, 1 Red. Gamma Data Lake is the primary concern. Escalation to steering committee is recommended before the July 5 milestone gate.",
    "wsr": "The latest WSR reports were generated on June 28. All 5 projects have reports available. You can view the full summary in the WSR tab. Reports are automatically emailed to stakeholders every Monday at 6am.",
    "meeting": "The last meeting minutes were generated from the Alpha Migration sprint review on June 27. 5 action items were extracted, 1 has been completed. The Risk Agent linked 2 items to existing risks.",
}

def get_chat_response(question, project, role):
    q = question.lower()
    if any(w in q for w in ["budget", "cost", "spend", "over"]):
        if project in CHAT_RESPONSES["budget"]:
            return CHAT_RESPONSES["budget"][project]
        return CHAT_RESPONSES["budget"]["default"]
    if any(w in q for w in ["risk", "concern", "issue", "danger"]):
        return CHAT_RESPONSES["risk"]
    if any(w in q for w in ["schedule", "delay", "behind", "slip", "timeline"]):
        return CHAT_RESPONSES["schedule"]
    if any(w in q for w in ["status", "health", "overall", "summary", "portfolio"]):
        return CHAT_RESPONSES["status"]
    if any(w in q for w in ["wsr", "report", "weekly"]):
        return CHAT_RESPONSES["wsr"]
    if any(w in q for w in ["meeting", "minutes", "action"]):
        return CHAT_RESPONSES["meeting"]
    return CHAT_RESPONSES["default"]

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────
def health_dot(health):
    colours = {"Green": "🟢", "Amber": "🟡", "Red": "🔴"}
    return colours.get(health, "⚪")

def budget_variance(plan, actual):
    return (actual - plan) / plan * 100

def severity_color(sev):
    return {"High": "#C0392B", "Medium": "#E67E22", "Low": "#27AE60"}.get(sev, "#999")

def kpi_card(label, value, sub, colour="blue"):
    return f"""<div class="kpi-card {colour}">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    <div class="kpi-sub">{sub}</div>
</div>"""

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">YASHPMO</div>', unsafe_allow_html=True)
    st.markdown("## 🏗️ Project Intelligence")
    st.markdown("---")

    selected_user = st.selectbox("👤 Login as", list(ROLES.keys()))
    role = ROLES[selected_user]
    accessible = PROJECT_ACCESS[role]

    st.markdown(f"""<span class="role-badge role-{role}">{role}</span>""", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### Navigation")
    page = st.radio("", [
        "📊 Portfolio Overview",
        "📁 Project Detail",
        "⚠️ Risk Intelligence",
        "📋 WSR Reports",
        "📝 Meeting Minutes",
        "💬 Ask the Agent",
        "🔧 Admin Panel",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### Project Switcher")
    if role == "PM":
        project = st.selectbox("My Project", accessible)
    else:
        project = st.selectbox("Select Project", accessible)

    st.markdown("---")
    st.markdown(f"**Last refreshed:** {datetime.datetime.now().strftime('%b %d, %H:%M')}")
    st.markdown("*Auto-refresh: every 30 min*")

# ── HEADER ─────────────────────────────────────────────────────────────────
user_short = selected_user.split("(")[0].strip()
st.markdown(f"""<div class="top-bar">
<h1>🏗️ Project Intelligence Dashboard</h1>
<span>Logged in as <b>{user_short}</b> &nbsp;|&nbsp; Role: <b>{role}</b> &nbsp;|&nbsp; RBAC: {len(accessible)} project(s) accessible &nbsp;|&nbsp; Azure AI Foundry + Copilot Studio</span>
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: PORTFOLIO OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Portfolio Overview":
    if role == "Viewer":
        st.info("You have read-only access to summary KPIs for your assigned projects.")

    # ── Portfolio KPIs
    all_projects = [PROJECT_DATA[p] for p in accessible]
    green = sum(1 for p in all_projects if p["health"] == "Green")
    amber = sum(1 for p in all_projects if p["health"] == "Amber")
    red   = sum(1 for p in all_projects if p["health"] == "Red")
    total_plan   = sum(PROJECT_DATA[p]["budget_plan"] for p in accessible)
    total_actual = sum(PROJECT_DATA[p]["budget_actual"] for p in accessible)
    portfolio_variance = budget_variance(total_plan, total_actual)
    all_risks = [r for p in accessible for r in RISKS.get(p, [])]
    high_risks = sum(1 for r in all_risks if r["severity"] == "High" and r["status"] == "Open")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(kpi_card("Active Projects", str(len(accessible)),
            f"🟢 {green}  🟡 {amber}  🔴 {red}", "blue"), unsafe_allow_html=True)
    with k2:
        colour = "red" if portfolio_variance > 5 else "amber" if portfolio_variance > 0 else "green"
        st.markdown(kpi_card("Portfolio Budget Variance", f"{portfolio_variance:+.1f}%",
            f"${abs(total_actual - total_plan):,.0f} {'over' if total_actual > total_plan else 'under'} plan", colour), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("High-Severity Risks", str(high_risks),
            f"Across {len([p for p in accessible if any(r['severity']=='High' for r in RISKS.get(p,[]))])} projects",
            "red" if high_risks > 3 else "amber"), unsafe_allow_html=True)
    with k4:
        on_time = sum(1 for p in accessible if PROJECT_DATA[p]["schedule_days"] >= 0)
        pct = round(on_time / len(accessible) * 100) if accessible else 0
        st.markdown(kpi_card("On-Time Delivery", f"{pct}%",
            f"{on_time} of {len(accessible)} projects on schedule",
            "green" if pct >= 80 else "amber"), unsafe_allow_html=True)

    st.markdown('<div class="section-title">Programme Rollup — Portfolio Insights Agent</div>', unsafe_allow_html=True)

    # ── Rollup table
    rows = []
    for proj in accessible:
        d = PROJECT_DATA[proj]
        bv = budget_variance(d["budget_plan"], d["budget_actual"])
        high = sum(1 for r in RISKS.get(proj, []) if r["severity"] == "High" and r["status"] == "Open")
        sched = f"{d['schedule_days']} days behind" if d["schedule_days"] < 0 else ("On track" if d["schedule_days"] == 0 else f"{d['schedule_days']} days ahead")
        rows.append({
            "Project": proj,
            "Health": health_dot(d["health"]) + " " + d["health"],
            "Budget Variance": f"{bv:+.1f}%",
            "High Risks": str(high),
            "Schedule": sched,
            "Phase": d["phase"],
            "PM": d["pm"],
            "Completion": f"{d['completion']}%",
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True,
        column_config={"Completion": st.column_config.ProgressColumn("Completion", min_value=0, max_value=100)})

    st.markdown("")
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-title">Budget Variance by Project</div>', unsafe_allow_html=True)
        variances = [(p, budget_variance(PROJECT_DATA[p]["budget_plan"], PROJECT_DATA[p]["budget_actual"])) for p in accessible]
        df_var = pd.DataFrame(variances, columns=["Project", "Variance (%)"])
        colors = ["#C0392B" if v > 10 else "#E67E22" if v > 0 else "#27AE60" for v in df_var["Variance (%)"]]
        fig = go.Figure(go.Bar(
            x=df_var["Project"], y=df_var["Variance (%)"],
            marker_color=colors, text=[f"{v:+.1f}%" for v in df_var["Variance (%)"]],
            textposition="outside"
        ))
        fig.update_layout(margin=dict(t=10, b=10), height=260, plot_bgcolor="white",
            yaxis_title="Variance (%)", showlegend=False, xaxis_tickangle=-20)
        fig.add_hline(y=0, line_dash="dash", line_color="#1F3864", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-title">Schedule Slip Trend (All Projects)</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        colours_line = {"Alpha Migration": "#E67E22", "Gamma Data Lake": "#C0392B",
                        "Beta Platform Rebuild": "#27AE60", "Delta CRM Integration": "#2E75B6",
                        "Epsilon Cloud Migration": "#3498DB"}
        for proj in accessible:
            fig2.add_trace(go.Scatter(x=WEEKS, y=SCHEDULE_WEEKLY[proj], name=proj,
                line=dict(color=colours_line.get(proj, "#999"), width=2)))
        fig2.update_layout(margin=dict(t=10, b=10), height=260, plot_bgcolor="white",
            yaxis_title="Days (+ ahead / – behind)", legend=dict(orientation="h", y=-0.3))
        fig2.add_hline(y=0, line_dash="dot", line_color="#aaa")
        st.plotly_chart(fig2, use_container_width=True)

    if role in ["Executive", "Admin"]:
        st.markdown('<div class="section-title">AI Summary — Portfolio Insights Agent</div>', unsafe_allow_html=True)
        st.info("🤖 **Gamma Data Lake** is the primary portfolio concern: an 11-day schedule slip and a 14.5% budget overrun, both trending worse over the last 2 weeks. **Alpha Migration** is Amber with vendor-related delays. The remaining 3 projects are Green. Recommend a steering committee review on Gamma before the July 5 milestone gate.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: PROJECT DETAIL
# ════════════════════════════════════════════════════════════════════════════
elif page == "📁 Project Detail":
    d = PROJECT_DATA[project]
    bv = budget_variance(d["budget_plan"], d["budget_actual"])

    k1, k2, k3, k4 = st.columns(4)
    colour_sched = "green" if d["schedule_days"] >= 0 else "amber" if d["schedule_days"] >= -5 else "red"
    colour_bv    = "green" if bv < 0 else "amber" if bv < 8 else "red"
    risks_here   = RISKS.get(project, [])
    open_high    = sum(1 for r in risks_here if r["severity"] == "High" and r["status"] == "Open")

    with k1:
        label = "On track" if d["schedule_days"] == 0 else f"{abs(d['schedule_days'])}d {'ahead' if d['schedule_days'] > 0 else 'behind'}"
        st.markdown(kpi_card("Schedule Health", health_dot(d["health"]) + " " + label,
            f"Phase: {d['phase']}", colour_sched), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("Budget Variance", f"{bv:+.1f}%",
            f"${abs(d['budget_actual'] - d['budget_plan']):,.0f} {'over' if bv > 0 else 'under'} plan", colour_bv), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("Open High Risks", str(open_high),
            f"{len(risks_here)} total open risks", "red" if open_high >= 2 else "amber"), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_card("Team Utilisation", f"{d['utilisation']}%",
            f"{d['team_size']} active members", "green"), unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="section-title">Budget Trend (Weekly Actual Spend)</div>', unsafe_allow_html=True)
        weeks_data = BUDGET_WEEKLY[project]
        plan_flat = [d["budget_plan"] / 10] * 10
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=WEEKS, y=plan_flat, name="Plan", line=dict(dash="dash", color="#1F3864", width=2)))
        fig.add_trace(go.Scatter(x=WEEKS, y=weeks_data, name="Actual", fill="tozeroy",
            line=dict(color="#E67E22" if bv > 0 else "#27AE60", width=2),
            fillcolor="rgba(230,126,34,0.1)" if bv > 0 else "rgba(39,174,96,0.1)"))
        fig.update_layout(margin=dict(t=10, b=10), height=240, plot_bgcolor="white",
            yaxis_title="Spend ($)", legend=dict(orientation="h", y=-0.3))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Completion Progress</div>', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=d["completion"],
            gauge={"axis": {"range": [0, 100]},
                   "bar": {"color": "#27AE60" if d["completion"] > 75 else "#E67E22"},
                   "steps": [{"range": [0, 50], "color": "#FADBD8"}, {"range": [50, 75], "color": "#FDEBD0"}, {"range": [75, 100], "color": "#D5F5E3"}]},
            number={"suffix": "%", "font": {"size": 40}},
        ))
        fig_gauge.update_layout(margin=dict(t=30, b=10, l=20, r=20), height=220)
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown('<div class="section-title">Open Action Items — Meeting Intelligence Agent</div>', unsafe_allow_html=True)
    actions = ACTIONS.get(project, [])
    for a in actions:
        done_class = "action-done" if a["done"] else ""
        status_icon = "✅" if a["done"] else "☐"
        st.markdown(f"""<div class="action-item">
            <span>{status_icon}</span>
            <span class="{done_class}"><b>{a['task']}</b><br>
            <span style="color:#888;font-size:12px;">Owner: {a['owner']} &nbsp;|&nbsp; Due: {a['due']} &nbsp;|&nbsp; From: {a['source']}</span></span>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: RISK INTELLIGENCE
# ════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Risk Intelligence":
    st.markdown('<div class="section-title">Risk Heatmap — Risk Intelligence Agent (Azure ML + NLP Scoring)</div>', unsafe_allow_html=True)

    # All risks across accessible projects
    all_risk_rows = []
    for proj in accessible:
        for r in RISKS.get(proj, []):
            all_risk_rows.append({**r, "project": proj})

    if not all_risk_rows:
        st.success("No open risks across your accessible projects.")
    else:
        # Heatmap: probability vs severity
        df_r = pd.DataFrame(all_risk_rows)
        sev_map = {"High": 3, "Medium": 2, "Low": 1}
        df_r["sev_num"] = df_r["severity"].map(sev_map)

        fig_heat = go.Figure()
        colours_sev = {"High": "#C0392B", "Medium": "#E67E22", "Low": "#27AE60"}
        for sev in ["High", "Medium", "Low"]:
            sub = df_r[df_r["severity"] == sev]
            fig_heat.add_trace(go.Scatter(
                x=sub["probability"], y=[sev] * len(sub),
                mode="markers+text",
                marker=dict(size=22, color=colours_sev[sev], opacity=0.85, line=dict(color="white", width=2)),
                text=sub["id"], textposition="middle center",
                textfont=dict(color="white", size=10, family="Arial"),
                name=sev,
                hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>Project: %{customdata[2]}<br>Probability: %{x}%<extra></extra>",
                customdata=list(zip(sub["id"], sub["description"], sub["project"]))
            ))

        fig_heat.update_layout(
            height=260, margin=dict(t=10, b=10),
            xaxis=dict(title="Probability (%)", range=[0, 100]),
            yaxis=dict(title="Severity", categoryorder="array", categoryarray=["Low", "Medium", "High"]),
            plot_bgcolor="#FFF8F8", showlegend=True,
            shapes=[
                dict(type="rect", x0=0, x1=50, y0=-0.5, y1=0.5, fillcolor="#D5F5E3", opacity=0.3, line_width=0),
                dict(type="rect", x0=50, x1=75, y0=-0.5, y1=2.5, fillcolor="#FDEBD0", opacity=0.3, line_width=0),
                dict(type="rect", x0=75, x1=100, y0=-0.5, y1=2.5, fillcolor="#FADBD8", opacity=0.3, line_width=0),
            ]
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown('<div class="section-title">Risk Register</div>', unsafe_allow_html=True)
        df_display = df_r[df_r["status"] == "Open"].copy()
        df_display = df_display.sort_values("probability", ascending=False)

        for _, r in df_display.iterrows():
            col1, col2, col3, col4, col5 = st.columns([1, 4, 2, 2, 2])
            col1.markdown(f"<span style='background:{colours_sev[r['severity']]};color:white;padding:3px 8px;border-radius:10px;font-size:11px;font-weight:700'>{r['severity']}</span>", unsafe_allow_html=True)
            col2.markdown(f"**{r['id']}** — {r['description']}")
            col3.markdown(f"📊 **{r['probability']}%** prob.")
            col4.markdown(f"👤 {r['owner']}")
            col5.markdown(f"📅 {r['due']}")

        # Risk trend by project (bubble chart)
        st.markdown('<div class="section-title">Risk Exposure by Project</div>', unsafe_allow_html=True)
        proj_risk_data = []
        for proj in accessible:
            risks_p = RISKS.get(proj, [])
            high_count = sum(1 for r in risks_p if r["severity"] == "High")
            avg_prob = round(sum(r["probability"] for r in risks_p) / len(risks_p)) if risks_p else 0
            proj_risk_data.append({"Project": proj, "High Risks": high_count, "Avg Probability": avg_prob, "Total Risks": len(risks_p)})
        df_bubble = pd.DataFrame(proj_risk_data)

        fig_bubble = px.scatter(df_bubble, x="Avg Probability", y="High Risks",
            size="Total Risks", color="High Risks",
            color_continuous_scale=[[0, "#27AE60"], [0.5, "#E67E22"], [1, "#C0392B"]],
            text="Project", size_max=50, hover_data=["Total Risks"])
        fig_bubble.update_traces(textposition="top center")
        fig_bubble.update_layout(height=300, margin=dict(t=10, b=10), plot_bgcolor="white")
        st.plotly_chart(fig_bubble, use_container_width=True)

        st.markdown('<div class="section-title">ML Prediction — Slippage & Budget Overrun Probability</div>', unsafe_allow_html=True)
        st.info("🤖 **Risk Intelligence Agent (Azure ML):** Based on historical data from 24 past projects, Gamma Data Lake has a 91% probability of exceeding the 15% budget threshold and a 79% probability of further schedule extension. Alpha Migration has a 68% probability of the vendor delay cascading into UAT phase. These predictions are updated daily from the trained scikit-learn model in Azure ML.")

        ml_data = {p: {"slippage_prob": max(0, min(99, 50 + PROJECT_DATA[p]["schedule_days"] * -6 + random.randint(-5, 5))),
                        "overrun_prob": max(0, min(99, max(0, budget_variance(PROJECT_DATA[p]["budget_plan"], PROJECT_DATA[p]["budget_actual"])) * 5 + random.randint(-5, 5)))}
                   for p in accessible}
        df_ml = pd.DataFrame([{"Project": p, "Slippage Probability (%)": ml_data[p]["slippage_prob"],
                                "Budget Overrun Probability (%)": ml_data[p]["overrun_prob"]} for p in accessible])
        fig_ml = go.Figure()
        fig_ml.add_trace(go.Bar(x=df_ml["Project"], y=df_ml["Slippage Probability (%)"], name="Schedule Slippage", marker_color="#E67E22"))
        fig_ml.add_trace(go.Bar(x=df_ml["Project"], y=df_ml["Budget Overrun Probability (%)"], name="Budget Overrun", marker_color="#C0392B"))
        fig_ml.update_layout(barmode="group", height=260, margin=dict(t=10, b=10),
            plot_bgcolor="white", yaxis_title="Probability (%)", legend=dict(orientation="h", y=-0.3))
        st.plotly_chart(fig_ml, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: WSR REPORTS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📋 WSR Reports":
    st.markdown('<div class="section-title">Weekly Status Reports — WSR Agent (Auto-generated every Monday)</div>', unsafe_allow_html=True)

    if role == "PM":
        proj_list = [project]
    else:
        proj_list = accessible

    for proj in proj_list:
        d = PROJECT_DATA[proj]
        bv = budget_variance(d["budget_plan"], d["budget_actual"])
        with st.expander(f"{health_dot(d['health'])}  {proj} — Latest WSR (generated Jun 28, 2026)", expanded=(proj == project)):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Health", d["health"])
            c2.metric("Budget Variance", f"{bv:+.1f}%")
            c3.metric("Schedule", f"{abs(d['schedule_days'])}d {'behind' if d['schedule_days'] < 0 else 'ahead' if d['schedule_days'] > 0 else 'on track'}")
            c4.metric("Completion", f"{d['completion']}%")

            st.markdown('<div class="wsr-box">' + WSR_SUMMARIES[proj] + "</div>", unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns(3)
            col_a.markdown("📧 **Auto-emailed to:** PM, Delivery Head, PMO")
            col_b.markdown("📁 **Template:** Project-specific (from Blob Storage)")
            col_c.markdown("📅 **Next generation:** Jul 7, 2026 (Mon 6am)")

    st.markdown("---")
    st.markdown('<div class="section-title">WSR Generation Flow</div>', unsafe_allow_html=True)
    st.markdown("""
    | Step | What Happens | Where |
    |------|-------------|-------|
    | 1. Upload | PM uploads WSR .docx to SharePoint | SharePoint document library |
    | 2. Trigger | Monday 6am — Azure Function wakes the WSR Agent | Azure AI Foundry |
    | 3. Parse | Document Intelligence extracts text | Azure Document Intelligence |
    | 4. Extract | GPT-4o pulls health, risks, milestones, actions | Azure AI Foundry Prompt Flow |
    | 5. Generate | Agent fills the project's PPT/Word template | python-pptx via Azure Function |
    | 6. Store | Completed report saved to SharePoint + Blob Storage | SharePoint + Azure Blob |
    | 7. Email | Graph API sends notification with link | Microsoft Graph API |
    | 8. Dashboard | Portfolio KPIs update on next scheduled refresh | Power BI / This dashboard |
    """)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: MEETING MINUTES
# ════════════════════════════════════════════════════════════════════════════
elif page == "📝 Meeting Minutes":
    st.markdown('<div class="section-title">Meeting Intelligence Agent — Auto-generated from Teams transcripts</div>', unsafe_allow_html=True)
    if project in MEETING_NOTES:
        m = MEETING_NOTES[project]
        st.markdown(f"**Meeting:** {m['date']} &nbsp;|&nbsp; **Attendees:** {m['attendees']}")
        st.markdown("")

        col_dec, col_risk = st.columns(2)
        with col_dec:
            st.markdown("#### ✅ Decisions Made")
            for dec in m["decisions"]:
                st.markdown(f"- {dec}")

        with col_risk:
            st.markdown("#### ⚠️ Risks Flagged in Meeting")
            for r in m["risks_flagged"]:
                st.markdown(f"- {r}")

        st.markdown("#### 📌 Action Items (auto-created in Microsoft To Do / Planner)")
        actions = ACTIONS.get(project, [])
        for a in actions:
            icon = "✅" if a["done"] else "🔲"
            style = "color:#aaa;text-decoration:line-through" if a["done"] else "color:#1F3864"
            st.markdown(f'{icon} <span style="{style}"><b>{a["task"]}</b> — {a["owner"]} (due {a["due"]})</span>', unsafe_allow_html=True)

        st.markdown("---")
        st.info("🤖 **Meeting Intelligence Agent** extracted these minutes automatically from the Jun 27 Teams recording transcript. Draft was shared with Priya Sharma for approval before distribution. Tasks were created in Microsoft To Do for each owner via Graph API.")
    else:
        st.info(f"No meeting minutes available for {project} yet. They will appear here automatically after the next Teams meeting ends.")

    st.markdown('<div class="section-title">Meeting Intelligence Flow</div>', unsafe_allow_html=True)
    st.markdown("""
    | Step | What Happens |
    |------|-------------|
    | Meeting ends in Teams | Webhook notification sent to Azure Function |
    | Transcript fetched | Graph API retrieves transcript text with speaker labels |
    | GPT-4o extracts structure | Decisions, risks, action items, owners, deadlines extracted |
    | Draft created | Stored in SharePoint page, visible to organiser for approval |
    | Organiser approves | Clicks 'Approve' — triggers distribution |
    | Tasks created | Graph API creates items in Microsoft To Do / Planner for each owner |
    | Reminders | Azure Function sends reminder if overdue |
    | Risk link | Any flagged risks linked to Risk Agent's Risks table automatically |
    """)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: ASK THE AGENT (CHAT)
# ════════════════════════════════════════════════════════════════════════════
elif page == "💬 Ask the Agent":
    st.markdown('<div class="section-title">Ask the Agent — Powered by Azure AI Foundry (GPT-4o) + Copilot Studio</div>', unsafe_allow_html=True)
    st.info(f"You are asking questions as **{user_short} ({role})**. Answers are scoped to your RBAC permissions — {len(accessible)} project(s) visible.")
    st.markdown("**Suggested questions:**")
    cols = st.columns(3)
    suggestions = [
        "What's the overall portfolio status?",
        "Why is budget over on Alpha Migration?",
        "What are the top risks this week?",
        "Which projects are behind schedule?",
        "When was the last WSR generated?",
        "What were the actions from the last meeting?",
    ]
    for i, s in enumerate(suggestions):
        if cols[i % 3].button(s, key=f"sug_{i}"):
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": s})
            resp = get_chat_response(s, project, role)
            st.session_state.messages.append({"role": "ai", "content": resp})

    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat
    chat_html = '<div class="chat-container">'
    if not st.session_state.messages:
        chat_html += '<div class="chat-msg-ai">👋 Hello! I\'m your Project Intelligence Agent. I can answer questions about your projects, risks, budget, and schedule. What would you like to know?</div><div class="clearfix"></div>'
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f'<div class="chat-msg-user">{msg["content"]}</div><div class="clearfix"></div>'
        else:
            chat_html += f'<div class="chat-msg-ai">🤖 {msg["content"]}</div><div class="clearfix"></div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)
    st.markdown("")

    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input("", placeholder="Ask anything about your projects...", label_visibility="collapsed", key="chat_input")
    with col_send:
        if st.button("Send 💬", use_container_width=True):
            if user_input.strip():
                st.session_state.messages.append({"role": "user", "content": user_input})
                resp = get_chat_response(user_input, project, role)
                st.session_state.messages.append({"role": "ai", "content": resp})
                st.rerun()

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("#### How this works in production")
    st.markdown("""
    - Simple Q&A (status, summary) → answered directly by **Copilot Studio** topics
    - Complex questions (budget analysis, risk explanations) → **escalated to Azure AI Foundry** via API
    - All answers **grounded** on real project data from the shared database
    - Responses **RBAC-filtered**: you only receive information your role permits
    """)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: ADMIN PANEL
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔧 Admin Panel":
    if role != "Admin":
        st.error("🔒 Access denied. This page is restricted to the Admin role.")
        st.markdown("Your current role is **" + role + "**. Contact your system administrator to request Admin access.")
        st.stop()

    st.markdown('<div class="section-title">Agent Configuration — Azure App Configuration</div>', unsafe_allow_html=True)
    df_agents = pd.DataFrame(AGENT_RUNS)
    df_agents["status_icon"] = df_agents["status"].map({"Healthy": "🟢 Healthy", "Degraded": "🟡 Degraded", "Error": "🔴 Error"})
    st.dataframe(df_agents[["agent", "trigger", "last_run", "status_icon", "duration"]].rename(columns={
        "agent": "Agent", "trigger": "Trigger", "last_run": "Last Run", "status_icon": "Status", "duration": "Duration"
    }), use_container_width=True, hide_index=True)

    st.warning("⚠️ **Risk Intelligence Agent** degraded: ML endpoint timeout on Gamma Data Lake at 07:01. SharePoint throttling detected on Beta Platform at 09:14.")

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown('<div class="section-title">RBAC Role Matrix (Entra ID Groups)</div>', unsafe_allow_html=True)
        rbac_df = pd.DataFrame([
            {"Role": "Admin", "Agents": "All 4", "Scope": "All projects", "Dashboard": "Full + Config + Audit"},
            {"Role": "Project Manager", "Agents": "WSR, Risk, Meeting", "Scope": "Own project only", "Dashboard": "Full project detail"},
            {"Role": "Executive", "Agents": "Portfolio, Risk (read)", "Scope": "Programme rollup", "Dashboard": "Executive summary"},
            {"Role": "Viewer", "Agents": "Portfolio (read)", "Scope": "Assigned projects", "Dashboard": "KPI tiles only"},
        ])
        st.dataframe(rbac_df, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown('<div class="section-title">Observability Metrics (App Insights)</div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg Run Latency", "4.2s", "-0.3s vs yesterday")
        m2.metric("Errors (24h)", "3", "+3 vs yesterday", delta_color="inverse")
        m3.metric("Agent Runs (24h)", "142", "+12 vs yesterday")

        fig_runs = go.Figure(go.Bar(
            x=["WSR Agent", "Portfolio", "Risk Agent", "Meeting"],
            y=[6, 24, 24, 88], marker_color=["#2E75B6", "#3D8B37", "#E67E22", "#7B3F99"]
        ))
        fig_runs.update_layout(height=150, margin=dict(t=5, b=5, l=5, r=5),
            plot_bgcolor="white", showlegend=False, yaxis_title="Runs (24h)")
        st.plotly_chart(fig_runs, use_container_width=True)

    st.markdown('<div class="section-title">Recent Audit Log</div>', unsafe_allow_html=True)
    df_audit = pd.DataFrame(AUDIT_LOG)
    st.dataframe(df_audit.rename(columns={"time": "Time", "user": "User", "action": "Action"}),
        use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Project Configuration (Azure App Configuration)</div>', unsafe_allow_html=True)
    config_df = pd.DataFrame([
        {"Key": f"ProjectAlpha:SharePoint:SiteUrl", "Value": "https://contoso.sharepoint.com/sites/alpha", "Last Updated": "Jun 1, 2026"},
        {"Key": f"ProjectAlpha:ADO:ProjectId", "Value": "alpha-001-ado", "Last Updated": "Jun 1, 2026"},
        {"Key": f"ProjectAlpha:Template:Name", "Value": "WSR_Template_Alpha_v2.pptx", "Last Updated": "Jun 15, 2026"},
        {"Key": f"ProjectGamma:SharePoint:SiteUrl", "Value": "https://contoso.sharepoint.com/sites/gamma", "Last Updated": "May 20, 2026"},
        {"Key": f"ProjectGamma:ADO:ProjectId", "Value": "gamma-003-ado", "Last Updated": "May 20, 2026"},
    ])
    st.dataframe(config_df, use_container_width=True, hide_index=True)
    st.caption("To add a new project: insert new key-value entries here. No code changes or agent redeployment needed.")
