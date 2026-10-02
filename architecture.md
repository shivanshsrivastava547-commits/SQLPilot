# Architecture: SQLPilot — Agentic AI Data Analyst

## 1. Purpose

This document defines the technical architecture, application flows, agent behavior, project structure, and technology stack for **SQLPilot**.

SQLPilot is an agentic AI data analyst that allows users to ask business questions about a relational database in natural language.

The system is intentionally designed **not** as a fixed Text-to-SQL pipeline.

Instead, the LangGraph agent dynamically decides:

- what information it needs,
- which tool to call,
- whether the current result is sufficient,
- whether clarification is required,
- whether further investigation is necessary,
- and when it has enough evidence to produce an answer.

The product concept is based on the core flow:

```text
User
 ↓
Agent investigates
 ↓
Understands database
 ↓
Finds relevant data
 ↓
Generates queries
 ↓
Executes queries
 ↓
Observes results
 ↓
Decides what to investigate next
 ↓
Runs additional analysis when necessary
 ↓
Forms evidence-based conclusion
 ↓
Answer + SQL + Evidence + Charts
```

The central agentic principle is:

> **The LLM does not follow a fixed pipeline. It decides what information it needs, which tool to use, whether the result is sufficient, and what action to take next.**

---

# 2. High-Level Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                         STREAMLIT UI                          │
│                                                               │
│  Database Connection  │  Query Input  │  Investigation View  │
│  Findings             │  SQL          │  Evidence            │
│  Charts               │  Clarification UI                    │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                        │
│                                                               │
│  Session Management │ Request Handling │ Response Formatting │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────┐
│                       LANGGRAPH AGENT                         │
│                                                               │
│  Understand Goal                                              │
│  Decide Next Action                                            │
│  Call Tools                                                    │
│  Observe Results                                               │
│  Evaluate Evidence                                            │
│  Continue / Clarify / Finish                                  │
└───────────────┬────────────────┬────────────────┬──────────────┘
                │                │                │
                ▼                ▼                ▼
       ┌────────────────┐ ┌───────────────┐ ┌──────────────────┐
       │ Schema Tools   │ │ Query Tools   │ │ Analysis Tools  │
       │                │ │               │ │                  │
       │ inspect DB     │ │ generate SQL  │ │ analyze results  │
       │ inspect table  │ │ validate SQL  │ │ compare periods  │
       │ relationships  │ │ execute SQL   │ │ hypotheses       │
       └───────┬────────┘ └───────┬───────┘ └────────┬─────────┘
               │                  │                  │
               └──────────────────┼──────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         │   Read-Only DB  │
                         └─────────────────┘

Additional outputs:

Agent ──────────────► Clarification UI
Agent ──────────────► Evidence Store / State
Agent ──────────────► Visualization Tool
Agent ──────────────► Final Response
```

---

# 3. Architectural Principles

## 3.1 Agent-First Architecture

The application should be centered around one LangGraph agent rather than a long chain of predetermined LLM calls.

The agent decides the next action from the current state.

```text
Current State
     ↓
Agent Decision
     ↓
Tool / Clarification / Final Answer
     ↓
Observation
     ↓
Updated State
     ↓
Agent Decision
```

---

## 3.2 Tool-Driven Interaction

The LLM should not directly access the database implementation.

It interacts with the database through controlled tools.

```text
LLM
 ↓
Tool
 ↓
Service Layer
 ↓
Database Layer
 ↓
PostgreSQL
```

This keeps database access deterministic and easier to secure.

---

## 3.3 Read-Only by Default

SQLPilot should initially operate against a read-only database connection.

The agent is intended to analyze data, not modify it.

The architecture should reject destructive SQL before execution.

---

## 3.4 Evidence-Based Answers

The final answer should be derived from actual tool observations.

Important findings should retain:

- the SQL that produced the evidence,
- the result,
- the analytical interpretation,
- and the relationship between the evidence and the finding.

---

## 3.5 No Fabricated Schema

If the database does not contain information needed to answer a question, the agent should explicitly report that limitation.

It must not invent:

- tables,
- columns,
- relationships,
- metrics,
- query results,
- or business facts.

---

## 3.6 No Private Chain-of-Thought Exposure

The UI can show high-level agent activity such as:

```text
✓ Inspecting database
✓ Checking monthly revenue
✓ Comparing categories
● Investigating order value
```

It should not expose hidden model chain-of-thought.

---

# 4. Application Flows

# 4.1 Application Startup Flow

When the application starts:

```text
Streamlit starts
      ↓
