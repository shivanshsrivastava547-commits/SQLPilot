# SQLPilot Frontend & UI Design Specification

## 1. Purpose

This document defines the visual design, interaction design, layout rules, component behavior, and frontend implementation standards for **SQLPilot: An Agentic Data Analyst**.

The frontend must communicate that SQLPilot is an **AI data analyst**, not a simple Text-to-SQL form.

The interface should make the agent's work understandable without exposing private chain-of-thought. Users should be able to see:

- what the agent is doing at a high level
- what it found
- which evidence supports a finding
- the SQL used
- charts and analytical results
- when user clarification is required
- whether the agent is still investigating or has completed the task

The project specification explicitly calls for an intelligent interface that shows investigation activity, findings, SQL, evidence, and charts rather than a plain input-and-submit screen.

---

# 2. Design Goals

The UI should be:

1. **Professional**
   - It should look like a modern analytics product.
   - Avoid the appearance of a college demo or generic chatbot.

2. **Minimal**
   - Show important information first.
   - Hide implementation details until the user asks to inspect them.

3. **Analytical**
   - Prioritize findings, metrics, comparisons, charts, and evidence.

4. **Transparent**
   - Make conclusions traceable to database evidence.
   - Never imply that an unsupported conclusion came from the database.

5. **Agentic**
   - The UI should visibly communicate that the agent investigates dynamically.
   - Do not present the experience as a fixed wizard with predetermined steps.

6. **Interactive**
   - Users should be able to inspect SQL, evidence, charts, investigation activity, and clarification options.

7. **Responsive within Streamlit**
   - Use Streamlit-native components where possible.
   - Avoid unnecessary frontend complexity.

8. **Consistent**
   - Components should follow one visual language across Ask, Investigate, and Explore modes.

---

# 3. Core Design Principle

## The UI should represent the agent's work, not the agent's hidden reasoning.

The agent can internally decide:

```text
inspect_database
→ execute_query
→ analyze_results
→ investigate_category
→ compare_periods
→ execute_query
→ final_answer
```

The user-facing interface should instead communicate this at a useful level:

```text
✓ Understanding database
✓ Checking monthly revenue
✓ Comparing categories
● Investigating average order value
```

Do not display private chain-of-thought, hidden reasoning tokens, or internal model deliberation.

Display **actions, evidence, results, and conclusions**.

---

# 4. Overall Visual Direction

SQLPilot should feel like a modern data/AI workspace.

### Visual characteristics

- clean
- restrained
- premium
- analytical
- calm
- high information density without visual clutter
- strong typography hierarchy
- subtle borders
- restrained use of color
- generous spacing
- clear cards
- strong alignment

Avoid:

- excessive gradients
- excessive rounded cards
- giant colorful icons
- cartoon illustrations
- excessive animations
- emoji-heavy interfaces
- neon "AI" aesthetics
- dashboard clutter
- unnecessary glassmorphism
- huge hero sections
- excessive shadows

The product should look like software used by analysts, engineers, and business teams.

---

# 5. Application Layout

Use a persistent application shell.

Recommended structure:

```text
┌──────────────────────────────────────────────────────────────┐
│ SQLPILOT                                      ● Connected     │
├───────────────┬──────────────────────────────────────────────┤
│               │                                              │
│  WORKSPACE    │              MAIN WORKSPACE                  │
│               │                                              │
│  Database     │                                              │
│  Mode         │                                              │
│  History      │                                              │
│               │                                              │
│               │                                              │
│               │                                              │
├───────────────┴──────────────────────────────────────────────┤
│ Status / connection information                              │
└──────────────────────────────────────────────────────────────┘
```

The exact implementation may use Streamlit's sidebar rather than a custom left navigation panel.

---

# 6. Header

The header should remain visually simple.

Recommended:

```text
SQLPILOT
AI DATA ANALYST

                         PostgreSQL
                         ● Connected
```

### Header responsibilities

Show:

- product name
- current database connection status
- optional database name
- optional current mode

