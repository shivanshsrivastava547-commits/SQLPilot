# Roadmap: SQLPilot — Agentic AI Data Analyst

## Overview

SQLPilot is constructed systematically across 21 phases (Phase 0 to Phase 20) grouped into 6 coherent milestones as defined in `phase.md`. The journey transitions from establishing a robust, safe database connection and deterministic tooling, to orchestrating an autonomous LangGraph agent, building human-in-the-loop clarification, implementing hypothesis testing and evidence tracking, crafting a bespoke Streamlit intelligence interface, and completing production hardening.

## Milestones

- 🏗️ **Milestone 1: Foundation** — Phases 0–3 (Database Connection, Schema Tools, Safe SQL)
- 🤖 **Milestone 2: Agent** — Phases 4–6 (LangGraph Orchestration, Dynamic Loop, Clarification)
- 📊 **Milestone 3: Analyst (Core MVP)** — Phases 7–10 (Evidence System, Hypothesis Engine, Streamlit UI, Visualization)
- 🧠 **Milestone 4: Intelligence** — Phases 11–13 (Ask Mode, Investigate Mode, Explore Mode)
- 🛡️ **Milestone 5: Reliability** — Phases 14–17 (Automated Testing, Resilience, Security, Performance)
- 🚀 **Milestone 6: Advanced Agent** — Phases 18–20 (Data Intelligence, Proactive Insights, Scheduled Monitoring)

---

## Phases

### Milestone 1: Foundation (Phases 0–3)

- [ ] **Phase 0: Project Foundation** — Clean Python project skeleton, dependency management, virtual environment configuration, and Streamlit shell.
- [ ] **Phase 1: Database Connection Layer** — Reliable PostgreSQL connection engine via SQLAlchemy with read-only connection management and error handling.
- [ ] **Phase 2: Database Understanding Tools** — Deterministic schema inspection tools (`inspect_database`, `inspect_table`, `inspect_relationships`) without LLM hallucination.
- [ ] **Phase 3: SQL Generation and Safety** — Robust SQL safety validator blocking all write/DDL operations, execution engine with timeouts and row limits, and structured output.

### Milestone 2: Agent (Phases 4–6)

- [ ] **Phase 4: First Working Agent** — Minimal stateful LangGraph agent answering simple natural-language questions through schema inspection and SQL execution.
- [ ] **Phase 5: Dynamic Agent Loop** — Fully dynamic investigation loop allowing the agent to observe intermediate query results and determine subsequent tool actions.
- [ ] **Phase 6: Clarification / Human-in-the-Loop** — Ambiguity detection and interactive user clarification pauses with bounded rounds.

### Milestone 3: Analyst / Core MVP (Phases 7–10)

- [ ] **Phase 7: Evidence System** — Comprehensive evidence trail tracking queries, results, and metric derivations behind every analytical conclusion.
- [ ] **Phase 8: Investigation and Hypothesis Testing** — Formulation and systematic testing of alternative candidate hypotheses for complex "why" questions.
- [ ] **Phase 9: Streamlit Intelligence UI** — Production-grade analytics workspace with vertical narrative layout, high-level activity feed, finding cards, and SQL viewer.
- [ ] **Phase 10: Visualization** — Automated and agent-selected Plotly charts generated directly from query results and integrated into findings.

### Milestone 4: Intelligence (Phases 11–13)

- [ ] **Phase 11: Ask Mode** — Streamlined execution for direct, single-turn factual questions with quick response and result tables.
- [ ] **Phase 12: Investigate Mode** — Multi-step investigative workflow showcasing autonomous hypothesis evaluation and deep-dive reporting.
- [ ] **Phase 13: Explore Mode** — Autonomous pattern, trend, and anomaly discovery without predefined questions.

### Milestone 5: Reliability & Hardening (Phases 14–17)

