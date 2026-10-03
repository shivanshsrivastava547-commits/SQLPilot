from __future__ import annotations

from typing import Any, TypedDict

MAX_AGENT_STEPS = 15
MAX_CONTEXT_MESSAGES = 6
MAX_CONTEXT_HYPOTHESES = 3
MAX_CONTEXT_EVIDENCE = 3


class AgentState(TypedDict):
    user_question: str
    mode: str
    database_url: str
    database_context: dict[str, Any]
    messages: list[dict[str, str]]
    current_goal: str
    clarification_required: bool
    clarification_question: str | None
    clarification_options: list[str]
    last_tool: str | None
    last_tool_result: dict[str, Any] | None
    investigation_history: list[str]
    hypotheses: list[dict[str, Any]]
    evidence: list[str]
    generated_sql: list[str]
    query_results: list[dict[str, Any]]
    findings: list[str]
    visualization_requests: list[str]
    final_answer: str | None
    is_complete: bool
    error: str | None
    step_count: int
    next_action: str | None
    analysis_summary: str | None


def compact_agent_state(
    state: dict[str, Any],
    *,
    max_messages: int = MAX_CONTEXT_MESSAGES,
    max_hypotheses: int = MAX_CONTEXT_HYPOTHESES,
    max_evidence: int = MAX_CONTEXT_EVIDENCE,
) -> dict[str, Any]:
    compacted = dict(state)
    compacted["messages"] = (state.get("messages") or [])[-max_messages:]
    compacted["hypotheses"] = (state.get("hypotheses") or [])[-max_hypotheses:]
    compacted["evidence"] = (state.get("evidence") or [])[-max_evidence:]
    compacted["findings"] = (state.get("findings") or [])[-max_evidence:]
    compacted["generated_sql"] = (state.get("generated_sql") or [])[-3:]
    return compacted