Load configuration
      ↓
Initialize LLM
      ↓
Initialize database configuration
      ↓
Initialize LangGraph agent
      ↓
Register tools
      ↓
Initialize Streamlit session state
      ↓
Render application
```

The application should not query the entire database unnecessarily at startup.

---

# 4.2 Database Connection Flow

```text
User
 ↓
Enter PostgreSQL connection information
 ↓
Application validates connection
 ↓
Create SQLAlchemy engine
 ↓
Test read-only connection
 ↓
Discover database metadata
 ↓
Store connection/session information
 ↓
Show "Connected"
```

Example UI:

```text
Database
────────────────────────
PostgreSQL

Host       [ localhost ]
Port       [ 5432 ]
Database   [ analytics ]
Username   [ postgres ]
Password   [ ******** ]

[ Connect ]
```

After successful connection:

```text
● PostgreSQL Connected
```

---

# 4.3 User Question Flow

Example:

> "What were our top 10 products last month?"

Flow:

```text
User Question
      ↓
Streamlit
      ↓
Application Controller
      ↓
Create / update AgentState
      ↓
LangGraph Agent
      ↓
Understand request
      ↓
Inspect schema if required
      ↓
Generate SQL
      ↓
Validate SQL
      ↓
Execute SQL
      ↓
Analyze result
      ↓
Is more investigation needed?
      │
      ├── No ──► Generate answer
      │
      └── Yes ─► Select another tool
                         ↓
                    Continue graph
```

---

# 4.4 Complex Investigation Flow

Example:

> "Why did revenue decrease?"

This should not be forced into a fixed sequence.

A possible execution:

```text
User Question
      ↓
Agent
      ↓
inspect_database()
      ↓
Agent observes schema
      ↓
generate / execute monthly revenue query
      ↓
Agent observes revenue decrease
      ↓
Agent decides more evidence is needed
      ↓
execute revenue-by-category query
      ↓
Agent observes category decline
      ↓
execute order-volume query
      ↓
Agent observes order volume remained stable
      ↓
execute average-order-value query
      ↓
Agent compares evidence
      ↓
Hypothesis supported?
      │
      ├── No ──► Investigate another dimension
      │
      └── Yes
           ↓
      Verify important finding
           ↓
      Build Evidence Trail
           ↓
      Generate chart
           ↓
      Final Answer
```

The exact number and order of tool calls is determined at runtime.

---

# 4.5 Clarification Flow

Example:

> "Show me the best customers."

The agent identifies ambiguity.

```text
User Question
      ↓
Agent
      ↓
Inspect schema if required
      ↓
Detect "best" is ambiguous
      ↓
ask_clarification()
      ↓
Streamlit renders options
      ↓
User selects:
"Highest total spending"
      ↓
Update AgentState
      ↓
Resume LangGraph
      ↓
Generate SQL
      ↓
Execute
      ↓
Analyze
      ↓
Answer
```

The clarification should become part of the current investigation state.

---

# 4.6 Missing-Data Flow

Example:

> "Which marketing campaign generated the most revenue?"

Database:

```text
customers
orders
products
payments
```

No campaign information exists.

Flow:

```text
Question
 ↓
Agent
 ↓
Inspect schema
 ↓
Determine required campaign data is unavailable
 ↓
Do not invent schema
 ↓
Return limitation
```

Example response:

```text
I cannot answer this from the connected database because
campaign or marketing-attribution data is not available.
```

---

# 4.7 SQL Error Flow

```text
Agent generates SQL
      ↓
SQL Validator
      ↓
Invalid
      ↓
Return structured error
      ↓
Agent observes error
      ↓
Agent repairs query
      ↓
Validate again
      ↓
Execute
```

A bounded number of repair attempts should be used to avoid infinite loops.

---

# 4.8 Empty Result Flow

```text
SQL executes
      ↓
Empty result
      ↓
Agent observes empty result
      ↓
Determine whether:
  - filters are too restrictive
  - interpretation is incorrect
  - requested data does not exist
      ↓
Either:
  - modify investigation
  - ask clarification
  - report no matching data
```

The system must not treat an empty result as evidence that a business event did or did not happen without appropriate context.

---

# 4.9 Investigation Completion Flow

The agent should stop when:

```text
Required evidence collected
        AND
