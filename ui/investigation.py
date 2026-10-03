from __future__ import annotations

from typing import Any

import streamlit as st


def render_investigation_status(result: dict[str, Any] | None) -> None:
    if not result:
        return

    st.subheader("Investigation status")

    status_steps = [
        ("Understanding request", True),
        ("Inspecting schema", bool(result.get("database_context"))),
        ("Reviewing evidence", bool(result.get("evidence"))),
        ("Testing hypotheses", bool(result.get("hypotheses"))),
    ]

    for label, is_done in status_steps:
        if is_done:
            st.markdown(f"✅ {label}")
        else:
            st.markdown(f"● {label}")

    if result.get("analysis_summary"):
        st.caption(result["analysis_summary"])

    if result.get("hypotheses"):
        st.subheader("Candidate hypotheses")
        for idx, hypothesis in enumerate(result["hypotheses"], start=1):
            evaluation = hypothesis.get("evaluation", {})
            status = evaluation.get("status", "unknown")
            score = evaluation.get("support_score", 0)
            st.markdown(f"**{idx}. {hypothesis.get('name', 'Hypothesis')}**")
            st.write(hypothesis.get("description", ""))
            st.caption(f"Status: {status} | Support score: {score}")


def render_evidence_panel(result: dict[str, Any] | None) -> None:
    if not result:
        return

    evidence = result.get("evidence") or []
    if not evidence:
        return

    st.subheader("Evidence trail")
    for item in evidence:
        with st.expander(item.get("finding", "Evidence item")):
            st.write(item.get("purpose", ""))
            st.code(item.get("sql", ""), language="sql")
            st.json(item.get("result", []))
