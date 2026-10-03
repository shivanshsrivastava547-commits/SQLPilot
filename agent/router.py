from __future__ import annotations

from agent.state import AgentState


def choose_next_step(state: AgentState) -> str:
    question = (state.get("user_question") or "").lower()
    last_tool = state.get("last_tool")
    last_result = state.get("last_tool_result") or {}
    generated_sql = state.get("generated_sql") or []

    if not state.get("database_context"):
        return "inspect_database"
    if not generated_sql:
        return "generate_sql"
    if last_result.get("status") == "error":
        return "finish"
    if last_tool == "continue_investigation":
        return "execute_sql"
    if last_tool == "analyze_result":
        if any(token in question for token in ["why", "decrease", "decline", "drop", "fall"]):
            if len(generated_sql) < 2:
                return "continue_investigation"
        return "finish"
    return "execute_sql"