Question can be answered
        AND
Important findings are supported
        AND
No required clarification remains
```

Then:

```text
Agent
 ↓
Evidence Builder
 ↓
Result Formatter
 ↓
Visualization Generator if appropriate
 ↓
Streamlit
```

---

# 5. LangGraph Architecture

LangGraph is responsible for managing the agent's state and execution loop.

Conceptually:

```text
                         ┌─────────────────┐
                         │   START / USER  │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │  Agent Decision │
                         └────────┬────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ↓                    ↓                    ↓
       Schema Tool           Query Tool          Clarification
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ↓
                         ┌─────────────────┐
                         │    Observe     │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │ Evidence Enough?│
                         └───────┬─────────┘
                              No │ Yes
                                 │
                      ┌──────────┘ └──────────┐
                      ↓                       ↓
                Agent Decision          Final Response
                      │                       │
                      └───────→───────────────┘
```

The graph should support cycles because an investigation may require multiple rounds of:

```text
decision → tool → observation → decision
```

---

# 6. Agent State

The LangGraph state should contain the information necessary for the agent to continue an investigation.

Suggested conceptual state:

```python
class AgentState(TypedDict):
    user_question: str

    mode: str

    database_context: dict

    messages: list

    current_goal: str

    clarification_required: bool
    clarification_question: str | None
    clarification_options: list[str]

    last_tool: str | None
    last_tool_result: dict | None

    investigation_history: list

    hypotheses: list

    evidence: list

    generated_sql: list

    query_results: list

    findings: list

    visualization_requests: list

    final_answer: str | None

    is_complete: bool
```

The exact schema can evolve during implementation.

---

# 7. Agent Modes

The application supports three primary modes.

## Ask

Optimized for straightforward questions.

```text
Question
 ↓
Understand
 ↓
Query
 ↓
Answer
```

---

## Investigate

Optimized for multi-step analysis.

```text
Question
 ↓
Understand
 ↓
Investigate
 ↓
Hypothesize
 ↓
Test
 ↓
Verify
 ↓
Answer
```

---

## Explore

Optimized for discovering interesting patterns.

```text
Database
 ↓
Understand available data
 ↓
Identify candidate metrics
 ↓
Explore patterns
 ↓
Validate findings
 ↓
Present interesting observations
```

---

# 8. Tool Architecture

Tools should be separated into logical groups.

```text
tools/
│
├── schema_tools.py
├── query_tools.py
├── analysis_tools.py
├── clarification_tools.py
└── visualization_tools.py
```

The LangGraph agent receives the tools through LangChain's tool interface.

Conceptually:

```python
tools = [
    inspect_database,
    inspect_table,
    inspect_relationships,
    generate_query,
    validate_sql,
    execute_query,
    analyze_results,
    compare_periods,
    ask_clarification,
    create_chart,
]
```

The LLM decides which tool to invoke.

---

# 9. Tool Execution Architecture

A tool call should follow:

```text
LLM
 ↓
LangChain Tool
 ↓
Tool Validation
 ↓
Service Layer
 ↓
Database / Analysis Function
 ↓
Structured Tool Result
 ↓
LangGraph State
 ↓
LLM
```

Tools should return structured data whenever possible.

Example:

```python
{
    "status": "success",
    "tool": "execute_query",
    "sql": "...",
    "columns": ["month", "revenue"],
    "rows": [...],
    "row_count": 12
}
```

Errors should also be structured:

```python
{
    "status": "error",
    "tool": "execute_query",
    "error_type": "sql_error",
    "message": "column revenue does not exist"
}
```

---

# 10. Database Architecture

```text
                SQLPilot
                   │
                   ▼
             SQLAlchemy
                   │
                   ▼
          Read-Only DB Session
                   │
                   ▼
              PostgreSQL
```

The database layer should provide:

- connection creation,
- connection testing,
- schema inspection,
- query execution,
- transaction handling,
- timeout handling,
- read-only enforcement.

The LLM should never receive unrestricted database credentials or a raw database connection object.

---

# 11. SQL Safety Layer

Before any generated SQL reaches PostgreSQL:

```text
Generated SQL
      ↓
SQL Safety Validator
      ↓
Parse / inspect statement
      ↓
Check operation
      ↓
Check limits
      ↓
Check timeout policy
      ↓
