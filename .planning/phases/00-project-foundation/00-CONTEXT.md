# Phase 0: Project Foundation - Context

**Gathered:** 2026-10-02  
**Status:** Ready for planning  
**Source:** Authoritative documents (`phase.md`, `architecture.md`, `rules.md`, `PRD.md`, `design.md`)

<domain>
## Phase Boundary

Phase 0 establishes a clean, modern Python application skeleton, virtual environment guidance, dependency management, environment variable schema, application entry point with a functional Streamlit shell, folder structure, and automated testing setup.

Scope strictly excludes:
- Agent reasoning logic (deferred to Phase 4)
- SQL generation or safety validator (deferred to Phase 3)
- Tool calling & schema inspection (deferred to Phase 2)
- Complex investigation & hypothesis testing (deferred to Phase 8)
- Visualizations & Plotly charts (deferred to Phase 10)
</domain>

<decisions>
## Implementation Decisions

### Project Structure & Layout
- **D-01:** Root directory layout will directly mirror `phase.md` Section 3:
  ```text
  app.py
  config.py
  requirements.txt
  .env.example
  .gitignore
  README.md
  agent/
  tools/
  database/
  analysis/
  visualization/
  models/
  ui/
  tests/
  ```
- **D-02:** Each submodule will contain an `__init__.py` to ensure clean Python package imports.

### Dependency Management & Python Environment
- **D-03:** Dependencies in `requirements.txt` will be pinned with modern, compatible versions:
  - `streamlit>=1.35.0`
  - `langchain>=0.2.0`
  - `langchain-core>=0.2.0`
  - `langgraph>=0.1.0`
  - `sqlalchemy>=2.0.0`
  - `psycopg2-binary>=2.9.9`
  - `pydantic>=2.7.0`
  - `plotly>=5.22.0`
  - `python-dotenv>=1.0.1`
  - `pytest>=8.2.0`
  - `sqlparse>=0.5.0`
- **D-04:** Environment settings will be managed with `pydantic-settings` / `python-dotenv` in `config.py`, loading database URL, LLM API keys, and operational limits.

### Application Entry Point
- **D-05:** `app.py` serves as the Streamlit entry point. In Phase 0, it renders the basic shell header ("SQLPilot: AI Data Analyst"), connection badge ("Disconnected"), and workspace layout placeholders adhering to `design.md` visual rules.

### Testing Setup
- **D-06:** `tests/` directory will include basic unit tests (`test_imports.py`, `test_config.py`, `test_app_structure.py`) to verify package integrity and configuration parsing under `pytest`.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing:**
- [`phase.md`](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/phase.md#L119-L196) — Section 3: Phase 0 specification and completion criteria.
- [`architecture.md`](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/architecture.md#L843-L885) — Project folder structure and module responsibilities.
- [`rules.md`](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/rules.md#L1-L70) — Golden rules, security boundaries, and secrets isolation.
- [`design.md`](file:///c:/Users/panka/OneDrive/Desktop/SQLPilot/design.md#L89-L195) — Visual identity, typography, header, and sidebar guidelines.
</canonical_refs>
