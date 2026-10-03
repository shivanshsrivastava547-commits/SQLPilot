import streamlit as st

from agent.graph import run_agent
from analysis.explore import build_explore_findings
from analysis.monitoring import build_monitoring_report
from analysis.reliability import build_reliability_report
from analysis.resilience import normalize_result_payload
from config import settings
from database.connection import test_connection
from database.schema_inspector import inspect_database
from ui.clarification import render_clarification_prompt
from ui.findings import render_findings_panel
from ui.investigation import render_evidence_panel, render_investigation_status
from ui.monitoring import render_monitoring_panel
from ui.reliability import render_reliability_panel
from visualization.charts import build_chart


st.set_page_config(
    page_title="SQLPilot",
    page_icon="🧠",
    layout="wide",
)


def render_sidebar() -> None:
    with st.sidebar:
        st.title("SQLPilot")
        st.caption("AI Data Analyst")

        st.subheader("Database")
        db_url = st.text_input(
            "Connection URL",
            value=settings.database_url,
            type="password",
            help="Use a PostgreSQL URL such as postgresql://user:password@host:5432/dbname",
        )

        if st.button("Connect"):
            try:
                is_ok, message = test_connection(db_url)
                if is_ok:
                    st.session_state["db_connected"] = True
                    st.session_state["db_url"] = db_url
                    st.success("Connected")
                    st.caption(message)
                else:
                    st.session_state["db_connected"] = False
                    st.error(f"Connection failed: {message}")
            except Exception as exc:
                st.session_state["db_connected"] = False
                st.error(f"Unable to connect: {exc}")

        if st.session_state.get("db_connected"):
            st.info("PostgreSQL ready for analysis")
        else:
            st.warning("Database not connected")

        st.subheader("Workspace")
        st.write(f"Database: {settings.default_database}")
        st.write(f"Environment: {settings.app_environment}")

        st.subheader("Mode")
        mode = st.radio("Current mode", ["Ask", "Investigate", "Explore"], index=0, horizontal=True)
        st.caption(f"Selected: {mode}")
        st.session_state["selected_mode"] = mode

        st.subheader("Recent questions")
        st.markdown(
            "- Why did revenue fall?\n"
            "- Top products\n"
            "- Monthly sales"
        )


def render_main() -> None:
    st.header("Ask your database")

    col1, col2 = st.columns([3, 1])

    with col1:
        question = st.text_area(
            "Question",
            value="",
            height=180,
            placeholder="Why did revenue fall in September?",
        )

    with col2:
        st.subheader("Connection")
        st.info("PostgreSQL")
        if st.session_state.get("db_connected"):
            st.success("Connected")
        else:
            st.warning("Disconnected")
        st.write(f"Model: {settings.default_model}")

    if st.button("Analyze", type="primary"):
        if not question.strip():
            st.warning("Please enter a question to analyze.")
        else:
            if st.session_state.get("db_connected"):
                db_url = st.session_state.get("db_url") or settings.database_url
                selected_mode = st.session_state.get("selected_mode", "Ask")

                if selected_mode == "Explore":
                    with st.spinner("Scanning the schema for useful observations..."):
                        schema = inspect_database(db_url)
                        findings = build_explore_findings(schema)
                    result = {
                        "user_question": question,
                        "mode": "Explore",
                        "database_url": db_url,
                        "database_context": schema,
                        "messages": [{"role": "assistant", "content": "Explored the database for candidate findings."}],
                        "current_goal": question,
                        "clarification_required": False,
                        "clarification_question": None,
                        "clarification_options": [],
                        "last_tool": "explore",
                        "last_tool_result": {"status": "success", "findings": findings},
                        "investigation_history": ["explore"],
                        "hypotheses": [],
                        "evidence": findings,
                        "generated_sql": [],
                        "query_results": [],
                        "findings": [item["finding"] for item in findings],
                        "visualization_requests": [],
                        "final_answer": "\n\n".join(f"- {item['finding']}" for item in findings),
                        "is_complete": True,
                        "error": None,
                        "step_count": 1,
                        "next_action": "finish",
                        "analysis_summary": "Exploration surfaced a few candidate patterns from the database schema.",
                    }
                else:
                    with st.spinner("Inspecting schema and generating SQL..."):
                        result = run_agent(question, database_url=db_url, mode=selected_mode)

                st.session_state["agent_result"] = result
                if result.get("clarification_required"):
                    st.session_state["clarification_result"] = result
                else:
                    st.session_state.pop("clarification_result", None)

                if result.get("clarification_required"):
                    st.warning(result["clarification_question"])
                    clarification_answer = render_clarification_prompt(
                        result["clarification_question"],
                        result["clarification_options"],
                    )
                    if clarification_answer:
                        clarified_question = f"{question} (Interpretation: {clarification_answer})"
                        follow_up = run_agent(clarified_question, database_url=db_url, mode=selected_mode)
                        st.session_state["agent_result"] = follow_up
                        st.success("Clarification received. Continuing the investigation.")
                        st.markdown(follow_up.get("final_answer") or "The follow-up analysis is in progress.")
                    return

                st.success("Analysis complete")
                latest_query = result.get("generated_sql")[-1] if result.get("generated_sql") else None
                reliability_report = build_reliability_report(result.get("database_context"), latest_query)
                render_reliability_panel(reliability_report)

                last_tool_result = normalize_result_payload(result.get("last_tool_result"))
                result["last_tool_result"] = last_tool_result
                result_rows = last_tool_result.get("rows", [])
                if result_rows:
                    monitoring_report = build_monitoring_report(result_rows, schedule="weekly")
                    render_monitoring_panel(monitoring_report)

                render_findings_panel(result)
                render_investigation_status(result)
                render_evidence_panel(result)

                if result_rows:
                    chart = build_chart(result_rows)
                    if chart.get("data"):
                        st.subheader("Visualization")
                        st.plotly_chart(chart, use_container_width=True)
            else:
                st.warning("Please connect to a database before analyzing a question.")

    st.subheader("Investigation status")
    agent_result = st.session_state.get("agent_result")
    progress_value = 1.0 if agent_result else 0.0
    st.progress(progress_value, text="Waiting for database analysis" if not agent_result else "Analysis complete")

    status_cols = st.columns(3)
    with status_cols[0]:
        st.markdown("✅ Understanding request")
    with status_cols[1]:
        st.markdown("✅ Inspecting schema")
    with status_cols[2]:
        st.markdown("✅ Agent answer ready" if agent_result else "● Ready for next phase")


def main() -> None:
    if "db_connected" not in st.session_state:
        st.session_state["db_connected"] = False
    render_sidebar()
    render_main()


if __name__ == "__main__":
    main()