Approved?
   /       \
 No         Yes
 ↓           ↓
Reject     Execute
```

At minimum, block:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE
```

The first version should support read-only analytical SQL.

---

# 12. Evidence Architecture

Evidence is a first-class object in the application.

Conceptually:

```python
{
    "finding": "Revenue decreased significantly in September.",
    "evidence": [
        {
            "query_id": "q1",
            "purpose": "Monthly revenue comparison",
            "sql": "...",
            "result": {...}
        },
        {
            "query_id": "q2",
            "purpose": "Revenue by category",
            "sql": "...",
            "result": {...}
        }
    ]
}
```

This allows the UI to display:

```text
Finding
   ↓
Evidence
   ├── Query
   ├── Result
   └── Calculation
```

---

# 13. Hypothesis Architecture

For investigation tasks, hypotheses should be represented explicitly.

Example:

```python
{
    "id": "H2",
    "description": "Average order value decreased",
    "status": "supported",
    "evidence_ids": ["q4", "q5"],
    "confidence": "high"
}
```

Important distinction:

- `supported` means the available evidence supports the hypothesis.
- It does not mean the database has proven causal certainty.

The final answer should use cautious language where appropriate.

---

# 14. Visualization Flow

Charts are optional and should be generated when they improve comprehension.

```text
Agent finds useful numeric/time-series result
              ↓
Agent decides visualization is useful
              ↓
create_chart()
              ↓
Chart specification
              ↓
Plotly
              ↓
Streamlit
```

Examples:

### Time series

```text
Revenue by month
→ Line chart
```

### Category comparison

```text
Revenue by category
→ Bar chart
```

### Relationship

```text
Ad spend vs revenue
→ Scatter chart
```

Visualization should be based on actual query results, not invented values.

---

# 15. Streamlit Frontend Architecture

Suggested UI layout:

```text
┌──────────────────────────────────────────────────────────────┐
│ SQLPILOT                                    ● Connected      │
├───────────────────────┬──────────────────────────────────────┤
│                       │                                      │
│ DATABASE              │       ASK YOUR DATABASE              │
│                       │                                      │
│ PostgreSQL            │  [ Why did revenue decrease? ]       │
│ analytics             │                                      │
│                       │  [ Ask ] [ Investigate ] [ Explore ] │
│ Tables                │                                      │
│ ├─ customers          │                                      │
│ ├─ orders             │                                      │
│ ├─ products           │                                      │
│ └─ payments           │                                      │
│                       │                                      │
├───────────────────────┴──────────────────────────────────────┤
│ INVESTIGATION                                                │
│                                                              │
│ ✓ Understanding database                                    │
│ ✓ Checking monthly revenue                                  │
│ ● Comparing categories                                      │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ FINDINGS                                                     │
│                                                              │
│ Revenue decreased 27.4%                                      │
│                                                              │
│ [ Chart ]                                                    │
│                                                              │
│ Evidence                                                    │
│ [Query 1] [Query 2] [Query 3]                               │
│                                                              │
│ SQL                                                        │
│ [Expand SQL]                                                │
└──────────────────────────────────────────────────────────────┘
```

---

# 16. Frontend Components

Suggested Streamlit components:

```text
ui/
│
├── connection.py
├── query_input.py
├── mode_selector.py
├── investigation_status.py
├── clarification.py
├── findings.py
├── evidence.py
├── sql_viewer.py
├── charts.py
└── sidebar.py
```

Each UI component should focus on rendering state rather than implementing agent logic.

---

# 17. Application Layer

The application layer sits between Streamlit and LangGraph.

```text
Streamlit
    ↓
Application Controller
    ↓
LangGraph
```

Responsibilities:

- Receive user requests.
- Create agent state.
- Resume interrupted investigations.
- Handle clarification responses.
- Format final results for the UI.
- Maintain session-level context.

It should not contain the core SQL-generation logic.

---

# 18. Suggested Folder and File Structure

