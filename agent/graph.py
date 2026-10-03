from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from agent.nodes import (
    analyze_result_node,
    continue_investigation_node,
    execute_sql_node,
    finish_node,
    generate_sql_node,
    inspect_database_node,
)
from agent.router import choose_next_step
from agent.state import AgentState, MAX_AGENT_STEPS, compact_agent_state
from tools.clarification_tools import detect_clarification_need


def create_agent_graph() -> Any:
    workflow = StateGraph(AgentState)
    workflow.add_node("inspect_database", inspect_database_node)
    workflow.add_node("generate_sql", generate_sql_node)
    workflow.add_node("execute_sql", execute_sql_node)
    workflow.add_node("analyze_result", analyze_result_node)
    workflow.add_node("continue_investigation", continue_investigation_node)
    workflow.add_node("finish", finish_node)

    workflow.add_edge(START, "inspect_database")
    workflow.add_edge("inspect_database", "generate_sql")
    workflow.add_edge("generate_sql", "execute_sql")
    workflow.add_edge("execute_sql", "analyze_result")
    workflow.add_conditional_edges(
        "analyze_result",
        choose_next_step,
        {
            "continue_investigation": "continue_investigation",
            "finish": "finish",
            "execute_sql": "execute_sql",
        },
    )
    workflow.add_edge("continue_investigation", "execute_sql")
    workflow.add_edge("finish", END)

    return workflow.compile()


def run_agent(
    question: str,
    database_url: str | None = None,
    graph: Any | None = None,
    mode: str = "Ask",
) -> dict[str, Any]:
    if not question or not question.strip():
        raise ValueError("A user question is required.")

    normalized_mode = mode or "Ask"
    clarification = detect_clarification_need(question)
    if clarification is not None:
        return {
            "user_question": question.strip(),
            "mode": normalized_mode,
            "database_url": database_url or "",
            "database_context": {},
            "messages": [{"role": "assistant", "content": clarification["question"]}],
            "current_goal": question.strip(),
            "clarification_required": True,
            "clarification_question": clarification["question"],
            "clarification_options": clarification["options"],
            "last_tool": "clarification",
            "last_tool_result": {"status": "needs_clarification"},
            "investigation_history": ["clarification"],
            "hypotheses": [],
            "evidence": [],
            "generated_sql": [],
            "query_results": [],
            "findings": [],
            "visualization_requests": [],
            "final_answer": None,
            "is_complete": False,
            "error": None,
            "step_count": 1,
            "next_action": "clarify",
            "analysis_summary": None,
        }

    initial_state: AgentState = {
        "user_question": question.strip(),
        "mode": normalized_mode,
        "database_url": database_url or "",
        "database_context": {},
        "messages": [],
        "current_goal": question.strip(),
        "clarification_required": False,
        "clarification_question": None,
        "clarification_options": [],
        "last_tool": None,
        "last_tool_result": None,
        "investigation_history": [],
        "hypotheses": [],
        "evidence": [],
        "generated_sql": [],
        "query_results": [],
        "findings": [],
        "visualization_requests": [],
        "final_answer": None,
        "is_complete": False,
        "error": None,
        "step_count": 0,
        "next_action": None,
        "analysis_summary": None,
    }

    if graph is None:
        graph = create_agent_graph()

    result = graph.invoke(initial_state)
    result = compact_agent_state(result)
    result["step_count"] = int(result.get("step_count", 0))
    if result["step_count"] > MAX_AGENT_STEPS:
        result["final_answer"] = (
            "The agent reached its maximum investigation budget before a definitive answer could be reached. "
            "Please narrow the question or provide more context."
        )
        result["is_complete"] = True
    return result
