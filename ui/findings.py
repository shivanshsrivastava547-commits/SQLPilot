from __future__ import annotations

from typing import Any

import streamlit as st


def render_findings_panel(result: dict[str, Any] | None) -> None:
    if not result:
        return

    st.subheader("Findings")
    final_answer = result.get("final_answer")
    if final_answer:
        st.markdown(final_answer)

    if result.get("generated_sql"):
        with st.expander("Generated SQL"):
            st.code(result["generated_sql"][-1], language="sql")

    if result.get("last_tool_result"):
        with st.expander("Query result"):
            st.json(result["last_tool_result"])
