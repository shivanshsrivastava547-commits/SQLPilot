# SQLPilot: An Agentic AI Data Analyst

## What This Is

SQLPilot is an autonomous AI data analyst that connects to a relational database (initially PostgreSQL), understands business questions in natural language, investigates data using safe SQL and deterministic analytical tools, resolves ambiguity through interaction, verifies findings, and presents evidence-backed answers and visualizations. The system is designed for business analysts, data teams, and technical stakeholders who need reliable, self-service exploratory analysis without writing manual SQL or relying on brittle, fixed Text-to-SQL pipelines.

## Core Value

The agent dynamically decides what information it needs, which tool to call, whether the result is sufficient, and what action to take next — behaving as an autonomous junior data analyst with an evidence trail, rather than a rigid Text-to-SQL pipeline.

## Business Context

- **Customer**: Business analysts, data analysts, and product/engineering teams seeking self-service, evidence-backed relational database analytics.
- **Value Model**: Accelerates exploratory analysis, eliminates repetitive query drafting, and provides verifiable analytical narratives with audit trails.
- **Success Metric**: Accuracy and transparency of analytical conclusions, 0 destructive queries executed, and high confidence in hypothesis-driven investigation.
- **Authoritative Docs**: [PRD.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/PRD.md), [architecture.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/architecture.md), [rules.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/rules.md), [phase.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/phase.md), [design.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/design.md), [memory.md](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/memory.md).

## Requirements

### Validated

(None yet — greenfield implementation starting from authoritative specs)

### Active

- [ ] **FOUND-01**: Clean Python project foundation with environment configuration, dependencies, and folder structure.
- [ ] **DB-01**: Reliable PostgreSQL connection layer using SQLAlchemy with read-only connection guarantees.
- [ ] **SCHEMA-01**: Deterministic database inspection tools (`inspect_database`, `inspect_table`, `inspect_relationships`) without LLM hallucination.
- [ ] **SAFE-01**: Robust SQL safety validation blocking all DDL/DML destructive statements (INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, etc.) and enforcing resource limits.
- [ ] **AGENT-01**: Stateful LangGraph agent architecture with dynamic decision node and conditional tool dispatch.
- [ ] **LOOP-01**: Dynamic investigation loop enabling multi-step observation, re-querying, and evidence accumulation.
- [ ] **CLAR-01**: Human-in-the-loop clarification system for ambiguity resolution with bounded rounds.
- [ ] **EVID-01**: Structured evidence trail linking every major conclusion to specific queries, results, and metric calculations.
- [ ] **HYPO-01**: Hypothesis formulation and testing engine for complex "why" questions (Investigate Mode).
- [ ] **UI-01**: Streamlit intelligence interface with vertical narrative layout, activity feed (without private CoT), findings cards, and SQL viewer.
- [ ] **VIZ-01**: Dynamic Plotly visualization tool mapping query results to appropriate charts (line, bar, scatter, etc.).
- [ ] **MODE-01**: Three distinct analytical modes: Ask Mode, Investigate Mode, and Explore Mode.
- [ ] **REL-01**: Comprehensive automated testing, structured error recovery, SQL repair loops, and production hardening.

### Out of Scope

- **Modifying Production Data**: No `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `GRANT`, `REVOKE` — SQLPilot is strictly read-only.
- **Exposing Private Chain-of-Thought**: Model deliberation tokens and internal prompt reasoning are never surfaced; only high-level activity steps, SQL, findings, and evidence are shown.
- **Fabricating Database Schema**: The agent must never invent tables, columns, relationships, or business facts; missing data must be explicitly reported as a limitation.
- **Arbitrary Code Execution**: No general-purpose Python, Bash, or OS execution tools exposed to the agent.
- **Multi-Tenant Cloud / Heterogeneous Non-Postgres DBs (v1)**: Initial MVP targets local/hosted PostgreSQL before expanding to Snowflake, BigQuery, or MySQL.
- **Autonomous Business Actions**: SQLPilot analyzes and reports; it does not automatically trigger operational workflows or external webhooks.

## Context

- The project has complete, authoritative specifications created by product and architecture teams:
  - `PRD.md`: Full product specifications, personas, capabilities, and success criteria.
  - `architecture.md`: LangGraph orchestration, tool architecture, state management, and data flows.
  - `rules.md`: Engineering guardrails, safety rules, query limits, and operational bounds.
  - `phase.md`: 21 implementation phases across 6 milestones.
  - `design.md`: Frontend UI requirements using Streamlit, Plotly, custom components, and restrained styling.
  - `memory.md`: Persistent working memory for coding sessions.
- Current repository state: Specification complete, git initialized, zero source code written. Active phase is Phase 0 (Project Foundation).

## Constraints

- **Orchestration**: LangGraph for stateful agent cycles, conditional routing, and human-in-the-loop pauses.
- **Database**: PostgreSQL accessed via SQLAlchemy engine with read-only session configuration.
- **Safety Enforcement**: Programmatic AST/keyword validation independent of LLM prompts before query execution.
- **Limits**: `MAX_AGENT_STEPS = 15`, `MAX_SQL_REPAIR_ATTEMPTS = 2`, `MAX_CLARIFICATION_ROUNDS = 3`, `MAX_QUERY_ROWS = 500`, `QUERY_TIMEOUT = 30s`.
- **Frontend**: Streamlit-based UI adhering to `design.md` standards (clean, analytical, non-chatbot look, no neon AI clichés).
- **Visualization**: Plotly charts rendered natively in Streamlit.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Dynamic LangGraph loop over fixed Text-to-SQL | Real business questions ("why did revenue fall?") require iterative exploration, hypothesis testing, and variable tool paths. | Pending |
| Read-only database connection + AST validator | Defense-in-depth: database level read-only user plus application-level statement inspection prevents data loss or corruption. | Pending |
| Deterministic schema tools without LLM guessing | LLMs hallucinate column names and joins; programmatic inspection ensures 100% schema grounding. | Pending |
| Separate high-level activity feed from private CoT | Users need clear, trustworthy visibility into what the agent is doing without being overwhelmed by raw model deliberation. | Pending |
| Streamlit + Plotly frontend | Fast development cycle with rich data visualization and interactive widgets tailored to analytics workflows. | Pending |

## Evolution

**After each phase transition:**
1. Requirements invalidated? Move to Out of Scope with reason.
2. Requirements validated? Move to Validated with phase reference.
3. New requirements emerged? Add to Active.
4. Decisions to log? Add to Key Decisions.
5. "What This Is" still accurate? Update if drifted.

---
*Last updated: 2026-10-02 after GSD initialization*
