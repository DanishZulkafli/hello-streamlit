from __future__ import annotations

from datetime import date, timedelta

import altair as alt
import pandas as pd
import streamlit as st

from utils import TASK_COLUMNS, dataframe_to_csv_bytes, hero, seed_data, setup_page

setup_page("GitHub Contribution Planner", "✅")
seed_data()

hero(
    "GitHub Contribution Planner",
    "Plan real contributions without creating random repositories: issues, PRs, changelogs, screenshots, releases, documentation, and small feature improvements.",
    "Contribution Workflow Planner",
)

tasks = st.session_state.tasks_df
projects = st.session_state.projects_df

project_options = projects["Project"].tolist() if not projects.empty else ["General Portfolio"]

with st.expander("➕ Add Contribution Task", expanded=True):
    with st.form("task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            task = st.text_input(
                "Task",
                placeholder="Example: Add project screenshots to README",
            )

            project = st.selectbox("Project", project_options)

            task_type = st.selectbox(
                "Type",
                [
                    "Documentation",
                    "Frontend",
                    "Bug Fix",
                    "Feature",
                    "Maintenance",
                    "Testing",
                    "Release",
                    "Issue",
                    "Pull Request",
                ],
            )

        with col2:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            status = st.selectbox("Status", ["Todo", "In Progress", "Done"])
            due_date = st.date_input("Due Date", value=date.today() + timedelta(days=2))

        submitted = st.form_submit_button("Add Task", use_container_width=True)

    if submitted:
        if not task.strip():
            st.error("Task title is required.")
        else:
            row = pd.DataFrame(
                [[task, project, task_type, priority, status, due_date]],
                columns=TASK_COLUMNS,
            )

            st.session_state.tasks_df = pd.concat(
                [tasks, row],
                ignore_index=True,
            )

            st.success("Task added.")
            st.rerun()

st.subheader("📋 Contribution Task Board")

col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox(
        "Status",
        ["All"] + sorted(tasks["Status"].dropna().unique().tolist()),
    )

with col2:
    priority_filter = st.selectbox(
        "Priority",
        ["All"] + sorted(tasks["Priority"].dropna().unique().tolist()),
    )

with col3:
    type_filter = st.selectbox(
        "Type",
        ["All"] + sorted(tasks["Type"].dropna().unique().tolist()),
    )

filtered = tasks.copy()

if status_filter != "All":
    filtered = filtered[filtered["Status"] == status_filter]

if priority_filter != "All":
    filtered = filtered[filtered["Priority"] == priority_filter]

if type_filter != "All":
    filtered = filtered[filtered["Type"] == type_filter]

if filtered.empty:
    st.warning("No tasks match the selected filters.")
else:
    display = filtered.copy()
    display["Due Date"] = pd.to_datetime(display["Due Date"], errors="coerce").dt.date.astype(str)

    st.dataframe(display, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download Tasks CSV",
        data=dataframe_to_csv_bytes(display),
        file_name="github-contribution-tasks.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Task Status Breakdown")

    if tasks.empty:
        st.info("No task status data yet.")
    else:
        status_df = tasks["Status"].value_counts().reset_index()
        status_df.columns = ["Status", "Count"]

        chart = (
            alt.Chart(status_df)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x="Status:N",
                y="Count:Q",
                color="Status:N",
                tooltip=["Status", "Count"],
            )
            .properties(height=330)
        )

        st.altair_chart(chart, use_container_width=True)

with col_b:
    st.subheader("Task Type Breakdown")

    if tasks.empty:
        st.info("No task type data yet.")
    else:
        type_df = tasks["Type"].value_counts().reset_index()
        type_df.columns = ["Type", "Count"]

        chart = (
            alt.Chart(type_df)
            .mark_arc(innerRadius=60)
            .encode(
                theta="Count:Q",
                color="Type:N",
                tooltip=["Type", "Count"],
            )
            .properties(height=330)
        )

        st.altair_chart(chart, use_container_width=True)

st.subheader("🧠 AI-Style Contribution Recommendation")

if tasks.empty:
    st.info("Add tasks to receive contribution planning advice.")
else:
    today = date.today()
    due_dates = pd.to_datetime(tasks["Due Date"], errors="coerce").dt.date

    overdue = tasks[(due_dates < today) & ~tasks["Status"].eq("Done")]
    todo = tasks[tasks["Status"].eq("Todo")]
    done = tasks[tasks["Status"].eq("Done")]

    if not overdue.empty:
        st.error(f"You have {len(overdue)} overdue task(s). Complete or reschedule these first.")
    elif len(done) == 0:
        st.warning("No task is marked as done yet. Finish one small contribution today to keep your graph active.")
    elif len(todo) > len(done) * 2:
        st.warning("Your todo list is growing. Choose only 1–2 high-impact tasks before adding more.")
    else:
        st.success("Your contribution workflow looks healthy. Keep improving existing repos with useful maintenance work.")

st.markdown(
    """
    ### Useful contribution ideas

    <span class="pill">README screenshots</span>
    <span class="pill">CHANGELOG.md</span>
    <span class="pill">ROADMAP.md</span>
    <span class="pill">CONTRIBUTING.md</span>
    <span class="pill">GitHub Issues</span>
    <span class="pill">Pull Requests</span>
    <span class="pill">Bug fixes</span>
    <span class="pill">Accessibility labels</span>
    <span class="pill">Mobile UI polish</span>
    <span class="pill">Releases</span>
    """,
    unsafe_allow_html=True,
)

st.divider()

with st.expander("Update Task Status / Delete Task"):
    if tasks.empty:
        st.info("No tasks available.")
    else:
        selected_task = st.selectbox("Select task", tasks["Task"].tolist())
        new_status = st.selectbox("New status", ["Todo", "In Progress", "Done"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update Status", use_container_width=True):
                st.session_state.tasks_df.loc[
                    st.session_state.tasks_df["Task"] == selected_task,
                    "Status",
                ] = new_status

                st.success("Task updated.")
                st.rerun()

        with col2:
            if st.button("Delete Task", use_container_width=True, type="primary"):
                st.session_state.tasks_df = tasks[
                    tasks["Task"] != selected_task
                ].reset_index(drop=True)

                st.success("Task deleted.")
                st.rerun()
