# SQLPilot Development Phases

## Purpose

This document breaks the SQLPilot project into controlled implementation phases so a coding agent can build the system incrementally without attempting to implement the entire application at once.

SQLPilot is an **Agentic AI Data Analyst**. The user connects a relational database and asks business questions in natural language. The agent investigates the database, selects tools, executes safe SQL, observes results, decides what to do next, and produces evidence-backed answers.

The project is intentionally not a simple:

```text
Question → LLM → SQL → Answer
```

The core runtime behavior is:

```text
User Goal
   ↓
Agent Decision
   ↓
Tool
   ↓
Observation
   ↓
Agent Decision
   ↓
Tool / Clarification
   ↓
Observation
   ↓
Evidence
   ↓
Final Answer
```

The development plan below turns that behavior into a sequence of independently testable milestones.

---

# 1. How the Coding Agent Must Use This File

The coding agent must follow the phases **in order**.

For each phase:

1. Read the relevant requirements.
2. Inspect the existing repository before changing anything.
3. Implement only the scope of the current phase.
4. Run the phase's tests/checks.
5. Fix errors before moving forward.
6. Do not silently implement future-phase features.
7. Update documentation when architecture changes.
8. Leave the repository in a runnable state.

### Important rule

> **Never implement Phase N+1 just because it looks easy while Phase N is incomplete.**

This prevents the project from becoming a pile of half-connected features, which is a remarkably popular software engineering hobby.

---

# 2. Phase Overview

```text
PHASE 0
Project Foundation
        ↓
PHASE 1
Database Connection
        ↓
PHASE 2
Database Understanding Tools
        ↓
PHASE 3
SQL Generation + Safety
        ↓
PHASE 4
Basic Agent
        ↓
PHASE 5
Dynamic Agent Loop
        ↓
PHASE 6
Clarification / Human-in-the-Loop
        ↓
PHASE 7
Evidence System
        ↓
PHASE 8
Investigation + Hypothesis Testing
        ↓
PHASE 9
Streamlit Intelligence UI
        ↓
PHASE 10
Visualization
        ↓
PHASE 11
Explore Mode
        ↓
PHASE 12
Reliability + Testing
        ↓
PHASE 13
Production Hardening
        ↓
PHASE 14
Advanced Features
```

The first meaningful MVP is reached around **Phase 7**.

The more impressive agentic demonstration is reached around **Phase 8–10**.

---

# 3. Phase 0 — Project Foundation

## Goal

Create a clean Python project with the basic architecture and development environment.

## Build

Create:

```text
sqlpilot/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── agent/
├── tools/
├── database/
├── analysis/
├── visualization/
├── models/
├── ui/
└── tests/
```

## Technology

Use:

```text
Python
Streamlit
LangChain
LangGraph
SQLAlchemy
PostgreSQL driver
Pydantic
Plotly
python-dotenv
pytest
```

## Requirements

- Create virtual environment instructions.
- Create dependency file.
- Create environment configuration.
- Create application entry point.
- Ensure Streamlit launches.
- Ensure imports work.

## Do Not Build Yet

Do not implement:

- agent logic,
- SQL generation,
- tool calling,
- investigation,
- charts,
- hypothesis testing.

## Done When

```text
[ ] Project starts
[ ] Streamlit opens
[ ] Dependencies install
[ ] .env.example exists
[ ] Git ignores secrets
[ ] Folder structure exists
```

---

# 4. Phase 1 — Database Connection Layer

## Goal

Make SQLPilot reliably connect to PostgreSQL.

The project initially targets PostgreSQL as the relational database.

## Build

```text
database/
├── connection.py
├── executor.py
└── safety.py
```

Start with `connection.py`.

Implement:

```python
create_engine()
test_connection()
get_connection()
```

## Requirements

Support:

- database URL from environment;
- connection testing;
- connection errors;
- read-only connection configuration where practical.

## UI

Create a minimal connection screen:

```text
Database
──────────────
PostgreSQL

[ Connection URL ]

[ Connect ]

● Connected
```

## Error Cases

Handle:

- invalid URL;
- wrong password;
- unavailable server;
- database does not exist;
- timeout.

## Tests

```text
test_database_connection()
test_invalid_connection()
```

## Done When