```text
sqlpilot/
│
├── app.py
│
├── config.py
├── requirements.txt
├── .env.example
├── README.md
│
├── agent/
│   ├── __init__.py
│   ├── graph.py
│   ├── state.py
│   ├── nodes.py
│   ├── router.py
│   ├── prompts.py
│   └── schemas.py
│
├── tools/
│   ├── __init__.py
│   ├── schema_tools.py
│   ├── query_tools.py
│   ├── analysis_tools.py
│   ├── clarification_tools.py
│   └── visualization_tools.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── schema_inspector.py
│   ├── executor.py
│   └── safety.py
│
├── analysis/
│   ├── __init__.py
│   ├── result_analyzer.py
│   ├── hypothesis.py
│   ├── evidence.py
│   └── metrics.py
│
├── visualization/
│   ├── __init__.py
│   ├── charts.py
│   └── chart_selector.py
│
├── ui/
│   ├── __init__.py
│   ├── connection.py
│   ├── sidebar.py
│   ├── query_input.py
│   ├── mode_selector.py
│   ├── investigation.py
│   ├── clarification.py
│   ├── findings.py
│   ├── evidence.py
│   └── sql_viewer.py
│
├── models/
│   ├── __init__.py
│   ├── llm.py
│   └── structured_outputs.py
│
├── tests/
│   ├── test_database.py
│   ├── test_tools.py
│   ├── test_sql_safety.py
│   ├── test_agent.py
│   └── test_analysis.py
│
└── logs/
    └── .gitkeep
```

---

# 19. File Responsibilities

## `app.py`

Main Streamlit entry point.

Responsibilities:

- Initialize UI.
- Initialize session state.
- Route user actions.
- Start/resume agent execution.
- Render results.

It should remain thin.

---

## `config.py`

Central configuration.

Examples:

```text
DATABASE_URL
MODEL_NAME
LLM_API_KEY
MAX_QUERY_ROWS
QUERY_TIMEOUT
MAX_AGENT_STEPS
```

Environment variables should be loaded through `.env`.

---

# 20. Agent Files

## `agent/state.py`

Defines the LangGraph state.

## `agent/graph.py`

Builds and compiles the LangGraph workflow.

## `agent/nodes.py`

Contains major agent node implementations.

Potential nodes:

```text
agent_decision
tool_execution
clarification
result_observation
final_response
```

## `agent/router.py`

Handles conditional routing.

Example decisions:

```text
→ tool
→ clarification
→ final_answer
→ retry
```

## `agent/prompts.py`

Contains system prompts and tool-selection instructions.

## `agent/schemas.py`

Contains structured Pydantic models for agent decisions and responses.

---

# 21. Tool Files

## `tools/schema_tools.py`

Database inspection tools.

## `tools/query_tools.py`

SQL generation, validation, and execution tools.

## `tools/analysis_tools.py`

Result analysis and comparison tools.

## `tools/clarification_tools.py`

Human clarification interaction.

## `tools/visualization_tools.py`

Chart generation requests.

---

# 22. Database Files

## `database/connection.py`

Creates SQLAlchemy engines and database sessions.

## `database/schema_inspector.py`

Handles deterministic schema inspection.

## `database/executor.py`

Executes approved SQL.

## `database/safety.py`

Validates SQL and enforces read-only policies.

---

# 23. Analysis Files

## `analysis/result_analyzer.py`

Contains deterministic or structured result-analysis helpers.

## `analysis/hypothesis.py`

Manages hypothesis creation and evaluation.

## `analysis/evidence.py`

Builds and stores evidence relationships.

## `analysis/metrics.py`

Reusable analytical calculations.

---

# 24. Visualization Files

## `visualization/charts.py`

Creates Plotly charts.

## `visualization/chart_selector.py`

Determines appropriate chart types from result structure.

Example:

```text
time series
→ line

category comparison
→ bar

two numeric variables
→ scatter
```

---

# 25. Model Architecture

LangChain should provide the model/tool abstraction.

Conceptually:

```text
                ┌─────────────────┐
                │   Chat Model    │
                └────────┬────────┘
                         │
                  LangChain Model
                         │
                         ▼
                Tool Calling Interface
                         │
                         ▼
                   LangGraph Agent
```

The specific model provider should remain configurable.

The architecture should avoid tightly coupling business logic to one LLM provider.

---

# 26. LangChain Responsibilities

Use LangChain for:

- Chat model abstraction.
- Tool definitions.
- Structured outputs.
- Prompt templates.
- Tool calling.
- Message handling.

LangChain should be the interface between the LLM and the application tools.

---

# 27. LangGraph Responsibilities

Use LangGraph for:

- Agent state.
- Graph construction.
- Conditional routing.
- Tool execution cycles.
- Human-in-the-loop clarification.
- Investigation loops.
- Persistence/checkpointing later if required.

