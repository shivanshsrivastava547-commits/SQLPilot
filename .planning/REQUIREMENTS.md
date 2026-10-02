# Requirements: SQLPilot — Agentic AI Data Analyst

**Defined:** 2026-10-02  
**Core Value:** The agent dynamically decides what information it needs, which tool to call, whether the result is sufficient, and what action to take next — behaving as an autonomous junior data analyst with an evidence trail, rather than a rigid Text-to-SQL pipeline.

## v1 Requirements

Requirements for initial system release (Phases 0–13, achieving full Ask, Investigate, and Explore capabilities with core MVP at Phase 7/10).

### Foundation & Environment

- [ ] **FOUND-01**: Project directory structure exists matching architectural specification (`agent/`, `database/`, `tools/`, `analysis/`, `visualization/`, `models/`, `ui/`, `tests/`).
- [ ] **FOUND-02**: Dependencies defined in `requirements.txt` installing LangChain, LangGraph, SQLAlchemy, psycopg2-binary/asyncpg, Streamlit, Plotly, Pydantic, python-dotenv, pytest.
- [ ] **FOUND-03**: Environment configuration managed through `config.py` and `.env.example` with zero secrets committed.
- [ ] **FOUND-04**: Application entry point `app.py` launches a functional Streamlit shell.
- [ ] **FOUND-05**: Automated test runner configuration with `pytest` and basic test suite passes.

### Database Connection Layer

- [ ] **DB-01**: User can configure PostgreSQL database connection via environment variables or UI parameters.
- [ ] **DB-02**: System creates SQLAlchemy engine with connection pooling and timeouts.
- [ ] **DB-03**: System verifies read-only connection status and handles connectivity failures gracefully.
- [ ] **DB-04**: UI displays real-time connection status badge (Connected, Connecting, Disconnected, Error).

### Database Understanding & Schema Inspection

- [ ] **SCHEMA-01**: `inspect_database()` deterministically inspects and returns all tables, columns, and data types without LLM guessing.
- [ ] **SCHEMA-02**: `inspect_table(table_name)` returns detailed column metadata, nullable status, and primary key definitions.
- [ ] **SCHEMA-03**: `inspect_relationships()` returns foreign key relationships and cardinalities between tables.
- [ ] **SCHEMA-04**: Schema metadata is cached in session/agent context to prevent redundant database queries.

### SQL Generation & Safety Guardrails

- [ ] **SAFE-01**: `validate_sql(query)` programmatically blocks all DDL and write DML statements (INSERT, UPDATE, DELETE, MERGE, UPSERT, DROP, ALTER, TRUNCATE, CREATE, GRANT, REVOKE).
- [ ] **SAFE-02**: Only read-only queries (SELECT and read-only CTEs) are permitted for database execution.
- [ ] **SAFE-03**: `execute_query(sql)` enforces `MAX_QUERY_ROWS = 500` and `QUERY_TIMEOUT = 30s`.
- [ ] **SAFE-04**: Structured execution output returns column names, typed rows, row count, execution latency, and query status.
- [ ] **SAFE-05**: SQL execution errors return structured error types and database error messages allowing repair.
- [ ] **SAFE-06**: Query repair mechanism is bounded by `MAX_SQL_REPAIR_ATTEMPTS = 2` to prevent infinite repair loops.

### Agent Core & LangGraph Orchestration

- [ ] **AGENT-01**: Typed `AgentState` encapsulates user question, database context, message history, current plan, findings, evidence, and tool results.
- [ ] **AGENT-02**: LangGraph graph connects decision router, tool execution node, and output formatting node.
- [ ] **AGENT-03**: Decision node dynamically selects next tool based on current observation and state rather than a predetermined pipeline.
- [ ] **AGENT-04**: Maximum agent steps bounded by `MAX_AGENT_STEPS = 15` with graceful termination and uncertainty summary when reached.
- [ ] **AGENT-05**: Agent explicitly acknowledges missing database data without hallucinating tables, columns, or values.

### Dynamic Investigation Loop