- [ ] **Phase 14: Reliability and Testing** — Comprehensive unit, tool, and agent scenario tests covering positive and negative edge cases.
- [ ] **Phase 15: Error Handling and Resilience** — Graceful recovery from database timeouts, provider errors, and bounded query repair loops.
- [ ] **Phase 16: Security and Production Hardening** — Defense-in-depth security, credential isolation, prompt injection defenses, and strict resource limits.
- [ ] **Phase 17: Performance Optimization** — Schema caching, token pruning, and query latency minimization.

### Milestone 6: Advanced Agent (Phases 18–20)

- [ ] **Phase 18: Advanced Data Intelligence** — Data quality auditing and automated anomaly detection across tables.
- [ ] **Phase 19: Proactive Insights** — Change detection and proactive analytical summaries.
- [ ] **Phase 20: Scheduled Monitoring** — Recurrent background monitoring jobs with alert generation.

---

## Phase Details

### Phase 0: Project Foundation
**Goal**: Create a clean Python project with the basic architecture, dependencies, and development environment.  
**Depends on**: Nothing (first phase)  
**Requirements**: FOUND-01, FOUND-02, FOUND-03, FOUND-04, FOUND-05  
**Success Criteria**:
1. Virtual environment and dependencies in `requirements.txt` install cleanly.
2. Directory structure created matching architectural specification.
3. `.env.example` provided with proper environment variable templates and secrets gitignored.
4. Streamlit application entry point `app.py` launches without import or runtime errors.
5. Basic pytest test suite runs and passes.  
**Plans**: 1 plan

Plans:
- [ ] 00-01: Project structure setup, dependency specification, environment configuration, and verification tests.

### Phase 1: Database Connection Layer
**Goal**: Implement a reliable, testable PostgreSQL connection layer via SQLAlchemy with read-only connection configuration.  
**Depends on**: Phase 0  
**Requirements**: DB-01, DB-02, DB-03, DB-04  
**Success Criteria**:
1. User can configure PostgreSQL connection URL via environment variable or UI.
2. System establishes connection and validates connectivity.
3. Connection errors (timeout, invalid credentials, unreachable host) are trapped and reported cleanly.
4. Streamlit displays connection status badge.  
**Plans**: 1 plan

Plans:
- [ ] 01-01: Database connection manager, connection testing functions, error handling, and connection status UI component.

### Phase 2: Database Understanding Tools
**Goal**: Provide deterministic tools for inspecting an unfamiliar database schema without LLM guessing.  
**Depends on**: Phase 1  
**Requirements**: SCHEMA-01, SCHEMA-02, SCHEMA-03, SCHEMA-04  
**Success Criteria**:
1. `inspect_database()` returns all tables, columns, and data types in structured format.
2. `inspect_table()` returns column nullable flags, default values, and primary keys for a given table.
3. `inspect_relationships()` returns foreign keys and table associations.
4. Schema tools run deterministically without contacting LLM.  
**Plans**: 1 plan

Plans:
- [ ] 02-01: Schema inspector service, database tools implementation, caching, and automated verification tests.

### Phase 3: SQL Generation and Safety
**Goal**: Create a robust SQL safety validator and safe execution engine before giving LLMs query privileges.  
**Depends on**: Phase 2  
**Requirements**: SAFE-01, SAFE-02, SAFE-03, SAFE-04, SAFE-05, SAFE-06  
**Success Criteria**:
1. AST/keyword validator strictly blocks INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, and other write operations.
2. SELECT and read-only CTE queries are allowed.
3. Queries execute with enforced `MAX_QUERY_ROWS = 500` and `QUERY_TIMEOUT = 30s`.
4. Structured results return columns, typed rows, row counts, and execution latency.
5. Malformed queries return structured errors with bounded repair attempts.  
**Plans**: 1 plan

Plans:
- [ ] 03-01: SQL AST safety validator, safe query executor, row limiters, timeout wrappers, and security test suite.

### Phase 4: First Working Agent
**Goal**: Construct the simplest functional LangGraph agent connecting user questions to database inspection, SQL generation, and answers.  
**Depends on**: Phase 3  
**Requirements**: AGENT-01, AGENT-02, AGENT-03, AGENT-04, AGENT-05  
**Success Criteria**:
1. Typed `AgentState` manages question, context, messages, and results.
2. LangGraph graph executes end-to-end for simple questions.
3. Agent uses schema tools and query tools to answer direct business questions.
4. Step counter enforces `MAX_AGENT_STEPS = 15`.  
**Plans**: 1 plan