Do not put too many controls in the header.

### Connection status

Use clear states:

```text
● Connected
● Connecting
● Disconnected
⚠ Connection error
```

Use color sparingly and always combine color with text.

Never communicate status through color alone.

---

# 7. Sidebar

The sidebar should contain persistent workspace controls.

Recommended structure:

```text
SQLPILOT

WORKSPACE

Database
  PostgreSQL
  ecommerce_pipeline
  ● Connected

MODE

  Ask
  Investigate
  Explore

────────────────────

RECENT QUESTIONS

  Why did revenue fall?
  Top products
  Monthly sales

────────────────────

SETTINGS
  Model
  Query limits
  Display
```

Not every item has to be implemented in the MVP.

The sidebar should remain secondary to the investigation workspace.

---

# 8. Main Query Area

The query area is the primary interaction point.

Use a large, comfortable text area rather than a tiny text input.

Example:

```text
Ask your database
────────────────────────────────────────────────────────

Why did revenue decrease in September?

                                          [ Investigate ]
```

The input should support natural business questions.

Placeholder examples:

```text
Ask a question about your data...
```

or:

```text
Try:
"Why did revenue decrease last month?"
```

Avoid making the interface look like a SQL editor.

The user should not need to know SQL.

---

# 9. Mode Selector

SQLPilot has three modes:

- Ask
- Investigate
- Explore

The project specification defines these as distinct experiences.

## Ask

For straightforward questions.

UI description:

```text
Ask
Quick answers to direct questions.
```

Example:

```text
"What were our top 10 products last month?"
```

Expected visual flow:

```text
Question
↓
Answer
↓
Supporting SQL / evidence
```

## Investigate

The primary showcase mode.

UI description:

```text
Investigate
Explore complex questions and explain why something happened.
```

Example:

```text
"Why did revenue decrease?"
```

Show investigation progress and findings.

## Explore

For discovering interesting patterns.

UI description:

```text
Explore
Find notable patterns and unusual changes in your database.
```

The selected mode should be visually obvious.

---

# 10. Investigation Workspace

This is the most important UI area.

For an investigation, use a vertical narrative:

```text
QUESTION

Why did revenue decrease in September?


INVESTIGATION

✓ Understanding database
✓ Checking monthly revenue
✓ Comparing categories
● Investigating average order value


FINDINGS

Revenue decreased 27.4% in September.

[ Revenue Trend Chart ]


KEY EVIDENCE

Electronics revenue decreased 46.9%.

[ View Evidence ] [ View SQL ]


CONCLUSION

...


SUPPORTING QUERIES

Query #1
Query #2
Query #3
```

The investigation should feel like an analytical report being built in real time.

---

# 11. Agent Activity Display

Use a compact activity component.

Example:

```text
INVESTIGATION

✓ Understanding database
✓ Checking monthly revenue
✓ Comparing categories
● Investigating average order value
○ Verifying product-level changes
```

States:

### Completed

```text
✓
```

### Active

```text
●
```

### Pending

```text
○
```

### Failed

```text
⚠
```

The activity display should communicate **what the agent did**, not its hidden thoughts.

Good:

```text
✓ Inspected order and payment tables
✓ Compared August and September revenue
● Investigating category-level changes
```

Bad:

```text
I think electronics might be responsible because...
```

---

# 12. Loading and Streaming Behavior

Do not freeze the interface while the agent works.

During execution:

```text
● Investigating...
```

Update the activity display as meaningful actions complete.

Avoid fake progress bars such as:

```text
34%
67%
91%
```

unless the application actually knows the progress.

The agent's investigation is dynamic, so a step-based activity feed is more truthful.

---

# 13. Finding Cards

Findings are the primary analytical output.

A finding card should contain:

```text
FINDING

Revenue decreased 27.4%

Compared with August

────────────────────────────

Main contributor

Electronics
↓ 46.9%

[ View evidence ]
```

Possible fields:

