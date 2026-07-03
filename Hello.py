from __future__ import annotations

import altair as alt
import streamlit as st

from utils import (
    ai_portfolio_insight,
    download_all_button,
    hero,
    metric_card,
    portfolio_score,
    seed_data,
    setup_page,
    status_label,
)

setup_page("DevPulse AI Portfolio Hub", "🧠")
seed_data()

hero(
    "DevPulse AI Portfolio Hub",
    "A complete Streamlit dashboard for tracking GitHub projects, developer skills, roadmap tasks, portfolio readiness, and AI-style improvement recommendations.",
    "Python Streamlit Portfolio Project",
)

projects = st.session_state.projects_df
skills = st.session_state.skills_df
tasks = st.session_state.tasks_df

score = portfolio_score(projects, skills, tasks)

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Portfolio Score", f"{score}%", status_label(score))

with col2:
    metric_card("Projects", str(len(projects)), "active portfolio records")

with col3:
    completed_projects = int(projects["Status"].eq("Completed").sum()) if not projects.empty else 0
    metric_card("Completed", str(completed_projects), "finished projects")

with col4:
    avg_confidence = skills["Confidence"].mean() if not skills.empty else 0
    metric_card("Skill Confidence", f"{avg_confidence:.0f}%", "average readiness")

st.divider()

insight = ai_portfolio_insight(projects, skills, tasks)

st.markdown(
    f"""
    <div class="{insight['box']}">
        <h3>{insight['title']}</h3>
        <p>{insight['text']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.15, 0.85])

with left:
    st.subheader("📌 Project Progress Overview")

    if projects.empty:
        st.info("No project data yet. Add projects from the Project Lab page.")
    else:
        chart_df = projects[["Project", "Progress", "Impact", "Complexity", "Status"]].copy()

        progress_chart = (
            alt.Chart(chart_df)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x=alt.X("Project:N", sort="-y", title="Project"),
                y=alt.Y("Progress:Q", title="Progress %"),
                color=alt.Color("Status:N", legend=alt.Legend(title="Status")),
                tooltip=["Project", "Progress", "Impact", "Complexity", "Status"],
            )
            .properties(height=360)
        )

        st.altair_chart(progress_chart, use_container_width=True)

with right:
    st.subheader("🎯 Priority Mix")

    if projects.empty:
        st.info("No priority data yet.")
    else:
        priority_df = projects["Priority"].value_counts().reset_index()
        priority_df.columns = ["Priority", "Count"]

        priority_chart = (
            alt.Chart(priority_df)
            .mark_arc(innerRadius=55)
            .encode(
                theta="Count:Q",
                color="Priority:N",
                tooltip=["Priority", "Count"],
            )
            .properties(height=360)
        )

        st.altair_chart(priority_chart, use_container_width=True)

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🧩 Skill Confidence")

    if skills.empty:
        st.info("No skill data yet.")
    else:
        skill_chart = (
            alt.Chart(skills)
            .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
            .encode(
                y=alt.Y("Skill:N", sort="-x"),
                x=alt.X("Confidence:Q", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color("Category:N", legend=None),
                tooltip=[
                    "Skill",
                    "Category",
                    "Current Level",
                    "Target Level",
                    "Confidence",
                ],
            )
            .properties(height=330)
        )

        st.altair_chart(skill_chart, use_container_width=True)

with col_b:
    st.subheader("✅ Task Status")

    if tasks.empty:
        st.info("No task data yet.")
    else:
        task_df = tasks["Status"].value_counts().reset_index()
        task_df.columns = ["Status", "Count"]

        task_chart = (
            alt.Chart(task_df)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x="Status:N",
                y="Count:Q",
                color="Status:N",
                tooltip=["Status", "Count"],
            )
            .properties(height=330)
        )

        st.altair_chart(task_chart, use_container_width=True)

st.divider()

st.subheader("📋 Current Portfolio Snapshot")
st.dataframe(projects, use_container_width=True, hide_index=True)

with st.sidebar:
    st.header("⚙️ Quick Actions")

    if st.button("Load / Reset Demo Data", use_container_width=True):
        seed_data(force=True)
        st.rerun()

    download_all_button()

    st.info("Use the pages in the sidebar to add projects, plan tasks, track skills, and export reports.")

st.markdown(
    '<p class="footer-note">Built with Streamlit, Python, Pandas and Altair · DevPulse AI Portfolio Hub</p>',
    unsafe_allow_html=True,
)