Plans:
- [ ] 04-01: Agent state definition, core LangGraph nodes and router, prompt engineering, and end-to-end question test.

### Phase 5: Dynamic Agent Loop
**Goal**: Upgrade agent from a linear sequence to a truly dynamic decision loop driven by intermediate observations.  
**Depends on**: Phase 4  
**Requirements**: LOOP-01, LOOP-02, LOOP-03  
**Success Criteria**:
1. Agent inspects query results and decides whether further investigation is needed.
2. Agent takes different tool paths based on observed findings.
3. Agent tracks intermediate observations and maintains investigation progress.  
**Plans**: 1 plan

Plans:
- [ ] 05-01: Dynamic routing node, observation feedback logic, multi-turn tool calling, and scenario tests.

### Phase 6: Clarification / Human-in-the-Loop
**Goal**: Allow the agent to detect ambiguous requests and pause execution to seek targeted user clarification.  
**Depends on**: Phase 5  
**Requirements**: CLAR-01, CLAR-02, CLAR-03, CLAR-04  
**Success Criteria**:
1. Agent identifies semantic ambiguities (e.g., undefined "best", "inactive") when multiple valid metrics exist.
2. Agent pauses graph execution and provides clear multiple-choice options.
3. User selection resumes graph execution with updated context.
4. Clarification is bounded to at most 3 rounds.  
**Plans**: 1 plan

Plans:
- [ ] 06-01: Ambiguity detection logic, clarification tool, graph pause/resume mechanics, and UI interactive component.

### Phase 7: Evidence System (Core MVP Milestone)
**Goal**: Build an audit-grade evidence trail linking all major findings to verifiable database queries and calculations.  
**Depends on**: Phase 6  
**Requirements**: EVID-01, EVID-02, EVID-03, EVID-04  
**Success Criteria**:
1. Structured evidence objects record query SQL, result data, purpose, and supported findings.
2. Final answer distinguishes verified facts from speculative interpretations.
3. Users can inspect underlying evidence for every key finding.  
**Plans**: 1 plan

Plans:
- [ ] 07-01: Evidence data models, result analyzer, metric calculation utilities, and evidence trail builder.

### Phase 8: Investigation and Hypothesis Testing
**Goal**: Add hypothesis generation and testing for complex analytical questions ("Why did revenue fall?").  
**Depends on**: Phase 7  
**Requirements**: HYPO-01, HYPO-02, HYPO-03, HYPO-04  
**Success Criteria**:
1. Agent generates candidate hypotheses for business questions.
2. Agent executes queries to systematically validate or reject each hypothesis.
3. Findings report supported vs. refuted hypotheses with concrete numbers.  
**Plans**: 1 plan

Plans:
- [ ] 08-01: Hypothesis data models, evaluation engine, hypothesis testing prompts, and multi-hypothesis scenarios.

### Phase 9: Streamlit Intelligence UI
**Goal**: Deliver a polished, restrained Streamlit interface embodying the "AI Data Analyst" experience according to `design.md`.  
**Depends on**: Phase 8  
**Requirements**: UI-01, UI-02, UI-03, UI-04, UI-05, UI-06, UI-07  
**Success Criteria**:
1. Persistent shell with workspace sidebar and vertical narrative main area.
2. Activity feed displays real-time high-level steps without exposing private chain-of-thought.
3. Findings cards render metrics, comparisons, and evidence drill-down buttons.
4. Formatted SQL viewer allows inspection of queries.  
**Plans**: 2 plans

Plans:
- [ ] 09-01: Layout shell, sidebar, query input area, and activity feed components.
- [ ] 09-02: Finding cards, metric displays, SQL modal/expander, and clarification interaction components.