The distinction is:

```text
LangChain
→ Model + Tools + Structured Interaction

LangGraph
→ Agent Workflow + State + Decisions + Loops
```

---

# 28. Python Responsibilities

Python is the primary application language.

Use Python for:

- Application logic.
- Database access.
- Tool implementations.
- SQL validation.
- Result processing.
- Agent state.
- Visualization.
- Testing.

---

# 29. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python | Main application language |
| Frontend | Streamlit | Web UI |
| Agent Framework | LangGraph | Agent orchestration and state |
| LLM Framework | LangChain | Models, tools, prompts, structured output |
| LLM | Configurable chat model | Reasoning and tool selection |
| Database | PostgreSQL | Relational data source |
| DB Access | SQLAlchemy | Database connection and execution |
| Validation | Pydantic | Structured state/output validation |
| Visualization | Plotly | Interactive charts |
| Configuration | python-dotenv | Environment configuration |
| Testing | pytest | Automated tests |
| Package Management | pip / venv | Python environment |

---

# 30. Dependencies

Initial dependency set:

```text
streamlit
langchain
langgraph
langchain-community
langchain-core
sqlalchemy
psycopg
pydantic
python-dotenv
plotly
pytest
```

Additional packages should only be introduced when a concrete requirement exists.

---

# 31. Runtime Flow

At runtime:

```text
                 ┌──────────────────┐
                 │    Streamlit     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Application      │
                 │ Controller       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ LangGraph Agent  │
                 └────────┬─────────┘
                          │
                    ┌─────┴─────┐
                    │           │
                    ▼           ▼
                 LLM       Tool Registry
                    │           │
                    └─────┬─────┘
                          ▼
                    Tool Execution
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Schema       PostgreSQL    Analysis
                          │
                          ▼
                       Results
                          │
                          ▼
                    LangGraph State
                          │
                          ▼
                     Agent Again
```

---

# 32. Example Investigation State

At the beginning:

```python
{
    "user_question": "Why did revenue decrease?",
    "mode": "investigate",
    "database_context": {},
    "investigation_history": [],
    "hypotheses": [],
    "evidence": [],
    "findings": [],
    "is_complete": False
}
```

After several tool calls:

```python
{
    "user_question": "Why did revenue decrease?",
    "mode": "investigate",

    "database_context": {
        "tables": ["orders", "products", "order_items"]
    },

    "investigation_history": [
        "inspect_database",
        "monthly_revenue",
        "revenue_by_category",
        "electronics_orders",
        "average_order_value"
    ],

    "hypotheses": [
        {
            "description": "Lower average order value contributed to the decline",
            "status": "supported"
        }
    ],

    "evidence": [
        "monthly revenue comparison",
        "category comparison",
        "order volume comparison",
        "AOV comparison"
    ],

    "findings": [
        "Revenue decreased",
        "Electronics was a major contributor",
        "Order volume remained relatively stable",
        "Average order value decreased"
    ],

    "is_complete": True
}
```

---

# 33. Error Handling

Every layer should return understandable errors.

## Database Error

```text
Database connection failed.
```

## SQL Error

```text
The generated query could not be executed.
The agent will attempt to repair it.
```

## Tool Error

```text
The requested analysis tool failed.
```

## LLM Error

```text
The AI model could not complete the current step.
```

The user should receive a useful message rather than a Python traceback.

Detailed tracebacks can be logged for development.

---

# 34. Agent Limits

To prevent runaway agent loops:

```text
MAX_AGENT_STEPS
MAX_SQL_REPAIR_ATTEMPTS
MAX_QUERY_ROWS
QUERY_TIMEOUT
MAX_CLARIFICATION_ROUNDS
```

Example initial values:

```text
MAX_AGENT_STEPS = 15
MAX_SQL_REPAIR_ATTEMPTS = 2
MAX_QUERY_ROWS = 500
QUERY_TIMEOUT = 30 seconds
MAX_CLARIFICATION_ROUNDS = 3
```

These are implementation defaults and should be configurable.

---

# 35. Security Architecture

Sensitive configuration belongs in environment variables.

Example:

```env
LLM_API_KEY=...
DATABASE_URL=...
```

Never commit secrets to Git.

The `.gitignore` should include:

```text
.env
.venv/
__pycache__/
*.pyc
logs/
```

