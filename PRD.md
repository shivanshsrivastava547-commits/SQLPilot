# PRD: SQLPilot --- Agentic AI Data Analyst

## 1. Product Overview

### Product Name

**SQLPilot**

### Product Type

Agentic AI application for natural-language database analysis.

### One-Line Description

SQLPilot is an autonomous AI data analyst that connects to a relational
database, understands business questions in natural language,
investigates the data using SQL and analytical tools, resolves ambiguity
through interaction, verifies findings, and presents evidence-backed
answers and visualizations.

### Core Product Principle

> **The LLM should not follow a fixed pipeline. It should decide what
> information it needs, which tool to use, whether the result is
> sufficient, and what action to take next.**

The product is therefore not simply a Text-to-SQL converter. Text-to-SQL
is one capability inside a larger agentic investigation system.

------------------------------------------------------------------------

# 2. Problem Statement

Traditional Text-to-SQL systems work well for questions with an obvious
query structure, such as:

> "What were the top 10 products by sales last month?"

However, real users frequently ask higher-level business questions such
as:

-   "Why did revenue decrease?"
-   "What happened to sales last month?"
-   "Which customers are performing poorly?"
-   "What is unusual in our data?"
-   "Find something interesting in this database."

These questions cannot always be answered with one predetermined SQL
query.

The system must determine:

1.  What the user actually means.
2.  Which database tables and columns are relevant.
3.  Whether the question is ambiguous.
4.  Which query should be executed first.
5.  Whether the result is sufficient.
6.  What should be investigated next.
7.  Whether a hypothesis is supported by evidence.
8.  When enough evidence has been collected to answer.

SQLPilot addresses this problem by giving an LLM access to database
inspection, SQL execution, analytical, clarification, and visualization
tools.

------------------------------------------------------------------------

# 3. Target Users

## Primary Users

### 3.1 Business Analysts

People who need to investigate business data but do not want to manually
write SQL for every question.

Typical needs:

-   Explore business metrics.
-   Investigate changes.
-   Compare periods.
-   Find anomalies.
-   Generate evidence-backed explanations.

### 3.2 Data Analysts

Analysts who already understand databases but want an AI assistant to
accelerate exploratory analysis.

Typical needs:

-   Quickly generate exploratory queries.
-   Investigate hypotheses.
-   Inspect unfamiliar databases.
-   Reduce repetitive SQL work.
-   Automatically generate supporting visualizations.

### 3.3 Technical / Product Teams

Teams that need a natural-language interface over internal relational
databases.

Typical needs:

-   Self-service analytics.
-   Fast investigation of operational questions.
-   Database exploration without exposing raw database complexity to
    every user.

## Secondary Users

### 3.4 Students and Learners

Users who want to learn how business questions translate into SQL and
analytical investigations.

SQLPilot can expose:

-   Generated SQL.
-   Evidence.
-   Investigation steps.
-   Result interpretation.

------------------------------------------------------------------------

# 4. Product Goals

## Primary Goals

1.  Allow users to ask database questions using natural language.
2.  Enable the AI to inspect an unfamiliar relational database.
3.  Detect ambiguity instead of guessing.
4.  Ask users targeted clarification questions when required.
5.  Allow the agent to choose tools dynamically.
6.  Generate and execute SQL safely.
7.  Analyze query results.
8.  Perform multi-step investigations.
9.  Form and test hypotheses using database evidence.
10. Provide evidence for important conclusions.
11. Automatically create useful visualizations when appropriate.
12. Clearly communicate when the database does not contain enough
    information to answer a question.

## Secondary Goals

1.  Make the investigation process understandable to users.
2.  Make generated SQL inspectable.
3.  Make the system extensible through additional tools.
4.  Support both simple questions and complex investigations.
5.  Provide a foundation for future proactive database monitoring.

------------------------------------------------------------------------

# 5. Non-Goals

The initial version will NOT attempt to:

-   Modify production data.
-   Perform INSERT, UPDATE, DELETE, DROP, ALTER, or other destructive
    database operations.
-   Replace a professional data analyst.
-   Guarantee causal explanations from observational database data.
-   Invent missing tables, columns, relationships, or business facts.
-   Expose the model's private chain-of-thought.
-   Support every database engine from day one.
-   Automatically take business actions based on analytical findings.