The application can connect to the test PostgreSQL database and clearly report success/failure.

---

# 5. Phase 2 — Database Understanding

## Goal

Give the system deterministic capabilities for understanding an unfamiliar database.

The agent needs database knowledge before it can reliably investigate business questions.

## Build Tools

```text
tools/schema_tools.py
database/schema_inspector.py
```

Implement:

```text
inspect_database()
inspect_table()
inspect_relationships()
```

## `inspect_database()`

Return:

```text
tables
columns
data types
primary keys
```

## `inspect_table(table_name)`

Return:

```text
column names
data types
nullable information
primary keys
```

## `inspect_relationships()`

Return:

```text
foreign keys
referenced tables
relationship direction
```

## Important

Schema inspection must be deterministic.

Do not ask an LLM to "guess" the schema.

## Example Result

```python
{
    "tables": [
        {
            "name": "orders",
            "columns": [...]
        }
    ],
    "relationships": [...]
}
```

## Tests

```text
test_inspect_database()
test_inspect_table()
test_inspect_relationships()
```

## Done When

The system can inspect an unknown PostgreSQL database and return structured schema information.

---

# 6. Phase 3 — SQL Generation and Safety

## Goal

Create a safe SQL capability before allowing an LLM to execute queries.

This phase is critical.

## Build

```text
tools/query_tools.py
database/safety.py
database/executor.py
models/structured_outputs.py
```

Implement:

```text
generate_query()
validate_sql()
execute_query()
```

## SQL Safety

Reject at minimum:

```text
INSERT
UPDATE
DELETE
MERGE
UPSERT
CREATE
ALTER
DROP
TRUNCATE
GRANT
REVOKE
```

Only read-oriented SQL should reach the database.

## Query Limits

Implement:

```text
MAX_QUERY_ROWS
QUERY_TIMEOUT
MAX_SQL_REPAIR_ATTEMPTS
```

Initial defaults can be:

```text
MAX_QUERY_ROWS = 500
QUERY_TIMEOUT = 30 seconds
MAX_SQL_REPAIR_ATTEMPTS = 2
```

## Structured Result

Successful execution:

```python
{
    "status": "success",
    "columns": [...],
    "rows": [...],
    "row_count": 10
}
```

Failure:

```python
{
    "status": "error",
    "error_type": "sql_error",
    "message": "..."
}
```

## Tests

Test both allowed and prohibited SQL.

```text
SELECT → allowed
WITH → allowed when read-only
INSERT → blocked
UPDATE → blocked
DELETE → blocked
DROP → blocked
ALTER → blocked
TRUNCATE → blocked
```

## Done When

No model-generated SQL can bypass the safety layer.

---

# 7. Phase 4 — First Working Agent

## Goal

Create the smallest real LangGraph agent.

This is the first point where the application becomes an agentic system.

## Build

```text
agent/
├── state.py
├── graph.py
├── nodes.py
├── router.py
└── prompts.py
```

## Agent State

Start with:

```python
class AgentState(TypedDict):
    user_question: str
    database_context: dict
    messages: list
    last_tool: str | None
    last_tool_result: dict | None
    final_answer: str | None
    is_complete: bool
```

## Initial Agent Capability

The agent should be able to:

```text
User question
      ↓
Inspect database
      ↓
Generate SQL
      ↓
Execute SQL
      ↓
Answer
```

This is intentionally simple.

## Example

User:

> What are the top 10 products by revenue?

Agent:

```text
inspect_database()
      ↓
generate SQL
      ↓
validate SQL
      ↓
execute SQL
      ↓
answer
```

## Done When

A simple natural-language question can be answered end-to-end through LangGraph and the real database.

---

# 8. Phase 5 — Dynamic Agent Loop

## Goal

Transform the basic agent into a genuinely agentic system.

This is one of the most important phases.

The project definition requires the agent to observe results and decide what to investigate next rather than follow a fixed sequence.

## Build

The graph should support:

```text
Agent
 ↓
Tool
 ↓
Observation
 ↓
Agent
 ↓
Tool
 ↓
Observation
 ↓
...
```

## Agent Decisions

The agent should be able to choose:

```text
inspect database
inspect table
execute query
analyze result
continue investigation
finish
```

## Example

Question:

> Why did revenue decrease?

Possible runtime:

```text
inspect_database()
      ↓
monthly revenue query
      ↓
observe decrease
      ↓
revenue by category
      ↓
observe Electronics decline
      ↓
order volume query
      ↓
observe stable order volume
      ↓
AOV query
      ↓
observe lower AOV
      ↓
finish
```

The exact sequence must not be hard-coded.

## Agent Step Limit

Add:

```text
MAX_AGENT_STEPS = 15
```

If reached:

```text
stop
+
summarize evidence
+
explain uncertainty
```

## Done When

Different questions can cause the agent to take different tool paths.

---

# 9. Phase 6 — Clarification / Human-in-the-Loop

## Goal

Allow the agent to stop and ask the user for missing information.

The project explicitly includes ambiguity resolution as part of the analyst behavior.

## Build

```text
tools/clarification_tools.py
ui/clarification.py
```

## Example

User:

> Show me the best customers.

Agent identifies:

```text
"best" is ambiguous
```

UI:

```text
How should "best customers" be defined?

○ Highest total spending
○ Most orders
○ Highest average order value
○ Most recent purchases
```

User chooses:

```text
Highest total spending
```

The agent resumes.

## LangGraph Behavior

Conceptually:

```text
Agent
 ↓
Clarification required
 ↓
Pause
 ↓
Human response
 ↓
Resume graph
```

## Limits

```text
MAX_CLARIFICATION_ROUNDS = 3
```

## Done When

The agent can pause, collect a user decision, update state, and continue the investigation.

---

# 10. Phase 7 — Evidence System

## Goal

Make every important conclusion traceable to actual database evidence.

This is the first major reliability feature.

## Build

```text
analysis/
├── evidence.py
├── result_analyzer.py
└── metrics.py
```

## Evidence Object

Conceptually:

```python
{
    "id": "evidence_001",
    "finding": "Revenue decreased 27.4%",
    "query_id": "query_001",
    "sql": "...",
    "result": {...},
    "purpose": "Monthly revenue comparison"
}
```

## Track

For every investigation:

```text
query
purpose
result
finding
relationship
```

## UI

Allow:

```text
Finding
 ↓
View Evidence
 ↓
Query
 ↓
Result
```

## Done When

A user can inspect why the agent made an important conclusion.

---

# 11. Phase 8 — Investigation and Hypothesis Testing

## Goal

Add the core "AI analyst" behavior.

This should become the signature feature.

## Build

```text
analysis/hypothesis.py
```

## Hypothesis Model

Example:

```python
{
    "id": "H1",
    "description": "Order volume decreased",
    "status": "supported | weak | rejected | unknown",
    "evidence_ids": [...]
}
```

## Example Investigation

Question:

> Why did sales decrease?

Agent creates possible hypotheses:

```text
H1: Fewer orders
H2: Lower average order value
H3: Product category decline
H4: Regional decline
H5: Customer activity decline
```

Then tests them.

```text
H1
 ↓
Orders decreased only 2%
 ↓
Weak explanation

H2
 ↓
AOV decreased 23%
 ↓
Supported

H3
 ↓
Electronics decreased 47%
 ↓
Supported
```

## Important Boundary

Do not expose private chain-of-thought.

The application should show:

```text
Hypothesis
Evidence
Result
Status
```

not hidden model reasoning.

## Done When

The agent can investigate a "why" question through multiple evidence-backed hypotheses.

---

# 12. Phase 9 — Streamlit Intelligence UI

## Goal

Move from a functional prototype to a proper AI analyst interface.

The UI should make the agent's work understandable.

## Build

```text
ui/
├── sidebar.py
├── query_input.py
├── mode_selector.py
├── investigation.py
├── clarification.py
├── findings.py
├── evidence.py
└── sql_viewer.py
```

## Main UI

```text
┌─────────────────────────────────────────────────────────┐
│ SQLPILOT                              ● Connected       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Ask your database                                      │
│                                                         │
│ [ Why did revenue decrease last month? ]               │
│                                                         │
│              [ Ask ] [ Investigate ] [ Explore ]        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ INVESTIGATION                                          │
│                                                         │
│ ✓ Understanding database                               │
│ ✓ Checking monthly revenue                             │
│ ● Comparing categories                                 │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ FINDINGS                                               │
│                                                         │
│ Revenue decreased 27.4%                                │
│                                                         │
│ [ chart ]                                              │
│                                                         │
│ [ View SQL ]  [ View Evidence ]                        │
└─────────────────────────────────────────────────────────┘
```