- [ ] **LOOP-01**: Agent observes returned query results and determines whether evidence is sufficient to answer the user's question.
- [ ] **LOOP-02**: Agent formulates follow-up queries based on previous query observations (e.g. drilling down from overall revenue to category breakdown to order volume).
- [ ] **LOOP-03**: Agent maintains an investigation trail of intermediate observations and steps.

### Human-in-the-Loop Clarification

- [ ] **CLAR-01**: Agent identifies semantic ambiguity in user questions (e.g. "best customers", "high value") when schema does not define it uniquely.
- [ ] **CLAR-02**: `ask_clarification(question, options)` pauses graph execution and presents specific options to user.
- [ ] **CLAR-03**: User clarification response updates agent state and resumes investigation graph.
- [ ] **CLAR-04**: Clarification rounds are bounded by `MAX_CLARIFICATION_ROUNDS = 3`.

### Evidence System & Audit Trail

- [ ] **EVID-01**: Every major finding is stored as an evidence object containing finding statement, supporting query SQL, result snapshot, and metric calculation.
- [ ] **EVID-02**: Findings distinguish between observed facts, computed metrics, supported explanations, and unverified possibilities.
- [ ] **EVID-03**: UI allows users to expand and view the exact evidence trail and underlying queries for any finding.
- [ ] **EVID-04**: Correlational findings are explicitly framed without unsupported claims of definitive causation.

### Hypothesis Testing Engine

- [ ] **HYPO-01**: For complex "why" questions, agent formulates candidate hypotheses (e.g., volume drop vs. basket size decrease vs. category shift).
- [ ] **HYPO-02**: Agent executes targeted queries to test each hypothesis against real database evidence.
- [ ] **HYPO-03**: Hypotheses are classified with statuses (`supported`, `weak`, `rejected`, `unknown`) based on query results.
- [ ] **HYPO-04**: Final conclusion summarizes supported hypotheses and dismisses refuted ones with supporting metrics.

### Streamlit Intelligence UI

- [ ] **UI-01**: UI implements persistent layout with sidebar (database status, mode selection, settings) and main analytical workspace.
- [ ] **UI-02**: Query input provides a spacious, comfortable natural language text area with prompt guidance and sample questions.
- [ ] **UI-03**: Activity feed displays high-level agent actions (completed, active, pending) without exposing private chain-of-thought tokens.
- [ ] **UI-04**: Findings panel renders clean finding cards with headline metric, percentage comparisons, and semantic direction indicators (↑, ↓, →).
- [ ] **UI-05**: Expandable SQL viewer displays formatted SQL queries used during analysis.
- [ ] **UI-06**: Clarification UI renders interactive multiple-choice selection or custom input when agent requests user guidance.
- [ ] **UI-07**: Visual styling adheres to `design.md` standards (clean, restrained, analytical, dark/light theme harmony, no gimmick animations).

### Visualization & Charts

- [ ] **VIZ-01**: Visualization module generates interactive Plotly charts based on query results.
- [ ] **VIZ-02**: Automatic chart selection maps time series to line charts, categorical comparisons to bar charts, and distributions to histograms/scatter plots.
- [ ] **VIZ-03**: Charts include clear titles, labeled axes, human-readable units, and formatted tooltips.
- [ ] **VIZ-04**: Charts are displayed seamlessly alongside findings and evidence cards.

### Analytical Modes

- [ ] **MODE-01**: **Ask Mode** optimized for fast, single-turn direct queries with result table, generated SQL, and optional chart.
- [ ] **MODE-02**: **Investigate Mode** coordinates multi-step hypothesis testing, evidence gathering, and comprehensive analytical reports.
- [ ] **MODE-03**: **Explore Mode** autonomously discovers interesting trends, anomalies, or distributions in connected database without requiring a specific question.

## v2 Requirements (Post-MVP & Future Releases)

Deferred to future releases (Phases 14–20).

### Advanced Intelligence & Resilience

