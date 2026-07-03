from __future__ import annotations

import io
from datetime import date, datetime, timedelta
from typing import Dict

import pandas as pd
import streamlit as st

PROJECT_COLUMNS = [
    "Project",
    "Category",
    "Tech Stack",
    "Status",
    "Progress",
    "Impact",
    "Complexity",
    "Priority",
    "Due Date",
    "Notes",
]

SKILL_COLUMNS = [
    "Skill",
    "Category",
    "Current Level",
    "Target Level",
    "Confidence",
    "Weekly Hours",
    "Status",
]

TASK_COLUMNS = [
    "Task",
    "Project",
    "Type",
    "Priority",
    "Status",
    "Due Date",
]


def setup_page(title: str, icon: str = "🚀") -> None:
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    inject_css()


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
            --card-bg: rgba(255,255,255,0.05);
            --card-border: rgba(255,255,255,0.14);
            --accent: #38bdf8;
            --green: #22c55e;
            --purple: #8b5cf6;
            --red: #ef4444;
            --yellow: #f59e0b;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 4rem;
            max-width: 1280px;
        }

        .hero-card {
            background: linear-gradient(135deg, rgba(14,165,233,.95), rgba(124,58,237,.90));
            border: 1px solid rgba(255,255,255,.22);
            border-radius: 28px;
            padding: 34px 36px;
            box-shadow: 0 24px 70px rgba(0,0,0,.28);
            margin-bottom: 24px;
        }

        .hero-card h1 {
            font-size: clamp(42px, 7vw, 76px);
            line-height: .95;
            margin: 10px 0 14px 0;
            letter-spacing: -3px;
            color: white;
        }

        .hero-card p {
            color: #e0f2fe;
            font-size: 17px;
            line-height: 1.7;
            max-width: 900px;
        }

        .tag {
            display: inline-block;
            background: rgba(255,255,255,.18);
            color: #fff;
            border: 1px solid rgba(255,255,255,.18);
            border-radius: 999px;
            padding: 7px 12px;
            font-weight: 800;
            font-size: 13px;
        }

        .metric-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 20px;
            min-height: 120px;
        }

        .metric-card span {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 800;
        }

        .metric-card strong {
            color: #f8fafc;
            display: block;
            font-size: 32px;
            line-height: 1.1;
            margin-top: 8px;
        }

        .insight-box {
            background: rgba(56,189,248,.08);
            border-left: 5px solid #38bdf8;
            border-radius: 16px;
            padding: 18px 20px;
            margin: 14px 0;
        }

        .success-box {
            background: rgba(34,197,94,.08);
            border-left: 5px solid #22c55e;
            border-radius: 16px;
            padding: 18px 20px;
            margin: 14px 0;
        }

        .warning-box {
            background: rgba(245,158,11,.08);
            border-left: 5px solid #f59e0b;
            border-radius: 16px;
            padding: 18px 20px;
            margin: 14px 0;
        }

        .danger-box {
            background: rgba(239,68,68,.08);
            border-left: 5px solid #ef4444;
            border-radius: 16px;
            padding: 18px 20px;
            margin: 14px 0;
        }

        .pill {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(56,189,248,.15);
            color: #bae6fd;
            font-size: 12px;
            font-weight: 800;
            margin-right: 6px;
            margin-bottom: 8px;
        }

        .footer-note {
            color: #94a3b8;
            font-size: 13px;
            text-align: center;
            margin-top: 30px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 32px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def seed_data(force: bool = False) -> None:
    if force or "projects_df" not in st.session_state:
        today = date.today()

        st.session_state.projects_df = pd.DataFrame(
            [
                [
                    "ResearchMate AI",
                    "Academic Tool",
                    "Python, Streamlit, Pandas",
                    "In Progress",
                    78,
                    9,
                    8,
                    "High",
                    today + timedelta(days=7),
                    "Literature review planner and research matrix.",
                ],
                [
                    "AI Personal Finance Coach",
                    "Finance AI",
                    "JavaScript, LocalStorage",
                    "Completed",
                    100,
                    8,
                    7,
                    "Medium",
                    today - timedelta(days=2),
                    "Budget analysis and finance recommendation app.",
                ],
                [
                    "EcoPulse AI",
                    "Climate Tech",
                    "Python, Streamlit",
                    "Planning",
                    35,
                    8,
                    6,
                    "High",
                    today + timedelta(days=14),
                    "Carbon habit coach and eco dashboard.",
                ],
            ],
            columns=PROJECT_COLUMNS,
        )

    if force or "skills_df" not in st.session_state:
        st.session_state.skills_df = pd.DataFrame(
            [
                ["Python", "Programming", 7, 9, 78, 5, "Improving"],
                ["Streamlit", "Data App", 6, 9, 70, 4, "Improving"],
                ["JavaScript", "Frontend", 8, 9, 82, 4, "Strong"],
                ["PHP", "Backend", 7, 9, 76, 3, "Improving"],
                ["AI/ML", "Artificial Intelligence", 5, 8, 58, 5, "Learning"],
                ["AWS", "Deployment", 4, 7, 45, 2, "Learning"],
            ],
            columns=SKILL_COLUMNS,
        )

    if force or "tasks_df" not in st.session_state:
        today = date.today()

        st.session_state.tasks_df = pd.DataFrame(
            [
                [
                    "Add screenshots to README",
                    "ResearchMate AI",
                    "Documentation",
                    "Medium",
                    "Todo",
                    today + timedelta(days=1),
                ],
                [
                    "Improve mobile layout",
                    "EcoPulse AI",
                    "Frontend",
                    "High",
                    "Todo",
                    today + timedelta(days=3),
                ],
                [
                    "Add changelog",
                    "AI Personal Finance Coach",
                    "Maintenance",
                    "Low",
                    "Done",
                    today - timedelta(days=1),
                ],
                [
                    "Create Streamlit deployment guide",
                    "hello-streamlit-pro",
                    "Documentation",
                    "High",
                    "In Progress",
                    today + timedelta(days=2),
                ],
            ],
            columns=TASK_COLUMNS,
        )


def project_score(row: pd.Series) -> int:
    progress = float(row.get("Progress", 0))
    impact = float(row.get("Impact", 0)) * 10
    complexity = float(row.get("Complexity", 0)) * 10

    priority_bonus = {
        "High": 10,
        "Medium": 6,
        "Low": 3,
    }.get(str(row.get("Priority", "Medium")), 5)

    status_bonus = {
        "Completed": 12,
        "In Progress": 8,
        "Planning": 3,
        "On Hold": 0,
    }.get(str(row.get("Status", "Planning")), 3)

    score = progress * 0.35 + impact * 0.25 + complexity * 0.20 + priority_bonus + status_bonus

    return int(min(100, score))


def portfolio_score(projects: pd.DataFrame, skills: pd.DataFrame, tasks: pd.DataFrame) -> int:
    if projects.empty and skills.empty:
        return 0

    project_component = projects.apply(project_score, axis=1).mean() if not projects.empty else 0
    skill_component = skills["Confidence"].mean() if not skills.empty else 0
    done_ratio = tasks["Status"].eq("Done").mean() * 100 if not tasks.empty else 0

    return int(round(project_component * 0.50 + skill_component * 0.30 + done_ratio * 0.20))


def status_label(score: int) -> str:
    if score >= 85:
        return "Portfolio Ready"
    if score >= 70:
        return "Strong Progress"
    if score >= 50:
        return "Needs More Polish"
    return "Early Stage"


def ai_portfolio_insight(
    projects: pd.DataFrame,
    skills: pd.DataFrame,
    tasks: pd.DataFrame,
) -> Dict[str, str]:
    score = portfolio_score(projects, skills, tasks)

    overdue = 0

    if not tasks.empty:
        due_dates = pd.to_datetime(tasks["Due Date"], errors="coerce").dt.date
        overdue = int(((due_dates < date.today()) & ~tasks["Status"].eq("Done")).sum())

    if projects.empty:
        return {
            "title": "Start by adding at least one project",
            "text": "Add a portfolio project with clear category, progress, impact score, and notes.",
            "box": "warning-box",
        }

    if overdue > 0:
        return {
            "title": "You have overdue portfolio tasks",
            "text": f"There are {overdue} overdue task(s). Focus on finishing or rescheduling them before adding new features.",
            "box": "danger-box",
        }

    if score >= 85:
        return {
            "title": "Your portfolio is strong",
            "text": "Focus on polishing README screenshots, live links, project topics, and deployment instructions.",
            "box": "success-box",
        }

    if not skills.empty and skills["Confidence"].mean() < 60:
        return {
            "title": "Skill confidence can improve",
            "text": "Choose 2 skills to improve this week and connect them to one visible GitHub commit.",
            "box": "warning-box",
        }

    return {
        "title": "Good progress, keep maintaining",
        "text": "Instead of creating new repos only, add changelogs, issues, roadmaps, screenshots, and small feature improvements.",
        "box": "insight-box",
    }


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def dataframe_to_excel_bytes(sheets: Dict[str, pd.DataFrame]) -> bytes:
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name[:31])

    return output.getvalue()


def date_safe(value) -> date:
    if isinstance(value, date):
        return value

    if isinstance(value, datetime):
        return value.date()

    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return date.today()

    return parsed.date()


def format_project_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    output = df.copy()
    output["Portfolio Score"] = output.apply(project_score, axis=1)
    output["Due Date"] = output["Due Date"].apply(lambda x: date_safe(x).isoformat())

    return output


def metric_card(title: str, value: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <span>{title}</span>
            <strong>{value}</strong>
            <small style="color:#94a3b8;">{subtitle}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, tag: str = "Streamlit Portfolio Project") -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <span class="tag">{tag}</span>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def download_all_button() -> None:
    data = dataframe_to_excel_bytes(
        {
            "Projects": format_project_table(st.session_state.projects_df),
            "Skills": st.session_state.skills_df,
            "Tasks": st.session_state.tasks_df,
        }
    )

    st.download_button(
        "⬇️ Download Full Portfolio Workbook",
        data=data,
        file_name="devpulse-portfolio-workbook.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
