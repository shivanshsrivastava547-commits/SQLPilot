from __future__ import annotations

import streamlit as st


def render_clarification_prompt(question: str, options: list[str]) -> str | None:
    st.warning(question)
    selected = st.radio("Choose the definition that best matches your intent", options, index=0, horizontal=False)
    if st.button("Continue with this definition", type="primary"):
        return selected
    return None