## Important

Do not expose private chain-of-thought.

Show only high-level activity.

## Done When

The entire investigation can be performed from Streamlit without developer intervention.

---

# 13. Phase 10 — Visualization

## Goal

Allow the agent to request useful visualizations from real query results.

## Build

```text
visualization/
├── charts.py
└── chart_selector.py

tools/
└── visualization_tools.py
```

## Basic Mapping

```text
time series
→ line chart

category comparison
→ bar chart

two numeric variables
→ scatter plot
```

## Rule

Do not create charts just because charts are available.

Create them when they improve understanding.

## Example

```text
Revenue by month
→ Line chart
```

## Done When

The agent can request a chart and Streamlit renders it from actual query results.

---

# 14. Phase 11 — Ask Mode

## Goal

Optimize the system for straightforward questions.

Example:

> What were our top 10 products last month?

Expected:

```text
Understand
 ↓
Query
 ↓
Answer
```

## Requirements

- Fast execution.
- Minimal unnecessary investigation.
- SQL visible.
- Result table.
- Optional chart.

## Done When

Simple questions are answered without unnecessary multi-step investigation.

---

# 15. Phase 12 — Investigate Mode

## Goal

Make complex investigation the main showcase mode.

Example:

> Why did revenue decrease?

Expected behavior:

```text
Understand
 ↓
Investigate
 ↓
Query
 ↓
Observe
 ↓
Hypothesize
 ↓
Test
 ↓
Verify
 ↓
Answer
```

## UI

Show:

```text
Investigation
──────────────
✓ Database inspected
✓ Revenue trend checked
✓ Categories compared
✓ Order volume checked
● Verifying AOV impact
```

Then:

```text
Finding
Revenue decreased 27.4%

Evidence
4 supporting queries

Visualization
Revenue trend

SQL
Expandable
```

## Done When

The project can convincingly demonstrate autonomous investigation.

---

# 16. Phase 13 — Explore Mode

## Goal

Allow the agent to discover potentially useful patterns without a specific question.

Example:

> Explore this database and tell me something interesting.

## Flow

```text
Understand database
 ↓
Identify useful metrics
 ↓
Generate candidate observations
 ↓
Test observations
 ↓
Reject weak/noisy findings
 ↓
Present supported findings
```

## Important

The agent should not report random statistical noise as a business insight.

Potential finding:

```text
Customer retention changed significantly.
```

should be validated before being shown.

## Done When

The agent can produce a small number of evidence-backed interesting findings.

---

# 17. Phase 14 — Reliability and Testing

## Goal

Make the system reliable enough for repeated use.

## Unit Tests

Test:

```text
database connection
schema inspection
SQL safety
SQL execution
result analysis
hypothesis logic
chart selection
```

## Tool Tests

Test:

```text
inspect_database()
inspect_table()
inspect_relationships()
execute_query()
analyze_results()
```

## Agent Tests

Create scenarios:

```text
simple question
ambiguous question
missing data
SQL error
empty result
multi-step investigation
clarification
step limit
```

## Safety Tests

Verify:

```text
INSERT → blocked
UPDATE → blocked
DELETE → blocked
DROP → blocked
ALTER → blocked
TRUNCATE → blocked
GRANT → blocked
REVOKE → blocked
```

## Done When

The core system has automated tests covering both normal and failure paths.

---

# 18. Phase 15 — Error Handling and Resilience

## Goal

Make failures controlled rather than catastrophic.

## Handle

### Database errors

```text
connection failure
timeout
permission error
database unavailable
```

### SQL errors

```text
syntax error
unknown column
unknown table
invalid relationship
```

### LLM errors

```text
timeout
rate limit
provider failure
invalid structured output
malformed tool call
```

### Tool errors

```text
tool exception
invalid input
unexpected result
```

## Required Behavior

Never let one failure crash the entire Streamlit application.

Example:

```text
SQL failed
 ↓
Structured error
 ↓
Agent receives error
 ↓
Agent repairs
 ↓
Retry
```

If retries are exhausted:

