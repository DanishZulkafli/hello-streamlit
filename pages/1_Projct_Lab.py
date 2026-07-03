
from __future__ import annotations

from datetime import date, timedelta

import altair as alt
import pandas as pd
import streamlit as st

from utils import (
    PROJECT_COLUMNS,
    dataframe_to_csv_bytes,
    format_project_table,
    hero,
    project_score,
    seed_data,
    setup_page,
)

setup_page("Project Lab", "🧪")
seed_data()

hero(
    "Project Lab",
    "Add, score, filter, and manage portfolio projects. Use this page to make your GitHub repositories look more maintained and professional.",
    "Project Management Dashboard",
)

projects = st.session_state.projects_df

with st.expander("➕ Add New Portfolio Project", expanded=True):
    with st.form("project_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            project = st.text_input(
                "Project Name",
                placeholder="Example: EcoPulse AI Carbon Habit Coach",
            )

            category = st.selectbox(
                "Category",
                [
                    "AI Tool",
                    "Academic Tool",
                    "Finance AI",
                    "Climate Tech",
                    "Wellness",
                    "Community Tool",
                    "Career Platform",
                    "Data App",
                    "Streamlit App",
                ],
            )

            tech = st.text_input(
                "Tech Stack",
                placeholder="Python, Streamlit, Pandas, Altair",
            )

            status = st.selectbox(
                "Status",
                ["Planning", "In Progress", "Completed", "On Hold"],
            )

        with col2:
            progress = st.slider("Progress", 0, 100, 40)
            impact = st.slider("Impact", 1, 10, 7)
            complexity = st.slider("Complexity", 1, 10, 6)
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            due_date = st.date_input("Due Date", value=date.today() + timedelta(days=7))

        notes = st.text_area(
            "Notes",
            placeholder="What problem does this project solve? What should be improved next?",
        )

        submitted = st.form_submit_button("Add Project", use_container_width=True)

    if submitted:
        if not project.strip():
            st.error("Project name is required.")
        else:
            new_row = pd.DataFrame(
                [
                    [
                        project,
                        category,
                        tech,
                        status,
                        progress,
                        impact,
                        complexity,
                        priority,
                        due_date,
                        notes,
                    ]
                ],
                columns=PROJECT_COLUMNS,
            )

            st.session_state.projects_df = pd.concat(
                [projects, new_row],
                ignore_index=True,
            )

            st.success("Project added successfully.")
            st.rerun()

st.subheader("🔍 Filter Projects")

col1, col2, col3 = st.columns(3)

with col1:
    selected_status = st.selectbox(
        "Status Filter",
        ["All"] + sorted(projects["Status"].dropna().unique().tolist()),
    )

with col2:
    selected_priority = st.selectbox(
        "Priority Filter",
        ["All"] + sorted(projects["Priority"].dropna().unique().tolist()),
    )

with col3:
    search = st.text_input("Search", placeholder="Search project or tech stack...")

filtered = projects.copy()

if selected_status != "All":
    filtered = filtered[filtered["Status"] == selected_status]

if selected_priority != "All":
    filtered = filtered[filtered["Priority"] == selected_priority]

if search:
    mask = filtered.apply(
        lambda row: search.lower() in " ".join(map(str, row.values)).lower(),
        axis=1,
    )

    filtered = filtered[mask]

if filtered.empty:
    st.warning("No projects match the current filter.")
else:
    view = format_project_table(filtered)

    st.dataframe(view, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download Filtered Projects CSV",
        data=dataframe_to_csv_bytes(view),
        file_name="portfolio-projects.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.divider()

left, right = st.columns([1.2, 0.8])

with left:
    st.subheader("📈 Portfolio Score by Project")

    if not projects.empty:
        score_df = projects.copy()
        score_df["Portfolio Score"] = score_df.apply(project_score, axis=1)

        chart = (
            alt.Chart(score_df)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x=alt.X("Project:N", sort="-y"),
                y="Portfolio Score:Q",
                color="Category:N",
                tooltip=[
                    "Project",
                    "Category",
                    "Status",
                    "Portfolio Score",
                    "Progress",
                ],
            )
            .properties(height=380)
        )

        st.altair_chart(chart, use_container_width=True)

with right:
    st.subheader("🧠 AI-Style Project Advice")

    if projects.empty:
        st.info("Add your first project to get advice.")
    else:
        avg_progress = projects["Progress"].mean()
        incomplete = projects[~projects["Status"].eq("Completed")]
        high_priority = projects[projects["Priority"].eq("High")]

        if avg_progress < 50:
            st.warning("Many projects are still early. Finish 1 project fully before starting more.")
        elif len(high_priority) > 3:
            st.warning(
                "You have many high-priority projects. Reduce priority overload by choosing only 1–2 main projects this week."
            )
        elif not incomplete.empty:
            project_name = incomplete.sort_values("Progress", ascending=False).iloc[0]["Project"]
            st.info(f"Focus next on polishing **{project_name}** because it is close to completion.")
        else:
            st.success("Your project list looks strong. Add screenshots, changelog, roadmap, and releases next.")

st.divider()

with st.expander("🗑️ Delete Project"):
    if projects.empty:
        st.info("No projects available.")
    else:
        delete_project = st.selectbox(
            "Select project to delete",
            projects["Project"].tolist(),
        )

        if st.button("Delete Selected Project", type="primary"):
            st.session_state.projects_df = projects[
                projects["Project"] != delete_project
            ].reset_index(drop=True)

            st.success("Project deleted.")
            st.rerun()