The initial product focuses on **read-only investigation and
evidence-backed analysis**.

------------------------------------------------------------------------

# 6. Core User Experience

A user connects a PostgreSQL database.

They can then enter a natural-language question.

Example:

> "Why did revenue fall in September?"

The agent should:

``` text
User Question
     ↓
Understand Goal
     ↓
Inspect Database
     ↓
Determine Relevant Data
     ↓
Ask Clarification if Necessary
     ↓
Generate Initial Query
     ↓
Execute Query
     ↓
Analyze Results
     ↓
Determine Whether Evidence Is Sufficient
     ↓
If Not:
    Investigate Further
     ↓
Verify Findings
     ↓
Generate Final Answer
     ↓
Show Evidence + SQL + Visualization
```

The sequence is dynamic. The agent decides which step is necessary next.

------------------------------------------------------------------------

# 7. Core Product Modes

## 7.1 Ask Mode

Designed for straightforward questions.

Example:

> "What were our top 10 products last month?"

Expected behavior:

``` text
Understand question
      ↓
Identify relevant tables
      ↓
Generate SQL
      ↓
Execute SQL
      ↓
Return result
```

Output should include:

-   Direct answer.
-   Relevant result table.
-   Generated SQL.
-   Optional visualization.

------------------------------------------------------------------------

## 7.2 Investigate Mode

Designed for complex business questions.

Example:

> "Why did revenue decrease?"

The agent may:

1.  Inspect the database.
2.  Establish a meaningful comparison period.
3.  Query revenue over time.
4.  Identify the size of the change.
5.  Investigate categories.
6.  Investigate regions.
7.  Compare order count.
8.  Compare average order value.
9.  Form hypotheses.
10. Test those hypotheses.
11. Verify the strongest findings.
12. Produce an evidence-backed conclusion.

This is the primary demonstration of the product's agentic behavior.

------------------------------------------------------------------------

## 7.3 Explore Mode

Designed for open-ended database discovery.

Example:

> "Explore this database and tell me something interesting."

The agent should:

1.  Understand available tables and relationships.
2.  Identify useful metrics.
3.  Search for notable trends, differences, or anomalies.
4.  Validate potentially interesting findings.
5.  Present selected findings with supporting evidence.

The system should avoid presenting random statistical noise as
meaningful insight.

------------------------------------------------------------------------

# 8. Agent Capabilities

## 8.1 Database Understanding

The agent must be able to inspect an unfamiliar database.

Required capabilities:

-   Discover tables.
-   Inspect table columns.
-   Identify primary keys.
-   Identify foreign keys.
-   Identify relationships.
-   Inspect relevant column metadata.
-   Understand available data types.

Example tools:

``` text
inspect_database()
inspect_table(table_name)
inspect_relationships()
```

------------------------------------------------------------------------

## 8.2 Ambiguity Detection

The agent should detect ambiguous terms instead of silently guessing.

Example:

> "Show me our best customers."

Possible meanings:

-   Highest total spending.
-   Most orders.
-   Highest average order value.
-   Most recent purchases.

The system should ask a targeted clarification question when the
ambiguity materially affects the result.

------------------------------------------------------------------------

## 8.3 Clarification

The agent can ask the user for missing information.

Clarification should be:

-   Specific.
-   Minimal.
-   Relevant to the query.
-   Based on the available schema and data.
-   Avoidable when the intent is already sufficiently clear.

Example:

``` text
How should "best customers" be defined?

○ Highest total spending
○ Most orders
○ Highest average order value
○ Most recent purchases
```

The user response becomes part of the agent's working context.

------------------------------------------------------------------------

# 9. Agent Toolset

The initial version should provide a small, focused toolbox.

## Database Tools

### `inspect_database()`

Purpose:

-   Discover database structure.
-   Return tables and high-level metadata.

### `inspect_table(table_name)`

Purpose:

-   Inspect columns and metadata for a specific table.

### `inspect_relationships()`

Purpose:

-   Identify relationships between tables.

------------------------------------------------------------------------

## Query Tools

### `generate_query()`

Purpose:

-   Generate SQL based on the current investigation objective and known
    schema.

### `execute_query(sql)`

Purpose:

-   Execute a validated read-only SQL query.

------------------------------------------------------------------------

## Analysis Tools

### `analyze_results()`

Purpose:

-   Analyze returned query results.
-   Identify meaningful patterns.
-   Determine whether further investigation may be required.

### `compare_periods()`

Purpose:

-   Compare relevant time periods or groups.

------------------------------------------------------------------------

## Interaction Tool

### `ask_clarification(question, options)`

Purpose:

-   Ask the user for information required to continue reliably.

------------------------------------------------------------------------

## Visualization Tool

### `create_chart(data, chart_type)`

Purpose:

-   Produce a useful visualization when a chart improves understanding.

------------------------------------------------------------------------

# 10. Agent Decision Loop

The central agent loop is:

``` text
                  ┌───────────────┐
                  │     Goal      │
                  │ Answer user   │
                  │   question    │
                  └───────┬───────┘
                          ↓
                  ┌───────────────┐
                  │     Agent     │
                  │               │
                  │ Understand    │
                  │ Decide        │
                  │ Act           │
                  │ Observe       │
                  └───────┬───────┘
                          ↓
             ┌────────────┼────────────┐
             ↓            ↓            ↓
        Inspect DB     Run SQL     Ask User
             │            │            │
             └────────────┼────────────┘
                          ↓
                    Observe Result
                          ↓
                  Is evidence enough?
                     /          \
                   No            Yes
                   ↓              ↓
              Investigate       Answer
                   │              │
                   └──────→───────┘
```

The agent should be able to choose a different next action based on the
result of each previous action.

------------------------------------------------------------------------

# 11. Investigation and Hypothesis Testing

This is a major differentiating feature.

For a question such as:

> "Why did sales decline?"

The agent may identify possible explanations:

``` text
H1: Fewer orders
H2: Lower average order value
H3: Certain product categories declined
H4: Certain regions declined
H5: Customer activity declined
```

The agent then gathers evidence for each hypothesis.

Example:

``` text
H1
Orders decreased 2%
→ Does not explain most of the decline.

H2
Average order value decreased 23%
→ Potentially significant.

H3
Electronics revenue decreased 47%
→ Potentially significant.

H4
No major regional anomaly.
→ Less likely to explain the decline.
```

The final answer should distinguish:

-   Observed facts.
-   Calculated metrics.
-   Supported explanations.
-   Unverified possibilities.

The system must not present correlation as proven causation.

------------------------------------------------------------------------

# 12. Evidence Trail

Every important conclusion should be traceable to evidence.

Example:

``` text
Finding:
Revenue decreased 27.4%.

Evidence:
├── Query #1
│   Monthly revenue comparison
│
├── Query #2
│   Revenue by category
│
├── Query #3
│   Electronics order volume
│
└── Query #4
    Average order value
```

The interface should allow the user to inspect:

-   SQL query.
-   Query result.
-   Relevant calculation.
-   Which finding the query supports.

This is a core reliability feature.

------------------------------------------------------------------------

# 13. Answer Format

A final answer should generally contain:

## Summary

A concise answer to the user's question.

## Key Findings

Important observations from the investigation.

## Evidence

The queries and data supporting the findings.

## Visualization

A chart when it materially improves understanding.

## SQL

The relevant SQL queries, available for inspection.

## Limitations

Any important uncertainty or missing data.

Example:

``` text
Revenue decreased 27.4% in September compared
with August.

Key findings:
- Electronics revenue fell substantially.
- Order volume changed only slightly.
- Average order value decreased significantly.

Evidence:
[View Query 1]
[View Query 2]
[View Query 3]

[Revenue Trend Chart]

Limitation:
The database does not contain marketing campaign
attribution data, so campaign-level explanations
cannot be evaluated.
```

------------------------------------------------------------------------

# 14. Handling Missing Information

If the database does not contain information required to answer a
question, the agent must explicitly say so.

Example user question:

> "Which marketing campaign generated the most revenue?"

If the database contains:

``` text
customers
orders
products
payments
```

but no campaign or marketing-attribution information, the system should
respond:

> "I can't answer this from the connected database because it does not
> contain campaign or marketing-attribution data."

The agent must never fabricate:

-   Tables.
-   Columns.
-   Relationships.
-   Business facts.
-   Query results.