### Phase 10: Visualization
**Goal**: Automatically select and render appropriate Plotly charts for analytical findings.  
**Depends on**: Phase 9  
**Requirements**: VIZ-01, VIZ-02, VIZ-03, VIZ-04  
**Success Criteria**:
1. Chart generator produces interactive Plotly figures from query result DataFrames.
2. Rule-based/agentic chart selector chooses line charts for time-series, bar charts for categories, and scatter for bivariate relationships.
3. Charts render seamlessly within Streamlit finding cards with labels and formatting.  
**Plans**: 1 plan

Plans:
- [ ] 10-01: Chart selector, Plotly styling theme, chart generator tools, and Streamlit display integration.

### Phase 11: Ask Mode
**Goal**: Optimize the system for fast, direct, single-turn factual questions.  
**Depends on**: Phase 10  
**Requirements**: MODE-01  
**Success Criteria**:
1. Simple questions execute with minimal unnecessary exploration steps.
2. Response includes direct answer, result table, SQL query, and optional chart.  
**Plans**: 1 plan

Plans:
- [ ] 11-01: Ask mode routing, expedited prompt path, result table presentation, and latency benchmarks.

### Phase 12: Investigate Mode
**Goal**: Perfect the end-to-end multi-step investigation experience as the primary showcase capability.  
**Depends on**: Phase 11  
**Requirements**: MODE-02  
**Success Criteria**:
1. Complex diagnostic questions trigger full hypothesis testing and evidence synthesis.
2. Narrative report compiles findings, key contributors, charts, and limitations.  
**Plans**: 1 plan

Plans:
- [ ] 12-01: Investigation workflow tuning, synthesis reporting, limitation reporting, and complex case verification.

### Phase 13: Explore Mode
**Goal**: Enable autonomous pattern, trend, and anomaly discovery without requiring a specific user question.  
**Depends on**: Phase 12  
**Requirements**: MODE-03  
**Success Criteria**:
1. Agent scans schema, identifies relevant metrics, and runs exploratory queries.
2. Statistical noise is filtered; only verified findings are surfaced.  
**Plans**: 1 plan

Plans:
- [ ] 13-01: Exploration heuristics, metric candidate generation, noise filtering, and overview card UI.

### Phase 14: Reliability and Testing
**Goal**: Build comprehensive test coverage across unit, integration, and agent execution layers.  
**Depends on**: Phase 13  
**Requirements**: REL-01  
**Success Criteria**:
1. Unit tests cover all database, safety, and analysis tools.
2. Agent scenario tests verify normal, edge, and error conditions.
3. Safety test suite confirms 100% of destructive operations are rejected.  
**Plans**: 1 plan

Plans:
- [ ] 14-01: Unit test expansion, agent scenario fixtures, safety regression suite, and CI test runner.

### Phase 15: Error Handling and Resilience
**Goal**: Ensure system fails gracefully under database timeouts, malformed SQL, or LLM rate limits.  
**Depends on**: Phase 14  
**Requirements**: REL-02  
**Success Criteria**:
1. Database timeouts or disconnects produce clear user messages without crashing Streamlit.
2. SQL syntax errors trigger automatic repair with repair attempt cap.
3. LLM rate limits and errors are caught with user-friendly retry guidance.  
**Plans**: 1 plan

Plans:
- [ ] 15-01: Exception hierarchy, retry decorators, boundary error handlers, and failure UI displays.

### Phase 16: Security and Production Hardening
**Goal**: Implement comprehensive defense-in-depth security and credential isolation.  
**Depends on**: Phase 15  
**Requirements**: REL-03  
**Success Criteria**:
1. Database credentials are isolated from agent prompt context.
2. Prompt injection attempts inside database values or user queries cannot override safety rules.
3. Strict execution timeouts and memory/row limits are enforced.  
**Plans**: 1 plan

Plans:
- [ ] 16-01: Security hardening audit, prompt sanitization, credential masking, and production limits.

