from __future__ import annotations

from typing import Any

import streamlit as st


def render_monitoring_panel(report: dict[str, Any] | None) -> None:
    if not report:
        return

    status = report.get("status", "stable")
    title = report.get("schedule", "monitoring").title()
    st.subheader(f"{title} Monitoring")

    if status == "alert":
        st.warning(report.get("notification", "Alert: significant change detected."))
    elif status == "watch":
        st.info(report.get("notification", "Watch: trend needs attention."))
    else:
        st.success(report.get("notification", "Stable: no material change detected."))

    st.write(report.get("summary", "No monitoring summary was generated."))
    st.caption(f"Change: {report.get('change_pct', 0.0):.2f}%")
