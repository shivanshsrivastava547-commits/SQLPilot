# SQLPilot Coding Agent Memory

## Purpose

This file is the persistent working memory for the coding agent building **SQLPilot: An Agentic AI Data Analyst**.

The coding agent MUST use this file to remember the project's current implementation state between sessions.

This file is not a replacement for the project documentation:

- `PRD.md` = what the product should do
- `architecture.md` = how the system is architected
- `rules.md` = engineering and behavioral boundaries
- `phase.md` = implementation order and phases
- `design.md` = frontend and UI design requirements
- `memory.md` = current implementation progress and working context

The agent should read the relevant documentation before making changes.

---

# 1. Memory Rules

## 1.1 Read memory before coding

At the beginning of every coding session:

1. Read `memory.md`.
2. Identify the current phase.
3. Read the relevant section of `phase.md`.
4. Read any relevant sections of `PRD.md`, `architecture.md`, `rules.md`, and `design.md`.
5. Inspect the actual repository before assuming that the remembered state is still correct.

Memory is a guide to the previous session, not absolute truth.

The actual repository and tests are the source of truth for implementation state.

---

## 1.2 Update memory after meaningful work

The coding agent MUST update this file after meaningful implementation progress.

Examples:

- A phase is completed.
- A feature is implemented.
- A major architectural decision is made.
- A bug is discovered.
- A bug is fixed.
- A dependency is added or removed.
- A database integration changes.
- A tool is added, removed, or redesigned.
- An agent node or graph flow changes.
- A UI component is completed.
- Tests are added or significantly changed.
- A known limitation is discovered.
- The next implementation step becomes clear.

Do not update memory for every tiny edit.

---

## 1.3 Never fabricate progress

Only record work that actually exists in the repository.

Do NOT write:

- "Implemented" when the code only exists in a plan.
- "Tests passing" when tests were not run.
- "Database connected" when connection was not verified.
- "Phase complete" when the completion criteria have not been met.

Use explicit states such as:

- `PLANNED`
- `IN PROGRESS`
- `BLOCKED`
- `COMPLETED`
- `PARTIALLY COMPLETED`
- `NOT STARTED`

---

# 2. Current Project State

## Project

**SQLPilot: An Agentic AI Data Analyst**

## Core purpose

SQLPilot connects to a relational database and allows users to ask business questions in natural language.

The system should behave like a junior data analyst rather than merely translating natural language into SQL.

Core loop:

```text
User Question
    ↓
Understand
    ↓
Investigate
    ↓
Use Tools
    ↓
Execute SQL
    ↓
Observe Results
    ↓
Decide What To Do Next
    ↓
Investigate Further If Needed
    ↓
Verify Findings
    ↓
Answer
    ↓
Evidence + SQL + Charts
```

The agent should not be forced through a rigid fixed pipeline.

The LLM should decide what information it needs, which tool to use, whether more investigation is required, whether clarification is necessary, and when there is enough evidence to answer.

---

# 3. Current Phase

Update this section whenever the active implementation phase changes.

```text
Current Phase:
Status:
Started:
Last Updated:
```

### Current Phase Notes

```text
Describe exactly what is currently being built.
```

---

# 4. Completed Phases

Maintain a concise record of completed phases.

Format:

```text
## Phase X — Name

Status: COMPLETED

Completed:
- ...
- ...
- ...

Verification:
- ...
- ...

Date:
```

Do not mark a phase completed until its completion criteria from `phase.md` have been satisfied.

---

# 5. Current Implementation

Record what actually exists in the repository.

## Backend

```text
Implemented:
- ...

Partially implemented:
- ...

Not implemented:
- ...
```

## Agent

```text
Graph:
- ...

Nodes:
- ...

State:
- ...

Routing:
- ...

Tool calling:
- ...

Clarification:
- ...

Investigation:
- ...

Evidence:
- ...
```

## Database

```text
Database:
Connection:
ORM / access layer:
Schema inspection:
Query execution:
SQL safety:
Read-only enforcement:
```

