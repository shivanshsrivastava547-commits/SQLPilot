from __future__ import annotations


def build_user_message(question: str) -> str:
    return (
        "You are SQLPilot, a cautious database analyst. "
        f"The user asks: {question}"
    )


def build_answer_prompt(question: str, sql: str, result: dict[str, object]) -> str:
    return (
        "Answer the user question using the query result and explain the evidence. "
        f"Question: {question}. SQL: {sql}. Result: {result}."
    )