------------------------------------------------------------------------

# 15. Safety and Database Protection

The initial product should operate in read-only mode.

## Required protections

-   Read-only database connection.
-   Block destructive SQL.
-   Query timeout.
-   Result-size limits.
-   SQL validation before execution.
-   Clear error handling.
-   No unrestricted arbitrary tool execution.

Blocked operations should include at minimum:

``` text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
```

The exact implementation may depend on the database engine and
connection configuration.

------------------------------------------------------------------------

# 16. User Interface Requirements

The interface should communicate that the system is an AI analyst, not a
simple chatbot.

## Main Screen

The main interface should contain:

### Database Status

``` text
● PostgreSQL Connected
```

### Query Input

``` text
Ask your database

[ Why did revenue decrease last month? ]

[ Ask ] [ Investigate ]
```

### Investigation Panel

Show high-level agent activity:

``` text
✓ Understanding database
✓ Checking monthly revenue
✓ Comparing categories
● Investigating average order value
```

Do not expose private chain-of-thought.

Only expose meaningful high-level actions.

### Findings Panel

Display:

-   Main finding.
-   Supporting metrics.
-   Chart.
-   Evidence links.
-   SQL.

------------------------------------------------------------------------

# 17. Technical Architecture

Initial architecture:

``` text
                    ┌─────────────────┐
                    │   Streamlit UI  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   Agent Layer   │
                    │    LangGraph    │
                    └────────┬────────┘
                             ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
        Schema Tools    Query Tools    Analysis Tools
              │              │              │
              └──────────────┼──────────────┘
                             ↓
                       PostgreSQL
                             ↓
                          Results
                             ↓
                       Agent Analysis
                             ↓
                   Evidence-backed Answer
```

------------------------------------------------------------------------

# 18. Initial Technology Stack

## Frontend

**Streamlit**

Purpose:

-   Fast development.
-   Database connection interface.
-   Query interface.
-   Investigation visualization.
-   Evidence display.

## Agent Orchestration

**LangGraph**

Purpose:

-   Agent state.
-   Tool calling.
-   Conditional routing.
-   Iterative investigation.
-   Human clarification.
-   Multi-step workflows.

## LLM

The implementation should support a capable tool-calling/chat model.

Possible providers include:

-   OpenAI.
-   Gemini.
-   Claude.
-   Compatible open-source models.

The specific model should remain configurable.

## Database

**PostgreSQL**

The first implementation should target PostgreSQL before expanding to
other relational databases.

## Database Access

**SQLAlchemy**

## Visualization

**Plotly**

------------------------------------------------------------------------

# 19. Suggested Project Structure

``` text
sqlpilot/
│
├── app/
│   ├── ui/
│   └── components/
│
├── agent/
│   ├── graph.py
│   ├── state.py
│   ├── prompts.py
│   └── decisions.py
│
├── tools/
│   ├── schema_tools.py
│   ├── query_tools.py
│   ├── analysis_tools.py
│   ├── clarification_tools.py
│   └── visualization_tools.py
│
├── database/
│   ├── connection.py
│   ├── schema.py
│   └── safety.py
│
├── analysis/
│   ├── result_analyzer.py
│   ├── hypothesis.py
│   └── evidence.py
│
├── visualization/
│   └── charts.py
│
├── tests/
│
├── config.py
├── requirements.txt
└── README.md
```

The exact structure can evolve during implementation.

------------------------------------------------------------------------

# 20. MVP Scope

The first working version should include only the following.

## Required

-   PostgreSQL connection.
-   Schema inspection.
-   Natural-language question input.
-   Agent orchestration.
-   Tool selection.
-   Clarification handling.
-   SQL generation.
-   SQL validation.
-   Read-only SQL execution.
-   Result analysis.
-   Multi-step investigation.
-   Final answer generation.
-   SQL visibility.
-   Evidence trail.

## Nice to Have

-   Automatic charts.
-   Hypothesis testing UI.
-   Investigation timeline.
-   Explore mode.

## Post-MVP

-   Data quality investigation.
-   Proactive insights.
-   Scheduled monitoring.
-   Multiple database engines.
-   Persistent user workspaces.
-   Historical investigations.

------------------------------------------------------------------------

# 21. Success Criteria