- **REL-01**: End-to-end integration and regression test suite covering normal and failure paths.
- **REL-02**: Resilience against database timeouts, network disconnects, and provider rate limits.
- **REL-03**: Production hardening: prompt injection defense, credential isolation, and sensitive data masking.
- **REL-04**: Latency and token optimization via schema caching and pruned agent state.
- **ADV-01**: Automated data quality profiling and anomaly detection across database tables.
- **ADV-02**: Proactive weekly insights and change detection alerts.
- **ADV-03**: Scheduled monitoring jobs running recurrent background investigations.
- **ADV-04**: Support for additional database engines (MySQL, Snowflake, BigQuery, SQLite).

## Out of Scope

| Feature | Reason |
|---------|--------|
| Database modification (INSERT/UPDATE/DELETE/DDL) | SQLPilot is strictly read-only to protect production database integrity. |
| Private Chain-of-Thought exposure | Violates transparency principle; exposes raw tokens instead of structured findings and evidence. |
| Schema hallucination / fallback guessing | Database is the sole source of truth; missing information must be declared as a limitation. |
| Arbitrary Python / Shell code execution | Security vulnerability; agent is restricted to structured, typed tools. |
| Generic chat assistant conversation | SQLPilot is an AI data analyst, not a general-purpose chat LLM. |
| Multi-tenant user auth & billing in v1 | Focused on single-tenant / local workspace analytics first. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 | Phase 0 | Pending |
| FOUND-02 | Phase 0 | Pending |
| FOUND-03 | Phase 0 | Pending |
| FOUND-04 | Phase 0 | Pending |
| FOUND-05 | Phase 0 | Pending |
| DB-01 | Phase 1 | Pending |
| DB-02 | Phase 1 | Pending |
| DB-03 | Phase 1 | Pending |
| DB-04 | Phase 1 | Pending |
| SCHEMA-01 | Phase 2 | Pending |
| SCHEMA-02 | Phase 2 | Pending |
| SCHEMA-03 | Phase 2 | Pending |
| SCHEMA-04 | Phase 2 | Pending |
| SAFE-01 | Phase 3 | Pending |
| SAFE-02 | Phase 3 | Pending |
| SAFE-03 | Phase 3 | Pending |
| SAFE-04 | Phase 3 | Pending |
| SAFE-05 | Phase 3 | Pending |
| SAFE-06 | Phase 3 | Pending |
| AGENT-01 | Phase 4 | Pending |
| AGENT-02 | Phase 4 | Pending |
| AGENT-03 | Phase 4 | Pending |
| AGENT-04 | Phase 4 | Pending |
| AGENT-05 | Phase 4 | Pending |
| LOOP-01 | Phase 5 | Pending |
| LOOP-02 | Phase 5 | Pending |
| LOOP-03 | Phase 5 | Pending |
| CLAR-01 | Phase 6 | Pending |
| CLAR-02 | Phase 6 | Pending |
| CLAR-03 | Phase 6 | Pending |
| CLAR-04 | Phase 6 | Pending |
| EVID-01 | Phase 7 | Pending |
| EVID-02 | Phase 7 | Pending |
| EVID-03 | Phase 7 | Pending |
| EVID-04 | Phase 7 | Pending |
| HYPO-01 | Phase 8 | Pending |
| HYPO-02 | Phase 8 | Pending |
| HYPO-03 | Phase 8 | Pending |
| HYPO-04 | Phase 8 | Pending |
| UI-01 | Phase 9 | Pending |
| UI-02 | Phase 9 | Pending |
| UI-03 | Phase 9 | Pending |
| UI-04 | Phase 9 | Pending |
| UI-05 | Phase 9 | Pending |
| UI-06 | Phase 9 | Pending |
| UI-07 | Phase 9 | Pending |
| VIZ-01 | Phase 10 | Pending |
| VIZ-02 | Phase 10 | Pending |
| VIZ-03 | Phase 10 | Pending |
| VIZ-04 | Phase 10 | Pending |
| MODE-01 | Phase 11 | Pending |
| MODE-02 | Phase 12 | Pending |
| MODE-03 | Phase 13 | Pending |

**Coverage:**
- v1 requirements: 50 total
- Mapped to phases: 50
- Unmapped: 0

---
*Requirements defined: 2026-10-02*  
*Last updated: 2026-10-02 after initial definition*