Database credentials should never be included in prompts sent to the LLM.

---

# 36. Development Strategy

Build in this order.

## Phase 1 — Foundation

```text
Python project
+
Streamlit
+
PostgreSQL
+
SQLAlchemy
+
LangChain
+
LangGraph
```

Verify the basic database connection.

---

## Phase 2 — Schema Tools

Implement:

```text
inspect_database
inspect_table
inspect_relationships
```

Test them independently.

---

## Phase 3 — SQL Tools

Implement:

```text
generate_query
validate_sql
execute_query
```

Add read-only protection before execution.

---

## Phase 4 — Basic Agent

Build:

```text
User
 ↓
Agent
 ↓
Schema
 ↓
SQL
 ↓
Execution
 ↓
Answer
```

This establishes the minimum working agent.

---

## Phase 5 — Dynamic Investigation

Add the loop:

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
```

The agent should now decide whether another query is required.

---

## Phase 6 — Clarification

Add:

```text
Agent
 ↓
Clarification
 ↓
Human
 ↓
Agent resumes
```

---

## Phase 7 — Evidence

Track:

```text
Queries
Results
Findings
Hypotheses
```

Then expose the evidence trail in Streamlit.

---

## Phase 8 — Visualization

Add Plotly-based charts.

---

## Phase 9 — Explore Mode

Allow the agent to discover potentially interesting patterns.

---

# 37. Testing Strategy

Testing should exist at three levels.

## Unit Tests

Test deterministic functions:

```text
SQL safety
database utilities
result calculations
chart selection
schema parsing
```

## Tool Tests

Test:

```text
inspect_database()
execute_query()
analyze_results()
```

using a controlled test database.

## Agent Tests

Test scenarios such as:

```text
simple question
ambiguous question
complex investigation
missing data
SQL error
empty result
multi-step investigation
```

The agent should be evaluated on both correctness and whether it selects sensible actions.

---

# 38. Key Architecture Decision

The project should **not** become:

```text
User
 ↓
LLM 1
 ↓
LLM 2
 ↓
LLM 3
 ↓
SQL
```

unless a future requirement specifically justifies multiple specialized model calls.

The default architecture should be:

```text
User
 ↓
LangGraph Agent
 ↓
LLM decides
 ↓
Tool
 ↓
Observation
 ↓
LLM decides
 ↓
Tool
 ↓
Observation
 ↓
...
 ↓
Final Answer
```

This keeps the agent genuinely dynamic.

---

# 39. Final Architecture

```text
                             USER
                              │
                              ▼
                    ┌───────────────────┐
                    │    STREAMLIT      │
                    │      FRONTEND     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ APPLICATION LAYER │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │     LANGGRAPH     │
                    │      AGENT        │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    │     LANGCHAIN     │
                    │ Model + Tools     │
                    └─────────┬─────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
          Schema Tools   Query Tools   Analysis Tools
                │             │             │
                │             ▼             │
                │       SQL Safety          │
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                         SQLAlchemy
                              │
                              ▼
                       PostgreSQL
                              │
                              ▼
                           Results
                              │
                              ▼
                       Agent observes
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 Continue             Finish
                    │                   │
                    ▼                   ▼
               More tools       Evidence + Answer
                                        │
                              ┌─────────┴─────────┐
                              ▼                   ▼
                            SQL                 Charts
                              │                   │
                              └─────────┬─────────┘
                                        ▼
                                  STREAMLIT UI
```

---

# 40. Architecture Summary

SQLPilot is built around a **LangGraph-based autonomous investigation loop**.

The responsibilities are intentionally separated:

```text
Streamlit
→ User interaction

Python
→ Application and business logic

LangGraph
→ Agent state, decisions, routing, loops

LangChain
→ LLM abstraction, tools, prompts, structured output

Tools
→ Controlled capabilities available to the agent

SQLAlchemy
→ Database access

PostgreSQL
→ Source of truth

Analysis layer
→ Deterministic calculations and evidence handling

Plotly
→ Visualization
```

The central runtime pattern is:

```text
GOAL
 ↓
AGENT DECISION
 ↓
ACTION
 ↓
OBSERVATION
 ↓
AGENT DECISION
 ↓
ACTION
 ↓
OBSERVATION
 ↓
...
 ↓
EVIDENCE
 ↓
FINAL ANSWER
```

That loop is the architectural foundation of SQLPilot.