## Tools

Maintain the actual tool inventory.

| Tool | Status | Purpose | Notes |
|---|---|---|---|
| `inspect_database()` | | | |
| `inspect_table()` | | | |
| `inspect_relationships()` | | | |
| `generate_query()` | | | |
| `execute_query()` | | | |
| `analyze_results()` | | | |
| `compare_periods()` | | | |
| `ask_clarification()` | | | |
| `create_chart()` | | | |

Only list a tool as implemented when it actually exists and works.

## Frontend

```text
Framework:
Main app:
Pages / views:
Components:
State management:
Current UI status:
```

## Visualization

```text
Chart library:
Implemented chart types:
Automatic chart selection:
Current limitations:
```

---

# 6. Recent Changes

Record the most recent meaningful changes.

Use newest entries first.

Format:

```text
## YYYY-MM-DD

Changed:
- ...

Reason:
- ...

Files:
- ...

Verification:
- ...

Result:
- ...
```

Keep this section concise.

---

# 7. Current Task

This section describes what the agent is currently working on.

```text
Task:
Status:
Goal:
Files being modified:
Expected result:
```

When the task is completed, move the important result into the appropriate implementation section and add an entry to `Recent Changes`.

---

# 8. Next Task

Record the next concrete implementation step.

```text
Next task:
Why:
Relevant phase:
Expected files:
Acceptance criteria:
```

The next task should be small enough that a coding agent can start working on it immediately.

Do not write vague items such as:

```text
Improve the application.
```

Prefer:

```text
Implement the SQL safety validator and add tests for SELECT-only enforcement.
```

---

# 9. Known Problems

Record unresolved technical problems.

Format:

```text
## Problem

Status: BLOCKED / INVESTIGATING / KNOWN LIMITATION

Symptom:
...

Likely cause:
...

What has been tried:
...

Next investigation:
...

Affected files:
...
```

Do not repeatedly attempt the same failed approach without recording what happened.

---

# 10. Decisions Log

Record important architectural or implementation decisions so future sessions do not accidentally reverse them.

Format:

```text
## Decision: <short title>

Date:
Decision:
Reason:
Alternatives considered:
Impact:
```

Examples of decisions worth recording:

- Why LangGraph is used for orchestration.
- Why SQLAlchemy is used for database access.
- Why the database is read-only.
- Why tools are separated by responsibility.
- Why evidence is stored as structured data.
- Why hidden chain-of-thought is not exposed.
- Why Streamlit is used for the frontend.
- Why a particular LLM interface was selected.

Do not record trivial coding choices.

---

# 11. Important Repository Facts

Record facts that future coding sessions need to know.

Examples:

```text
Python version:
Package manager:
Virtual environment:
Entry point:
Test command:
Run command:
Environment variable names:
Database configuration:
Important directories:
```

Never store secret values here.

NEVER store:

- API keys
- passwords
- database credentials
- access tokens
- private keys
- session tokens

Store only variable names and configuration structure.

---

# 12. Dependencies

Track meaningful dependency changes.

Format:

```text
Added:
- package
- reason

Removed:
- package
- reason

Changed:
- package
- version/reason
```

Avoid duplicating the complete `requirements.txt` here.

---

# 13. Testing State

Record the current testing situation.

```text
Test command:

Total tests:
Passing:
Failing:
Skipped:

Last verification:

Known failing tests:
- ...

Untested areas:
- ...
```

Never claim tests pass unless they were actually executed.

---

# 14. UI / Design State

Because `design.md` defines the frontend rules, this section should only record implementation progress.

```text
Completed UI:
- ...

In progress:
- ...

Remaining:
- ...

Known UI issues:
- ...
```

Do not copy the entire design specification into this file.

---

# 15. Agent Behavior State

Track important behavior that has actually been implemented.

```text
Can inspect schema:
Can inspect relationships:
Can generate SQL:
Can execute SQL:
Can inspect results:
Can decide next action:
Can ask clarification:
Can perform investigation:
Can maintain evidence:
Can create charts:
Can produce final answer:
```

