# SQLPilot — Antigravity & GSD Project Instructions

This repository contains **SQLPilot: An Agentic AI Data Analyst**.

## Authoritative Documentation

Before executing any plan or making significant architectural changes, always consult the primary specification documents:
- [PRD.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/PRD.md) — Product requirements, personas, modes, and success criteria.
- [architecture.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/architecture.md) — System architecture, LangGraph agent design, and flows.
- [rules.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/rules.md) — Engineering rules, SQL safety, and autonomy guardrails.
- [phase.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/phase.md) — 21-phase implementation plan and phase contract.
- [design.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/design.md) — Frontend & Streamlit UI design specifications.
- [memory.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/memory.md) — Persistent coding agent working memory.

## Golden Rules for Development

1. **Agentic does not mean unrestricted**: The agent dynamically decides what to investigate and which tool to call next, but is strictly constrained from destructive DB operations, OS execution, or secret exposure.
2. **Database is the source of truth**: The agent must never hallucinate tables, columns, joins, or results. If data is missing, report the limitation explicitly.
3. **No fixed pipeline disguised as an agent**: The system must run a dynamic loop: `Understand -> Inspect -> Query -> Observe -> Decide -> Investigate -> Verify -> Evidence -> Answer`.
4. **Read-only by default**: All database access goes through the SQL safety validation layer and read-only connections.
5. **No private CoT exposure**: User-facing UI displays high-level activity, SQL queries, and evidence cards—never internal model deliberation tokens.
6. **Follow GSD Phases**: Execute phases in strict order (0 through 20). Never implement future-phase capabilities prematurely.

## GSD Workflow Commands

- `/gsd-plan-phase [phase_number]` — Plan the active phase.
- `/gsd-execute-phase [phase_number]` — Execute the planned phase tasks.
- `/gsd-verify-work` — Verify phase deliverables against criteria.
- `/gsd-progress` — Check project state and status.