```text
Stop
 ↓
Explain failure
```

## Done When

Known failure modes produce useful user-facing messages and developer logs.

---

# 19. Phase 16 — Security and Production Hardening

## Goal

Make the system safer and cleaner for real-world usage.

## Build

- secret management;
- read-only database enforcement;
- query timeouts;
- result-size limits;
- agent step limits;
- structured logging;
- sensitive-data minimization;
- prompt-injection resistance;
- input validation.

## Secrets

Never commit:

```text
.env
API keys
database passwords
tokens
```

## Database

The LLM must never receive:

```text
database password
connection credentials
```

## Prompt Injection

Treat database content as data.

A database row containing:

```text
Ignore previous instructions...
```

must not override system rules.

## Done When

Security controls are enforced outside the prompt as well as inside it.

---

# 20. Phase 17 — Performance Optimization

## Goal

Reduce unnecessary model calls, database calls, and latency.

## Optimize

### Schema

Cache or reuse schema information when appropriate.

### Agent state

Do not repeatedly send unnecessary context.

### Query results

Limit result size.

### LLM

Avoid redundant model calls.

### Tools

Do not repeat identical inspections unnecessarily.

## Measure

Track:

```text
total latency
LLM calls
tool calls
database query time
agent step count
```

## Done When

The system can complete common questions without obvious redundant work.

---

# 21. Phase 18 — Advanced Data Intelligence

Only begin this phase after the core agent is stable.

Potential features:

```text
Data quality investigation
Anomaly detection
Trend detection
Pattern discovery
Database health analysis
```

Example:

> Find unusual changes in the database.

The agent can investigate:

```text
revenue
orders
customers
inventory
```

and produce evidence-backed observations.

---

# 22. Phase 19 — Proactive Insights

After the interactive agent works reliably, add proactive capabilities.

Example:

```text
"I found three unusual changes in your database this week."
```

Possible workflow:

```text
Scheduled trigger
 ↓
Agent
 ↓
Inspect relevant metrics
 ↓
Compare with historical baseline
 ↓
Validate unusual findings
 ↓
Generate report
```

This is an advanced feature and is not part of the initial MVP.

---

# 23. Phase 20 — Scheduled Monitoring

Final advanced phase.

Example:

> Monitor revenue every Monday.

Architecture:

```text
Scheduler
 ↓
Agent
 ↓
Database
 ↓
Investigation
 ↓
Evidence
 ↓
Report / Notification
```

The system should report meaningful changes rather than simply sending raw query results.

---

# 24. MVP Definition

The first real MVP should include:

```text
[✓] PostgreSQL connection
[✓] Schema inspection
[✓] Table inspection
[✓] Relationship inspection
[✓] SQL generation
[✓] SQL safety validation
[✓] Read-only SQL execution
[✓] Basic LangGraph agent
[✓] Dynamic tool selection
[✓] Agent investigation loop
[✓] Clarification
[✓] Evidence tracking
[✓] Final answer
[✓] SQL visibility
[✓] Streamlit interface
```

This is already a serious project.

Do not delay the MVP by trying to build:

```text
Explore Mode
Hypothesis engine
Proactive monitoring
Data quality
```

before the core agent works.

---

# 25. Recommended Implementation Order

The coding agent should follow this exact order:

```text
1. Project setup
        ↓
2. PostgreSQL connection
        ↓
3. Schema inspection
        ↓
4. SQL safety
        ↓
5. SQL execution
        ↓
6. Basic LangGraph agent
        ↓
7. Tool calling
        ↓
8. Dynamic investigation loop
        ↓
9. Clarification
        ↓
10. Evidence
        ↓
11. Hypothesis testing
        ↓
12. Streamlit UI
        ↓
13. Visualization
        ↓
14. Testing
        ↓
15. Reliability
        ↓
16. Security
        ↓
17. Advanced features
```

---

# 26. Phase Completion Contract

At the end of every phase, the coding agent must produce:

## 1. Implementation

The requested feature works.

## 2. Tests

Relevant tests exist and pass.

## 3. Documentation

If architecture or behavior changed, update the appropriate documentation.

## 4. Verification

Report:

```text
What was implemented
What was tested
What passed
What remains
```

## 5. No Hidden Future Work

Do not silently implement unrelated features.