### Phase 17: Performance Optimization
**Goal**: Optimize latency, token utilization, and database resource usage.  
**Depends on**: Phase 16  
**Requirements**: REL-04  
**Success Criteria**:
1. Schema information is cached to eliminate redundant discovery calls.
2. Agent message history is pruned to retain only relevant findings and context.
3. Common query execution latency is reduced.  
**Plans**: 1 plan

Plans:
- [ ] 17-01: Schema caching layer, state compaction, token profiling, and latency optimization.

### Phase 18: Advanced Data Intelligence
**Goal**: Provide data quality profiling and anomaly detection capabilities.  
**Depends on**: Phase 17  
**Requirements**: ADV-01  
**Success Criteria**:
1. System identifies missing values, schema inconsistencies, and outlier records.
2. Data health overview report is generated on request.  
**Plans**: 1 plan

Plans:
- [ ] 18-01: Data quality analyzer, anomaly detection heuristics, and health report views.

### Phase 19: Proactive Insights
**Goal**: Implement change detection and proactive analytical summaries.  
**Depends on**: Phase 18  
**Requirements**: ADV-02  
**Success Criteria**:
1. Baseline metrics are compared against recent periods to detect notable shifts.
2. Proactive summary alerts highlight significant metric deviations.  
**Plans**: 1 plan

Plans:
- [ ] 19-01: Baseline tracker, delta comparison engine, and proactive insight cards.

### Phase 20: Scheduled Monitoring
**Goal**: Enable recurring scheduled investigations and automated monitoring reports.  
**Depends on**: Phase 19  
**Requirements**: ADV-03  
**Success Criteria**:
1. Scheduled jobs execute recurring database analyses.
2. Notification summaries highlight key weekly/monthly changes.  
**Plans**: 1 plan

Plans:
- [ ] 20-01: Scheduler integration, recurring report runner, and notification formatting.

---

## Progress

**Execution Order:**
Phases execute strictly in numeric order: 0 → 1 → 2 → ... → 20

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 0. Project Foundation | Milestone 1: Foundation | 0/1 | In progress | - |
| 1. Database Connection Layer | Milestone 1: Foundation | 0/1 | Not started | - |
| 2. Database Understanding Tools | Milestone 1: Foundation | 0/1 | Not started | - |
| 3. SQL Generation and Safety | Milestone 1: Foundation | 0/1 | Not started | - |
| 4. First Working Agent | Milestone 2: Agent | 0/1 | Not started | - |
| 5. Dynamic Agent Loop | Milestone 2: Agent | 0/1 | Not started | - |
| 6. Clarification / Human-in-the-Loop | Milestone 2: Agent | 0/1 | Not started | - |
| 7. Evidence System (Core MVP) | Milestone 3: Analyst | 0/1 | Not started | - |
| 8. Investigation & Hypotheses | Milestone 3: Analyst | 0/1 | Not started | - |
| 9. Streamlit Intelligence UI | Milestone 3: Analyst | 0/2 | Not started | - |
| 10. Visualization | Milestone 3: Analyst | 0/1 | Not started | - |
| 11. Ask Mode | Milestone 4: Intelligence | 0/1 | Not started | - |
| 12. Investigate Mode | Milestone 4: Intelligence | 0/1 | Not started | - |
| 13. Explore Mode | Milestone 4: Intelligence | 0/1 | Not started | - |
| 14. Reliability and Testing | Milestone 5: Reliability | 0/1 | Not started | - |
| 15. Error Handling & Resilience | Milestone 5: Reliability | 0/1 | Not started | - |
| 16. Security & Hardening | Milestone 5: Reliability | 0/1 | Not started | - |
| 17. Performance Optimization | Milestone 5: Reliability | 0/1 | Not started | - |
| 18. Advanced Data Intelligence | Milestone 6: Advanced | 0/1 | Not started | - |
| 19. Proactive Insights | Milestone 6: Advanced | 0/1 | Not started | - |
| 20. Scheduled Monitoring | Milestone 6: Advanced | 0/1 | Not started | - |

---
*Roadmap defined: 2026-10-02 based on authoritative phase.md*  
*Last updated: 2026-10-02 after initial definition*