- finding title
- metric
- comparison
- short explanation
- supporting evidence count
- chart
- SQL/evidence controls

Do not overload every card with technical information.

---

# 14. Key Metrics

For quantitative results, use compact metric cards.

Example:

```text
┌─────────────────┐
│ Revenue         │
│ ₹61.0L          │
│ ↓ 27.4%         │
│ vs August       │
└─────────────────┘
```

Possible metrics:

- Revenue
- Orders
- Customers
- Average Order Value
- Conversion rate
- Growth rate

Use semantic indicators:

```text
↑ increase
↓ decrease
→ unchanged
```

Do not use color as the only signal.

---

# 15. Charts

Charts should answer a question, not decorate the page.

Use Plotly.

Recommended chart types:

| Analytical purpose | Chart |
|---|---|
| Trend over time | Line chart |
| Category comparison | Bar chart |
| Before vs after | Grouped bar |
| Composition | Stacked bar |
| Distribution | Histogram |
| Relationship | Scatter plot |
| Geographic comparison | Map only when geographic data exists |

Every chart should have:

- meaningful title
- labeled axes
- readable units
- sensible formatting
- appropriate tooltip
- source/context where useful

Avoid 3D charts and decorative chart effects.

---

# 16. Chart Layout

For a primary finding:

```text
Revenue Trend

┌──────────────────────────────────────────────┐
│                                              │
│                 Plotly chart                 │
│                                              │
└──────────────────────────────────────────────┘

August → September: -27.4%
```

For multiple related charts, prefer a small number of focused visualizations.

Do not put six charts on screen just because the database returned six interesting columns. Humans have limited eyeballs.

---

# 17. Evidence Trail

Evidence Trail is a core product feature.

Every major finding should be traceable to evidence.

Example:

```text
WHY THIS FINDING?

Revenue decreased 27.4%.

Supporting evidence

┌─────────────────────────────────────────────┐
│ Query #1                                    │
│ Monthly revenue comparison                 │
│                                             │
│ [ View SQL ] [ View Results ]              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Query #2                                    │
│ Revenue by category                         │
│                                             │
│ [ View SQL ] [ View Results ]              │
└─────────────────────────────────────────────┘
```

The user should be able to trace:

```text
Finding
   ↓
Evidence
   ↓
Query
   ↓
Result
```

This is one of the main trust mechanisms of the application.

---

# 18. SQL Viewer

SQL should be available without dominating the interface.

Use an expandable section:

```text
▶ View SQL
```

When expanded:

```sql
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(amount) AS revenue
FROM orders
GROUP BY 1
ORDER BY 1;
```

Provide:

```text
[ Copy SQL ]
```

Potentially show:

```text
Executed successfully
124 rows
82 ms
```

Do not force the user to read SQL before seeing the answer.

---

# 19. Result Viewer

When useful, show tabular query results.

Recommended:

```text
Query result

┌─────────────┬───────────────┬────────────┐
│ Month       │ Revenue       │ Change     │
├─────────────┼───────────────┼────────────┤
│ July        │ ₹80L          │ +4.2%      │
│ August      │ ₹84L          │ +5.0%      │
│ September   │ ₹61L          │ -27.4%     │
└─────────────┴───────────────┴────────────┘
```

For large datasets:

- paginate
- limit displayed rows
- allow expansion
- do not render thousands of rows into the main page

---

# 20. Clarification UI

When the agent cannot safely interpret a question, the UI should stop and ask.

Example:

```text
CLARIFICATION NEEDED

How should "best customers" be defined?

○ Highest total spending
○ Most orders
○ Highest average order value
○ Most recent purchases

                         [ Continue ]
```

The clarification interface should be visually distinct but not alarming.

Do not automatically select an option.

The user must explicitly choose when the ambiguity materially affects the query.

---

# 21. Clarification Design Rules

Use clarification when:

- a business term has multiple valid meanings
- the time period is unclear
- the comparison baseline matters
- multiple metrics could reasonably answer the question
- the database cannot safely determine the intended interpretation

