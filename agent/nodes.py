from __future__ import annotations

from typing import Any

from analysis.evidence import create_evidence_entry
from analysis.hypothesis import build_hypotheses, evaluate_hypothesis
from analysis.result_analyzer import analyze_query_result
from database.executor import execute_query
from database.schema_inspector import inspect_database
from tools.query_tools import generate_query

from agent.state import AgentState


def inspect_database_node(state: AgentState) -> AgentState:
    database_url = state["database_url"]
    context = inspect_database(database_url)
    state["database_context"] = context
    state["messages"] = [{"role": "assistant", "content": "Inspected the connected database schema."}]
    state["investigation_history"] = ["inspect_database"]
    state["last_tool"] = "inspect_database"
    state["last_tool_result"] = {"status": "success", "tables": len(context.get("tables", []))}
    state["step_count"] = int(state.get("step_count", 0)) + 1
    return state


def generate_sql_node(state: AgentState) -> AgentState:
    question = state["user_question"]
    schema = state["database_context"]
    query = generate_query(question, schema)
    state["generated_sql"] = [query]
    state["messages"].append({"role": "assistant", "content": f"Generated SQL for the question: {query}"})
    state["investigation_history"].append("generate_sql")
    state["last_tool"] = "generate_sql"
    state["last_tool_result"] = {"status": "success", "query": query}
    state["step_count"] = int(state.get("step_count", 0)) + 1
    return state


def execute_sql_node(state: AgentState) -> AgentState:
    query = state["generated_sql"][-1]
    result = execute_query(query, database_url=state["database_url"])
    state["query_results"] = [result]
    state["last_tool"] = "execute_sql"
    state["last_tool_result"] = result
    state["messages"].append({"role": "assistant", "content": f"Executed query with status: {result.get('status', 'unknown')}"})
    state["investigation_history"].append("execute_sql")
    state["step_count"] = int(state.get("step_count", 0)) + 1
    return state


def analyze_result_node(state: AgentState) -> AgentState:
    result = state.get("last_tool_result") or {}
    rows = result.get("rows", [])
    findings = []
    evidence = []
    if rows:
        findings.append(f"The query returned {len(rows)} rows of evidence.")
        metric_key = next((key for key in rows[0].keys() if key.lower() in {"revenue", "sales", "total", "count", "amount"}), None)
        analysis = analyze_query_result(rows, metric_key)
        state["analysis_summary"] = analysis["summary"]
        sql = state.get("generated_sql", [])[-1] if state.get("generated_sql") else ""
        evidence_entry = create_evidence_entry(
            finding=analysis["summary"],
            query_id=f"query_{len(state.get('generated_sql', []))}",
            sql=sql,
            result=rows,
            purpose="Trend analysis",
        )
        evidence.append(evidence_entry)
        hypothesis_candidates = build_hypotheses(state["user_question"], rows)
        evaluated_hypotheses = [
            {
                **candidate,
                "evaluation": evaluate_hypothesis(candidate, rows),
            }
            for candidate in hypothesis_candidates
        ]
        state["hypotheses"] = evaluated_hypotheses
    else:
        findings.append("The query returned no rows, so more investigation may be needed.")
        state["analysis_summary"] = "The query returned no evidence, so additional investigation is required."
        state["hypotheses"] = []

    if any(token in state["user_question"].lower() for token in ["why", "decrease", "decline", "drop", "fall"]):
        state["next_action"] = "continue_investigation" if len(state.get("generated_sql", [])) < 2 else "finish"
        if not rows:
            state["analysis_summary"] = "The first query supplied partial evidence; a follow-up query is needed to explain the decline."
    else:
        state["next_action"] = "finish"
        state["analysis_summary"] = state["analysis_summary"] or "The initial query returned enough evidence to answer the question."

    state["evidence"] = evidence
    state["findings"] = findings
    state["investigation_history"].append("analyze_result")
    state["last_tool"] = "analyze_result"
    state["step_count"] = int(state.get("step_count", 0)) + 1
    return state


def continue_investigation_node(state: AgentState) -> AgentState:
    question = state["user_question"].lower()
    if any(token in question for token in ["why", "decrease", "decline", "drop", "fall"]):
        follow_up_sql = "SELECT name, revenue FROM products ORDER BY revenue DESC LIMIT 5"
    else:
        follow_up_sql = "SELECT name, revenue FROM products ORDER BY revenue DESC LIMIT 5"

    existing_queries = state.get("generated_sql") or []
    existing_queries.append(follow_up_sql)
    state["generated_sql"] = existing_queries
    state["investigation_history"].append("continue_investigation")
    state["analysis_summary"] = "The agent continued the investigation with a follow-up revenue check to confirm the likely explanation."
    state["last_tool"] = "continue_investigation"
    state["last_tool_result"] = {"status": "success", "query": follow_up_sql}
    state["step_count"] = int(state.get("step_count", 0)) + 1
    return state


def finish_node(state: AgentState) -> AgentState:
    result = state.get("last_tool_result") or {}
    question = state["user_question"]
    sql = state["generated_sql"][-1] if state.get("generated_sql") else ""

    if result.get("status") == "error":
        state["final_answer"] = (
            "I could not answer that question because the database query failed. "
            f"The system reported: {result.get('message', 'Unknown error')}."
        )
        state["is_complete"] = True
        state["error"] = result.get("message")
        state["last_tool"] = "finish"
        state["step_count"] = int(state.get("step_count", 0)) + 1
        return state

    rows = result.get("rows", [])
    if not rows:
        state["final_answer"] = (
            f"I inspected the database for: '{question}' and ran the query. "
            "The result set was empty, so there is no evidence in the connected database for that request."
        )
        state["is_complete"] = True
        state["last_tool"] = "finish"
        state["step_count"] = int(state.get("step_count", 0)) + 1
        return state

    columns = result.get("columns", []) or list(rows[0].keys())
    preview = rows[:5]
    formatted_rows = []
    for row in preview:
        values = []
        for key in columns:
            values.append(f"{key}={row.get(key)}")
        formatted_rows.append("{" + ", ".join(values) + "}")

    evidence_summary = ""
    if state.get("evidence"):
        evidence_summary = " Evidence: " + "; ".join(item["finding"] for item in state["evidence"][:2])

    state["final_answer"] = (
        f"I inspected the schema, generated SQL, and executed it to answer: '{question}'. "
        f"SQL: {sql}. Result rows: {'; '.join(formatted_rows)}{evidence_summary}"
    )
    state["is_complete"] = True
    state["last_tool"] = "answer"
    state["step_count"] = int(state.get("step_count", 0)) + 1
    return state
