import json

import streamlit as st

from modules.ai_prd_generator import generate_prd, PRDGenerationError
from modules.prd_evaluator import evaluate_prd
from modules.schemas import PRDDocument


def build_prd_markdown(data):
    lines = [
        f"# {data.get('product_name', 'Product Requirements Document')}",
        "",
        "## Executive Summary",
        data.get("executive_summary", ""),
        "",
        "## Problem Statement",
        data.get("problem_statement", ""),
    ]

    for heading, key in [
        ("Target Users", "target_users"),
        ("Product Goals", "product_goals"),
        ("Non-Goals", "non_goals"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in data.get(key, []))

    lines.extend(["", "## User Stories"])

    for story in data.get("user_stories", []):
        lines.extend([
            "",
            f"### {story.get('story_id', 'User Story')}",
            story.get("story", ""),
            f"**Priority:** {story.get('priority', 'Not specified')}",
            "",
            "**Acceptance Criteria:**",
        ])
        lines.extend(
            f"- {item}" for item in story.get("acceptance_criteria", [])
        )

    lines.extend(["", "## Acceptance Criteria"])
    lines.extend(
        f"- {item}" for item in data.get("acceptance_criteria", [])
    )

    lines.extend(["", "## Success Metrics"])

    for metric in data.get("success_metrics", []):
        lines.extend([
            "",
            f"### {metric.get('metric_name', 'Metric')}",
            metric.get("definition", ""),
            f"**Measurement:** {metric.get('measurement_method', '')}",
            f"**Proposed Target:** {metric.get('proposed_target') or 'Baseline required'}",
            f"**Target Rationale:** {metric.get('target_rationale', '')}",
        ])

    for heading, key in [
        ("Assumptions", "assumptions"),
        ("Open Questions", "open_questions"),
        ("Risks and Mitigations", "risks_and_mitigations"),
    ]:
        lines.extend(["", f"## {heading}"])
        lines.extend(f"- {item}" for item in data.get(key, []))

    lines.extend([
        "",
        "---",
        "*AI-generated draft. Validate requirements with stakeholders before implementation.*",
    ])

    return "\n".join(lines)


def render_prd_workspace(navigate, surface, text, primary):
    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">PRODUCT REQUIREMENTS WORKSPACE</div>
            <div class="hero-title">Your PRD workspace.</div>
            <div class="hero-description">
                Generate, review and refine structured product requirements
                using AI assistance and human judgement.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.session_state.setdefault("generated_prd", None)
    st.session_state.setdefault("reviewed_prd_markdown", "")

    if not st.session_state.workspace_created:
        st.info("Your workspace is empty. Start by entering a product idea.")

        if st.button("Create your first PRD →", type="primary"):
            navigate("Create PRD")
            st.rerun()

        return

    st.subheader(st.session_state.product_name)
    st.caption("PRODUCT CONTEXT · SAVED IN THIS SESSION")

    with st.container(border=True):
        st.markdown("**Product idea**")
        st.write(st.session_state.product_idea)

        st.markdown("**Target users**")
        st.write(st.session_state.target_users or "Not specified yet.")

        st.markdown("**Problem**")
        st.write(st.session_state.problem or "Not specified yet.")

        st.markdown("**Proposed solution**")
        st.write(st.session_state.solution or "Not specified yet.")

    st.divider()
    st.subheader("AI PRD generation")

    st.write(
        "Generate a structured first draft from your saved product context. "
        "Missing information will be identified as assumptions or open questions."
    )

    if st.button(
        "Generate PRD with AI →",
        type="primary",
        use_container_width=True,
    ):
        try:
            with st.spinner("Generating your structured PRD..."):
                prd = generate_prd(
                    product_name=st.session_state.product_name,
                    idea=st.session_state.product_idea,
                    target_users=st.session_state.target_users,
                    problem=st.session_state.problem,
                    solution=st.session_state.solution,
                )

                data = prd.model_dump()

                st.session_state.generated_prd = data
                st.session_state.reviewed_prd_markdown = (
                    build_prd_markdown(data)
                )

            st.success("Your PRD has been generated successfully.")

        except ValueError as exc:
            st.error(f"Please check your product information: {exc}")

        except PRDGenerationError as exc:
            st.error(f"PRD generation could not be completed: {exc}")

        except Exception as exc:
            st.error(f"Unexpected error: {exc}")

    data = st.session_state.generated_prd

    if data is not None:
        st.divider()
        st.subheader("Generated PRD")
        st.caption("AI-GENERATED DRAFT · READY FOR HUMAN REVIEW")

        st.warning(
            "Review this draft before using it. Validate assumptions, "
            "open questions and proposed requirements with stakeholders."
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("User Stories", len(data.get("user_stories", [])))
        col2.metric("Success Metrics", len(data.get("success_metrics", [])))
        col3.metric("Open Questions", len(data.get("open_questions", [])))

        st.divider()
        st.subheader("PRD quality evaluation")
        st.caption("Rule-based quality checks. This score is a review aid, not a measure of factual accuracy.")
        evaluation = evaluate_prd(PRDDocument.model_validate(data))
        score_col, method_col = st.columns([1, 2])
        score_col.metric("Heuristic quality score", f"{evaluation["overall_score"]}/{evaluation["maximum_score"]}")
        method_col.write(f"Method: {evaluation["evaluation_type"]}")
        for dimension in evaluation["dimensions"]:
            st.write(f"**{dimension["name"]}** — {dimension["score"]}/{dimension["maximum"]}")
            st.progress(dimension["score"] / dimension["maximum"])
        if evaluation["strengths"]:
            with st.expander("Evaluation strengths"):
                for item in evaluation["strengths"]:
                    st.markdown(f"- {item}")
        if evaluation["warnings"]:
            with st.expander(f"Items to review ({len(evaluation["warnings"])})", expanded=True):
                for item in evaluation["warnings"]:
                    st.markdown(f"- {item}")
        else:
            st.success("No rule-based review warnings were identified.")
        with st.expander("Evaluation limitations"):
            st.write(evaluation["limitations"])

        with st.expander("Executive summary and problem statement", expanded=True):
            st.markdown("**Executive Summary**")
            st.write(data.get("executive_summary", "Not provided."))

            st.markdown("**Problem Statement**")
            st.write(data.get("problem_statement", "Not provided."))

        with st.expander("Target users, goals and non-goals"):
            for heading, key in [
                ("Target Users", "target_users"),
                ("Product Goals", "product_goals"),
                ("Non-Goals", "non_goals"),
            ]:
                st.markdown(f"**{heading}**")
                for item in data.get(key, []):
                    st.markdown(f"- {item}")

        with st.expander("User stories and acceptance criteria"):
            for story in data.get("user_stories", []):
                st.markdown(f"**{story.get('story_id', 'User Story')}**")
                st.write(story.get("story", ""))
                st.caption(
                    f"Proposed priority: {story.get('priority', 'Not specified')}"
                )

                for criterion in story.get("acceptance_criteria", []):
                    st.markdown(f"- {criterion}")

                st.divider()

        with st.expander("Success metrics"):
            for metric in data.get("success_metrics", []):
                st.markdown(f"**{metric.get('metric_name', 'Metric')}**")
                st.write(metric.get("definition", ""))
                st.write(f"Measurement: {metric.get('measurement_method', '')}")
                st.write(
                    f"Proposed target: {metric.get('proposed_target') or 'Baseline required'}"
                )
                st.write(f"Rationale: {metric.get('target_rationale', '')}")
                st.divider()

        for heading, key in [
            ("Assumptions", "assumptions"),
            ("Open Questions", "open_questions"),
            ("Risks and Mitigations", "risks_and_mitigations"),
        ]:
            with st.expander(heading):
                for item in data.get(key, []):
                    st.markdown(f"- {item}")

        st.divider()
        st.subheader("Review and edit your PRD")

        st.text_area(
            "PRD document editor",
            key="reviewed_prd_markdown",
            height=550,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "Download reviewed PRD (.md)",
                data=st.session_state.reviewed_prd_markdown,
                file_name="product_requirements_document.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with col2:
            st.download_button(
                "Download structured PRD (.json)",
                data=json.dumps(data, indent=2, ensure_ascii=False),
                file_name="product_requirements_document.json",
                mime="application/json",
                use_container_width=True,
            )

        st.caption(
            "Markdown includes your edits. JSON preserves the original "
            "structured AI response."
        )

    st.divider()

    if st.button("Edit product context"):
        navigate("Create PRD")
        st.rerun()