Do not ask unnecessary questions.

Bad:

```text
What database are you using?
```

when the database is already connected.

Good:

```text
When you say "best customers", should that mean highest total spending or most orders?
```

---

# 22. Missing Data UI

If the database cannot answer the user's question, show a clear limitation.

Example:

```text
DATA NOT AVAILABLE

I can't answer this from the connected database.

The database contains customer, order, product,
and payment data, but no marketing campaign
or attribution data.

What you can investigate:
• Revenue by product
• Customer activity
• Order trends
```

Never fabricate:

- tables
- columns
- metrics
- results
- database capabilities

The UI should make missing data understandable rather than simply saying "error."

---

# 23. Error States

Errors should be human-readable.

Avoid:

```text
HfHubHTTPError: 402 Payment Required
```

as the primary user-facing message.

Instead:

```text
QUERY FAILED

The generated query could not be executed.

Reason:
The query referenced a column that does not exist.

The agent will attempt to correct the query.
```

If recovery fails:

```text
I couldn't complete this investigation because
the database rejected the required query.

[ View details ]
```

Technical details may be available through an expandable section.

---

# 24. Empty Results

Empty results are not necessarily errors.

Show:

```text
NO MATCHING DATA

The query executed successfully, but no rows
matched the requested conditions.

This may mean:
• there are no matching records
• the selected time period has no data
• the filter is too restrictive
```

The agent may decide whether another investigation is needed.

---

# 25. Final Answer Design

The final answer should prioritize the conclusion.

Recommended structure:

```text
ANSWER

Revenue decreased 27.4% in September compared
with August.

The largest contribution came from Electronics,
where revenue fell 46.9% while order volume
remained relatively stable.

This indicates that lower average order value
was a major contributor to the decline.

────────────────────────────────────────

KEY FINDINGS

27.4%
Revenue decline

46.9%
Electronics decline

↓
Lower average order value

────────────────────────────────────────

EVIDENCE

[ Revenue trend ]
[ Category comparison ]
[ AOV comparison ]

────────────────────────────────────────

SQL

▶ View SQL
```

The answer should be concise first, detailed second.

---

# 26. Confidence and Evidence

Avoid fake numerical confidence scores such as:

```text
Confidence: 94%
```

unless the application has a clearly defined and meaningful statistical basis.

Instead use evidence-oriented language:

```text
Supported by 4 queries
```

or:

```text
Strong evidence
```

only when the application has defined what that label means.

Prefer:

```text
Evidence
3 supporting queries
```

over arbitrary model-generated confidence percentages.

---

# 27. Hypothesis Testing UI

When hypothesis testing is implemented, expose the process as a structured analytical artifact.

Example:

```text
HYPOTHESES

┌─────────────────────────────────────────────┐
│ H1  Fewer orders                            │
│                                             │
│ Orders changed: -2%                        │
│ Evidence: Weak                             │
│                                             │
│ [ View evidence ]                           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ H2  Lower average order value               │
│                                             │
│ AOV changed: -23%                           │
│ Evidence: Strong                            │
│                                             │
│ [ View evidence ]                           │
└─────────────────────────────────────────────┘
```

Important:

The UI should expose **hypotheses and evidence**, not private chain-of-thought.

---

# 28. Explore Mode UI

Explore mode should feel different from a normal question-answering session.

Example:

```text
EXPLORE DATABASE

Looking for notable patterns...

✓ Checked time-series metrics
✓ Compared major categories
✓ Checked customer activity
● Validating unusual changes
```

Then:

```text
NOTABLE FINDINGS

01
Customer retention decreased 12%
between March and April.

02
Electronics revenue dropped 31%
in one region.

03
Average order value increased
despite lower order volume.
```

Each finding should include:

```text
[ View evidence ]
[ View chart ]
[ View SQL ]
```

The agent must validate interesting patterns before presenting them as findings.

---

# 29. Ask Mode UI

