from __future__ import annotations

from typing import Any

import streamlit as st


def render_reliability_panel(report: dict[str, Any] | None) -> None:
    if not report:
        return

    st.subheader("Reliability checks")
    if report.get("status") == "warning":
        st.warning("One or more checks raised a warning.")
    else:
        st.success("All core reliability checks are passing.")

    for key, value in report.get("checks", {}).items():
        label = key.replace("_", " ").title()
        if value:
            st.caption(f"✅ {label}")
        else:
            st.caption(f"⚠️ {label}")

    if report.get("issues"):
        for issue in report["issues"]:
            st.write(issue)
