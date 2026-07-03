from __future__ import annotations

import pandas as pd
import streamlit as st

from utils import (
    ai_portfolio_insight,
    dataframe_to_csv_bytes,
    download_all_button,
    format_project_table,
    hero,
    portfolio_score,
    seed_data,
    setup_page,
    status_label,
)

setup_page("Report Export", "📄")
seed_data()

hero(
    "Portfolio Report Export",
    "Generate a portfolio-ready summary, download project/skill/task datasets, and copy AI-style recommendations for your GitHub README or LinkedIn updates.",
    "Reporting Dashboard",
)

projects = st.session_state.projects_df
skills = st.session_state.skills_df
tasks = st.session_state.tasks_df

score = portfolio_score(projects, skills, tasks)
insight = ai_portfolio_insight(projects, skills, tasks)

st.subheader("📌 Executive Summary")

completed_projects = int(projects["Status"].eq("Completed").sum()) if not projects.empty else 0
average_confidence = skills["Confidence"].mean() if not skills.empty else 0
completed_tasks = int(tasks["Status"].eq("Done").sum()) if not tasks.empty else 0

summary = f"""
Developer Portfolio Summary

Portfolio Score: {score}% ({status_label(score)})
Total Projects: {len(projects)}
Completed Projects: {completed_projects}
Tracked Skills: {len(skills)}
Average Skill Confidence: {average_confidence:.0f}%
Planned Contribution Tasks: {len(tasks)}
Completed Tasks: {completed_tasks}

AI-Style Insight:
{insight['title']} - {insight['text']}

Recommended Next Actions:
1. Add screenshots and live demo links to top repositories.
2. Create or update CHANGELOG.md for maintained projects.
3. Open real GitHub issues for planned improvements.
4. Use small pull requests for documentation and UI fixes.
5. Keep project topics, descriptions, and READMEs consistent.
""".strip()

st.text_area("Generated Portfolio Summary", value=summary, height=320)

st.download_button(
    "⬇️ Download Summary TXT",
    data=summary.encode("utf-8"),
    file_name="devpulse-portfolio-summary.txt",
    mime="text/plain",
    use_container_width=True,
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Dataset Downloads")

    st.download_button(
        "Download Projects CSV",
        data=dataframe_to_csv_bytes(format_project_table(projects)),
        file_name="projects.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.download_button(
        "Download Skills CSV",
        data=dataframe_to_csv_bytes(skills),
        file_name="skills.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.download_button(
        "Download Tasks CSV",
        data=dataframe_to_csv_bytes(tasks),
        file_name="tasks.csv",
        mime="text/csv",
        use_container_width=True,
    )

    download_all_button()

with col2:
    st.subheader("🧠 README Improvement Checklist")

    checklist = pd.DataFrame(
        [
            ["Repository description added", "High"],
            ["Topics added", "High"],
            ["Live demo link available", "High"],
            ["Screenshots included", "Medium"],
            ["Features list updated", "High"],
            ["Tech stack included", "Medium"],
            ["Roadmap section added", "Medium"],
            ["Changelog added", "Medium"],
            ["Contribution guide added", "Low"],
            ["Release created", "Low"],
        ],
        columns=["Checklist Item", "Priority"],
    )

    st.dataframe(checklist, use_container_width=True, hide_index=True)

st.divider()

st.subheader("🗂️ Current Project Report")
st.dataframe(format_project_table(projects), use_container_width=True, hide_index=True)

st.subheader("🧩 Current Skill Report")
st.dataframe(skills, use_container_width=True, hide_index=True)

st.subheader("✅ Current Contribution Task Report")
st.dataframe(tasks, use_container_width=True, hide_index=True)