The MVP should satisfy the following.

### SC-01: Simple Question

Given:

> "What were the top 10 products by revenue last month?"

The agent should produce a correct answer using the database.

### SC-02: Ambiguous Question

Given:

> "Show me the best customers."

The agent should identify that "best" is ambiguous when the schema does
not provide a uniquely implied definition and ask for clarification.

### SC-03: Multi-Step Investigation

Given:

> "Why did revenue decrease?"

The agent should perform multiple relevant queries instead of stopping
after one query.

### SC-04: Result-Driven Decisions

The next agent action should be influenced by the previous query result.

### SC-05: Missing Data

Given a question requiring unavailable data, the agent should clearly
state that the database cannot answer it.

### SC-06: Evidence

Major conclusions should have supporting queries and results.

### SC-07: Safety

The system must prevent destructive SQL operations.

### SC-08: No Fabrication

The system must not invent database structures or results.

------------------------------------------------------------------------

# 22. Example End-to-End Scenario

## User

> Why did revenue fall in September?

## Agent

### Action 1

Inspect database.

Finds:

``` text
orders
order_items
products
customers
```

### Action 2

Determine how revenue can be calculated.

### Action 3

Query monthly revenue.

Result:

``` text
July       ₹80L
August     ₹84L
September  ₹61L
```

### Agent Decision

September revenue clearly decreased.

Continue investigating.

### Action 4

Query revenue by category.

Result:

``` text
Electronics     -46.9%
Clothing        -3.2%
Home            +1.4%
```

### Agent Decision

Electronics is a major contributor.

### Action 5

Compare Electronics order volume.

Result:

``` text
August       4,200
September    4,100
```

### Agent Decision

Order volume did not fall enough to explain the revenue decline.

### Action 6

Compare average order value.

Result:

``` text
August       ₹7,620
September    ₹4,146
```

### Agent Decision

Lower average order value is a significant factor.

### Final Answer

The agent reports:

-   Overall revenue change.
-   Major contributing category.
-   Order-volume comparison.
-   Average-order-value comparison.
-   Supporting SQL.
-   Relevant chart.
-   Any limitations.

------------------------------------------------------------------------

# 23. Future Roadmap

## Phase 1 --- Core Agent

-   Database connection.
-   Schema understanding.
-   Tool calling.
-   Text-to-SQL.
-   Clarification.
-   SQL execution.
-   Result analysis.

## Phase 2 --- Investigation

-   Multi-step investigations.
-   Hypothesis generation.
-   Hypothesis testing.
-   Evidence tracking.

## Phase 3 --- Visualization

-   Automatic chart selection.
-   Interactive charts.
-   Result exploration.

## Phase 4 --- Data Intelligence

-   Data quality investigation.
-   Anomaly detection.
-   Pattern discovery.
-   Database health reports.

## Phase 5 --- Proactive Agent

-   Scheduled database checks.
-   Change detection.
-   Alerting.
-   Recurring reports.

------------------------------------------------------------------------

# 24. Product Differentiation

SQLPilot should not be positioned as:

> "An AI that converts English into SQL."

Its core value proposition is:

> **"An AI analyst that investigates your database to answer business
> questions."**

The distinction is:

``` text
Traditional Text-to-SQL

Question
   ↓
SQL
   ↓
Answer
```

versus:

``` text
SQLPilot

Business Question
       ↓
Understand
       ↓
Inspect
       ↓
Plan
       ↓
Query
       ↓
Observe
       ↓
Investigate
       ↓
Verify
       ↓
Evidence
       ↓
Answer
```

The second workflow is the core product.

------------------------------------------------------------------------

# 25. Final Product Definition

> **SQLPilot is an agentic AI data analyst for relational databases. It
> allows users to ask business questions in natural language and
> autonomously investigates the connected data using dynamically
> selected tools. The agent can inspect the database, resolve ambiguity,
> generate and execute safe SQL, analyze results, formulate and test
> hypotheses, continue investigating when evidence is insufficient, and
> present evidence-backed answers with SQL and visualizations.**

The most important requirement is that the agent's behavior is **dynamic
and result-driven**.

It should not simply execute a predetermined chain of steps.

It should continuously answer:

> **"Given the user's goal and what I have learned so far, what should I
> do next?"**