---

# 27. Coding Agent Rules During Development

For every task:

### Step 1

Inspect the repository.

### Step 2

Read:

```text
PRD.md
architecture.md
rules.md
phase.md
```

when relevant to the task.

### Step 3

Identify the current phase.

### Step 4

Implement only that phase's scope.

### Step 5

Run tests.

### Step 6

Fix errors.

### Step 7

Verify integration.

### Step 8

Summarize changes.

---

# 28. If a Phase Fails

Do not continue blindly.

Use:

```text
Phase N
 ↓
Test
 ↓
Failure
 ↓
Diagnose
 ↓
Fix
 ↓
Retest
 ↓
Pass
 ↓
Next Phase
```

Do not build Phase N+1 on top of a broken Phase N.

---

# 29. If the Architecture Needs to Change

Architecture changes are allowed when implementation reveals a real problem.

But the coding agent must:

1. explain the reason;
2. update `architecture.md`;
3. update affected rules;
4. update this phase plan if necessary;
5. avoid silently changing the project's core behavior.

The central principle should remain:

```text
Agent
 ↓
Decide
 ↓
Act
 ↓
Observe
 ↓
Decide again
```

---

# 30. Final Project Milestones

## Milestone 1 — Foundation

```text
Phase 0–3
```

Result:

```text
Reliable database + safe SQL foundation
```

---

## Milestone 2 — Agent

```text
Phase 4–6
```

Result:

```text
Working LangGraph agent
+
tool calling
+
dynamic investigation
+
human clarification
```

---

## Milestone 3 — Analyst

```text
Phase 7–10
```

Result:

```text
Evidence
+
hypothesis testing
+
Streamlit intelligence UI
+
visualization
```

This is the main demonstration version.

---

## Milestone 4 — Intelligence

```text
Phase 11–13
```

Result:

```text
Ask
+
Investigate
+
Explore
```

---

## Milestone 5 — Reliability

```text
Phase 14–17
```

Result:

```text
tested
+
secure
+
bounded
+
performant
```

---

## Milestone 6 — Advanced Agent

```text
Phase 18–20
```

Result:

```text
data intelligence
+
proactive insights
+
scheduled monitoring
```

---

# 31. Final Architecture Evolution

The system should evolve like this:

### Version 0

```text
User
 ↓
Database
```

### Version 1

```text
User
 ↓
SQL Agent
 ↓
Database
```

### Version 2

```text
User
 ↓
Agent
 ↓
Tools
 ↓
Database
 ↓
Agent
 ↓
Answer
```

### Version 3

```text
User
 ↓
Agent
 ↓
Investigate
 ↓
Hypothesize
 ↓
Test
 ↓
Verify
 ↓
Evidence
 ↓
Answer
```

### Final Version

```text
                       USER
                         │
                         ▼
                    SQLPILOT
                         │
                         ▼
                  LANGGRAPH AGENT
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          SCHEMA       QUERY      ANALYSIS
           TOOLS       TOOLS        TOOLS
             │           │           │
             └───────────┼───────────┘
                         ▼
                     DATABASE
                         │
                         ▼
                      RESULTS
                         │
                         ▼
                    AGENT OBSERVES
                         │
                  ┌──────┴──────┐
                  │             │
               MORE DATA       ENOUGH
                  │             │
                  ▼             ▼
              INVESTIGATE     EVIDENCE
                  │             │
                  └──────┬──────┘
                         ▼
                    FINAL ANSWER
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
             SQL      Evidence    Charts
```

---

# 32. Final Development Principle

The project should become more capable **phase by phase**, not more complicated all at once.

The first objective is not:

> "Build every AI feature."

The first objective is:

> **Build one reliable agent that can connect to PostgreSQL, understand the schema, safely query it, observe results, and decide what to do next.**

Once that works, everything else is an extension of the same foundation.

The defining behavior of SQLPilot remains:

```text
BUSINESS QUESTION
       ↓
UNDERSTAND
       ↓
DECIDE
       ↓
ACT
       ↓
OBSERVE
       ↓
DECIDE AGAIN
       ↓
INVESTIGATE
       ↓
VERIFY
       ↓
EVIDENCE
       ↓
ANSWER
```

That loop is the product.

The phases exist to make building that loop manageable.