Ask mode should be faster and less visually heavy.

Example:

```text
ASK

What were the top 10 products last month?

────────────────────────────

ANSWER

1. Product A      ₹8.4L
2. Product B      ₹7.9L
3. Product C      ₹7.2L
...

[ View chart ]

▶ View SQL
▶ View evidence
```

Do not show a large investigation timeline for trivial questions.

The UI should adapt to the complexity of the task.

---

# 30. Investigation Complexity

The UI should scale with the agent's work.

### Simple

```text
Question
↓
Answer
↓
SQL
```

### Moderate

```text
Question
↓
Activity
↓
Finding
↓
Chart
↓
Evidence
```

### Complex

```text
Question
↓
Investigation
↓
Hypotheses
↓
Queries
↓
Findings
↓
Evidence
↓
Conclusion
```

Do not force every query to look like a complex investigation.

---

# 31. Conversation / History

Previous questions should be accessible.

Example:

```text
RECENT

Why did revenue decrease?
Top products last month
Customer retention trend
Sales by region
```

Selecting a previous investigation should restore the result if session persistence supports it.

History should be secondary to the current investigation.

---

# 32. Database Overview

After connecting a database, provide a lightweight overview.

Example:

```text
DATABASE

ecommerce_pipeline

PostgreSQL
● Connected

Tables
24

Relationships
31

Last inspected
Just now
```

Optional expandable section:

```text
TABLES

orders
customers
products
payments
...
```

Do not overwhelm the user with the full schema immediately.

---

# 33. Design Tokens

Keep visual values centralized.

Suggested tokens:

```text
--background
--surface
--surface-secondary
--border
--text-primary
--text-secondary
--text-muted
--accent
--success
--warning
--error
```

Spacing should follow a consistent scale.

Example:

```text
4px
8px
12px
16px
24px
32px
48px
```

Do not randomly choose spacing values throughout the application.

---

# 34. Typography

Use a modern, highly readable sans-serif.

Hierarchy:

```text
Page title
32px

Section title
20–24px

Card title
16–18px

Body
14–16px

Metadata
12–13px
```

The exact values can be adapted to Streamlit limitations.

Prioritize readability over visual novelty.

---

# 35. Color System

Use a restrained palette.

Recommended semantic roles:

```text
Primary accent
→ interactive elements

Success
→ completed actions / positive changes

Warning
→ attention / ambiguity

Error
→ failed operations

Neutral
→ normal analytical information
```

Do not color every metric.

For financial/analytical values, avoid assuming:

```text
green = good
red = bad
```

A decrease in cost may be positive while a decrease in revenue may be negative.

The meaning must come from context.

---

# 36. Dark and Light Themes

The UI should work in both themes if Streamlit configuration permits.

Do not hard-code colors that become unreadable in the opposite theme.

Charts must also remain readable.

Use theme-aware Plotly configuration.

---

# 37. Buttons

Buttons should have clear action labels.

Good:

```text
Investigate
Continue
View evidence
View SQL
Copy SQL
Run again
```

Avoid:

```text
Click here
Proceed
Go
Do it
Magic
AI
```

Primary actions should be visually stronger than secondary actions.

---

# 38. Expanders

Use expanders for technical details.

Good candidates:

```text
▶ View SQL
▶ View raw results
▶ View evidence
▶ Investigation details
▶ Technical details
```

Do not hide the actual conclusion inside an expander.

---

# 39. Notifications

Use Streamlit status/notification components consistently.

Examples:

```text
Success
Database connected.

Warning
This question is ambiguous.

Error
The query could not be executed.

Info
The database contains no marketing attribution data.
```

Avoid excessive toast-style notifications.

Persistent important information should remain visible in the page.

---

# 40. Responsive Design

The application must remain usable on smaller screens.

Priorities:

1. Main answer
2. Findings
3. Charts
4. Evidence
5. SQL
6. Secondary metadata

Avoid layouts that require users to horizontally scroll across the entire application.