Use:

```text
YES
PARTIAL
NO
```

and add a short note when necessary.

---

# 16. MVP Status

Track the MVP requirements from `PRD.md` and `phase.md`.

| Capability | Status | Notes |
|---|---|---|
| PostgreSQL connection | | |
| Schema understanding | | |
| Ambiguity detection | | |
| Clarification | | |
| Tool selection | | |
| SQL generation | | |
| SQL safety | | |
| SQL execution | | |
| Result inspection | | |
| Additional investigation | | |
| Final answer | | |
| Evidence trail | | |
| Basic visualization | | |

The MVP is complete only when the relevant acceptance criteria in `phase.md` are complete.

---

# 17. Session Handoff

At the end of every meaningful coding session, update this section so another coding session can continue without reconstructing the entire history.

Use this exact structure:

```text
## Last Session

Date:

What was being built:
- ...

What was completed:
- ...

What is currently working:
- ...

What is not working:
- ...

Important discovery:
- ...

Files changed:
- ...

Tests run:
- ...

Test result:
- ...

Current phase:
- ...

Next action:
- ...

Warnings:
- ...
```

The next coding session should read this section first after reading the overall memory.

---

# 18. Memory Maintenance Rules

The memory file must remain useful.

## Keep it concise

Do not turn this file into a diary.

Bad:

```text
At 3:17 PM I opened the file and changed line 42...
```

Good:

```text
Implemented read-only SQL validation and added SELECT/CTE tests.
```

## Remove stale information

When a temporary problem is fixed, update or remove it.

Do not allow outdated information to mislead future sessions.

## Preserve important history

Do not delete architectural decisions or important discoveries merely to make the file shorter.

## Prefer current state over historical narration

The purpose is to answer:

> "Where is the project now, what works, what doesn't, and what should I do next?"

---

# 19. Conflict Resolution

If information conflicts:

1. Actual repository code is the implementation source of truth.
2. Passing tests are stronger evidence than memory claims.
3. `phase.md` defines the intended development order.
4. `architecture.md` defines intended architecture.
5. `rules.md` defines mandatory boundaries.
6. `design.md` defines frontend/UI requirements.
7. `PRD.md` defines product requirements.
8. `memory.md` records the latest known implementation state.

If the repository differs from the documentation:

- Do not silently rewrite architecture.
- Determine whether the difference is intentional.
- Record the discrepancy.
- Update documentation when the architecture has genuinely changed.

---

# 20. Coding Agent Session Protocol

Every coding session should follow this process:

```text
START
  ↓
Read memory.md
  ↓
Read phase.md
  ↓
Identify current phase
  ↓
Read relevant project documentation
  ↓
Inspect repository
  ↓
Compare repository state with memory
  ↓
Choose one concrete task
  ↓
Implement
  ↓
Run tests / verification
  ↓
Fix failures
  ↓
Verify again
  ↓
Update memory.md
  ↓
Report what changed
  ↓
STOP
```

Do not skip repository inspection simply because memory says something is implemented.

---

# 21. Important Rule For Autonomous Coding

The coding agent may make implementation decisions within the boundaries of:

- `PRD.md`
- `architecture.md`
- `rules.md`
- `phase.md`
- `design.md`

But when an implementation decision materially changes the architecture, product behavior, security model, database behavior, or agent behavior:

1. Record the decision in `Decisions Log`.
2. Update the relevant project documentation if necessary.
3. Update `memory.md`.
4. Continue only after ensuring the repository remains coherent.

The agent should not silently evolve the project into a different product.

---

# 22. Final Principle

This file exists so that every coding session starts with context instead of forcing the agent to rediscover the project from scratch.

The goal is not to remember every action.

The goal is to remember:

```text
WHERE WE ARE
WHAT WORKS
WHAT DOESN'T
WHAT WE DECIDED
WHAT CHANGED
WHAT COMES NEXT
```

The coding agent should leave the repository in a state where another session can continue the work with minimal reconstruction.
