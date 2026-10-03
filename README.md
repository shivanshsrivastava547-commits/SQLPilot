# SQLPilot

SQLPilot is an agentic AI data analyst for relational databases. The system is designed to understand a business question, inspect schema and data, decide what to investigate next, and produce evidence-backed answers with SQL and visualizations.

## Project structure

- `app.py` — Streamlit entry point
- `config.py` — application settings and environment loading
- `agent/` — LangGraph agent orchestration and nodes
- `database/` — connection and SQL safety utilities
- `tools/` — schema, query, analysis, and clarification tools
- `analysis/` — hypothesis and evidence analysis logic
- `visualization/` — chart generation helpers
- `models/` — shared domain models and state objects
- `ui/` — dashboard and component helpers
- `tests/` — verification tests

## Local setup

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment variables:
   ```bash
   copy .env.example .env
   ```
4. Start the app:
   ```bash
   streamlit run app.py
   ```

## Notes

SQLPilot now includes a working agentic data analysis flow, database safety checks, schema inspection, evidence-backed investigation, proactive insights, and scheduled monitoring summaries. The project is verified with a passing automated test suite and a runnable Streamlit dashboard.