Use columns only when the content remains readable.

---

# 41. Accessibility

Follow basic accessibility principles.

- Do not rely only on color.
- Use readable contrast.
- Use meaningful labels.
- Keep controls keyboard accessible where supported.
- Use descriptive button text.
- Avoid tiny text.
- Do not communicate state through animation alone.

Charts should have textual context.

Example:

```text
Revenue decreased 27.4% from August to September.
```

should appear near the chart rather than requiring the user to infer everything visually.

---

# 42. Agent State Mapping

The frontend should map backend agent states into clear UI states.

Recommended:

```text
CONNECTING
↓
READY
↓
UNDERSTANDING
↓
INVESTIGATING
↓
WAITING_FOR_USER
↓
EXECUTING
↓
ANALYZING
↓
COMPLETED
```

Error:

```text
FAILED
```

The exact backend state names can differ, but the frontend should have a stable presentation layer.

---

# 43. Streamlit Implementation Rules

Use Streamlit as the primary frontend framework.

Prefer:

- `st.sidebar`
- `st.text_area`
- `st.button`
- `st.radio`
- `st.selectbox`
- `st.tabs`
- `st.expander`
- `st.metric`
- `st.dataframe`
- `st.plotly_chart`
- `st.status`
- `st.spinner`
- `st.session_state`

Use custom CSS only where Streamlit's native components are insufficient.

Do not turn the application into a fragile collection of HTML/CSS hacks.

---

# 44. Session State

Use `st.session_state` for UI state such as:

```text
database_connection
selected_mode
current_question
investigation_state
clarification_options
selected_clarification
findings
evidence
charts
query_history
```

Do not put business logic inside UI state management.

The agent and database layers should remain independent of Streamlit.

---

# 45. Frontend Architecture Boundary

The UI should not:

- generate SQL
- inspect database schema directly
- decide hypotheses
- execute arbitrary SQL
- implement agent reasoning
- contain database credentials

Instead:

```text
Streamlit UI
    ↓
Application / Agent interface
    ↓
LangGraph agent
    ↓
Tools
    ↓
Database
```

The frontend renders state produced by the application.

---

# 46. Component Organization

Recommended UI structure:

```text
ui/
├── __init__.py
├── connection.py
├── sidebar.py
├── query_input.py
├── mode_selector.py
├── investigation.py
├── clarification.py
├── findings.py
├── evidence.py
└── sql_viewer.py
```

Additional components can be introduced when justified.

Avoid creating a separate file for every tiny UI element.

---

# 47. Suggested Main Screen

A mature version of the main screen should resemble:

```text
┌──────────────────────────────────────────────────────────────┐
│ SQLPILOT                                    ● Connected       │
│ AI DATA ANALYST                                               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Ask your database                                            │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Why did revenue decrease in September?                   │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ [ Ask ]     [ Investigate ]     [ Explore ]                 │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ INVESTIGATION                                                │
│                                                              │
│ ✓ Understanding database                                    │
│ ✓ Checking monthly revenue                                  │
│ ✓ Comparing categories                                      │
│ ● Investigating average order value                         │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ KEY FINDING                                                  │
│                                                              │
│ Revenue decreased 27.4%                                      │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │                    Revenue Trend                         │ │
│ │                                                          │ │
│ │                     Plotly chart                         │ │
│ └──────────────────────────────────────────────────────────┘ │
│                                                              │
│ Main contributor: Electronics                                │
│ Revenue change: -46.9%                                      │
│                                                              │
│ [ View evidence ]   [ View SQL ]                            │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ANSWER                                                      │
│                                                              │
│ Revenue decreased primarily because Electronics revenue      │
│ fell sharply while order volume remained relatively stable.  │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ EVIDENCE                                                     │
│                                                              │
│ Query #1   Monthly revenue comparison     [View]            │
│ Query #2   Revenue by category            [View]            │
│ Query #3   Average order value            [View]            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

This is the target interaction model, not a requirement that every screen always contain every section.

---

# 48. What the UI Must Never Become

Do not turn SQLPilot into:

### A generic chatbot

```text
User:
Why did revenue fall?

