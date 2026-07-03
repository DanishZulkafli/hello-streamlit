from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from utils import SKILL_COLUMNS, dataframe_to_csv_bytes, hero, seed_data, setup_page

setup_page("Skill Roadmap", "🧭")
seed_data()

hero(
    "Skill Roadmap",
    "Track current skill levels, target levels, weekly learning hours, and AI-style recommendations for your developer growth plan.",
    "Developer Skills Dashboard",
)

skills = st.session_state.skills_df

with st.expander("➕ Add Skill", expanded=True):
    with st.form("skill_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            skill = st.text_input("Skill", placeholder="Example: FastAPI")

            category = st.selectbox(
                "Category",
                [
                    "Programming",
                    "Frontend",
                    "Backend",
                    "Data App",
                    "Artificial Intelligence",
                    "Deployment",
                    "Database",
                    "Design",
                ],
            )

            status = st.selectbox(
                "Status",
                ["Learning", "Improving", "Strong", "Need Practice"],
            )

        with col2:
            current = st.slider("Current Level", 1, 10, 5)
            target = st.slider("Target Level", 1, 10, 8)
            confidence = st.slider("Confidence", 0, 100, 60)
            hours = st.number_input(
                "Weekly Learning Hours",
                min_value=0.0,
                value=3.0,
                step=0.5,
            )

        submitted = st.form_submit_button("Add Skill", use_container_width=True)

    if submitted:
        if not skill.strip():
            st.error("Skill name is required.")
        else:
            row = pd.DataFrame(
                [[skill, category, current, target, confidence, hours, status]],
                columns=SKILL_COLUMNS,
            )

            st.session_state.skills_df = pd.concat(
                [skills, row],
                ignore_index=True,
            )

            st.success("Skill added successfully.")
            st.rerun()

st.subheader("📊 Skill Gap Analysis")

if skills.empty:
    st.info("No skills added yet.")
else:
    skill_view = skills.copy()
    skill_view["Gap"] = skill_view["Target Level"] - skill_view["Current Level"]
    skill_view["Weekly Focus Score"] = skill_view["Gap"] * skill_view["Weekly Hours"]

    st.dataframe(skill_view, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download Skills CSV",
        data=dataframe_to_csv_bytes(skill_view),
        file_name="developer-skills-roadmap.csv",
        mime="text/csv",
        use_container_width=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Current vs Target Level")

        long_df = skill_view.melt(
            id_vars=["Skill", "Category"],
            value_vars=["Current Level", "Target Level"],
            var_name="Type",
            value_name="Level",
        )

        chart = (
            alt.Chart(long_df)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x="Skill:N",
                y="Level:Q",
                color="Type:N",
                tooltip=["Skill", "Type", "Level"],
            )
            .properties(height=360)
        )

        st.altair_chart(chart, use_container_width=True)

    with col2:
        st.subheader("Recommended Weekly Focus")

        focus_df = skill_view.sort_values("Weekly Focus Score", ascending=False).head(6)

        chart = (
            alt.Chart(focus_df)
            .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
            .encode(
                y=alt.Y("Skill:N", sort="-x"),
                x="Weekly Focus Score:Q",
                color="Category:N",
                tooltip=[
                    "Skill",
                    "Gap",
                    "Weekly Hours",
                    "Weekly Focus Score",
                ],
            )
            .properties(height=360)
        )

        st.altair_chart(chart, use_container_width=True)

    st.subheader("🧠 AI-Style Learning Recommendation")

    biggest_gap = skill_view.sort_values("Gap", ascending=False).iloc[0]
    low_conf = skill_view.sort_values("Confidence", ascending=True).iloc[0]
    total_hours = skill_view["Weekly Hours"].sum()

    if total_hours < 5:
        st.warning("Your weekly learning hours are quite low. Try to reserve at least 5 focused hours per week.")
    elif biggest_gap["Gap"] >= 3:
        st.info(f"Focus on **{biggest_gap['Skill']}** because the gap between current and target level is high.")
    elif low_conf["Confidence"] < 50:
        st.info(f"Practice **{low_conf['Skill']}** with one small GitHub project because confidence is still low.")
    else:
        st.success("Your skill roadmap looks balanced. Maintain consistency and connect each skill to visible projects.")

st.divider()

with st.expander("🗑️ Delete Skill"):
    if skills.empty:
        st.info("No skills available.")
    else:
        delete_skill = st.selectbox(
            "Select skill to delete",
            skills["Skill"].tolist(),
        )

        if st.button("Delete Selected Skill", type="primary"):
            st.session_state.skills_df = skills[
                skills["Skill"] != delete_skill
            ].reset_index(drop=True)

            st.success("Skill deleted.")
            st.rerun()