AI:
Revenue may have fallen due to several factors...
```

without showing actual database evidence.

### A SQL generator

```text
Question
↓
SQL
↓
Table
```

with no investigation capability.

### A static dashboard

The dashboard should be generated around the user's current analytical task.

### A developer console

The user should not need to understand LangGraph, SQLAlchemy, prompts, model providers, or tool schemas.

### An "AI magic" interface

Do not use visual effects to imply intelligence.

The intelligence should be demonstrated by the investigation itself.

---

# 49. Design for Trust

Every important UI decision should answer:

> "Can the user understand why SQLPilot reached this conclusion?"

Trust comes from:

```text
Question
↓
Visible investigation activity
↓
Finding
↓
Evidence
↓
SQL
↓
Result
↓
Conclusion
```

Not from:

```text
AI says so.
```

---

# 50. MVP UI

The first frontend implementation should contain only the necessary pieces.

### Required

- database connection status
- database name
- mode selector
- natural-language input
- Ask / Investigate action
- investigation activity
- final answer
- findings
- SQL viewer
- evidence viewer
- basic chart support
- clarification UI
- error states

### Defer

- advanced animations
- complex navigation
- user accounts
- collaborative workspaces
- advanced dashboards
- scheduled monitoring UI
- proactive insight feeds
- extensive customization

Build the analytical experience first.

---

# 51. UI Development Order

Implement the frontend in this order:

## Step 1 — Application shell

Build:

```text
Header
Sidebar
Main workspace
Connection status
```

## Step 2 — Query experience

Build:

```text
Mode selector
Question input
Submit / Investigate
```

## Step 3 — Agent activity

Build:

```text
Investigation status
Completed / active / pending states
```

## Step 4 — Answer

Build:

```text
Final answer
Key findings
Metrics
```

## Step 5 — Evidence

Build:

```text
Evidence cards
SQL viewer
Result viewer
```

## Step 6 — Clarification

Build:

```text
Ambiguity message
Options
Continue
```

## Step 7 — Visualization

Build:

```text
Plotly charts
Chart containers
Chart explanations
```

## Step 8 — Polish

Improve:

```text
Spacing
Typography
Responsive layout
Theme
Error states
Loading states
Empty states
```

Do not start with visual polish before the core analytical workflow works.

---

# 52. Frontend Quality Checklist

Before considering a UI feature complete, verify:

### Visual

- [ ] Consistent spacing
- [ ] Consistent typography
- [ ] Clear hierarchy
- [ ] No unnecessary decoration
- [ ] Charts are readable
- [ ] Light/dark themes remain usable

### Interaction

- [ ] Loading state exists
- [ ] Error state exists
- [ ] Empty state exists
- [ ] Buttons have clear labels
- [ ] Clarification requires explicit user choice
- [ ] Technical details are expandable

### Analytical

- [ ] Findings are visible
- [ ] Evidence is accessible
- [ ] SQL is accessible
- [ ] Results can be inspected
- [ ] Unsupported conclusions are not presented as facts
- [ ] Missing data is clearly communicated

### Architecture

- [ ] UI does not contain database logic
- [ ] UI does not generate SQL
- [ ] UI does not contain agent reasoning
- [ ] Agent state is separated from presentation
- [ ] Streamlit-specific code stays in the UI layer

---

# 53. Final Design Principle

SQLPilot should feel like this:

```text
"I asked an analyst a question,
and I can see the investigation,
the evidence,
the result,
and the conclusion."
```

Not this:

```text
"I entered a sentence into a SQL generator."
```

The frontend exists to make the agent's analytical process **observable, understandable, and trustworthy**.

The single most important UI principle is:

> **Show the user's question, the agent's high-level actions, the evidence it gathered, and the conclusion it reached. Hide private reasoning, implementation complexity, and unnecessary technical noise.**
