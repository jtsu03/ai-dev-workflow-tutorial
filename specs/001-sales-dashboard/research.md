# Research: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-16

## Resolved Decisions

### 1. Streamlit App Structure

**Decision**: Single `app.py` entry point assembling imported components; logic separated
into `services/`, `components/`, and `utils/` submodules under `dashboard/`.

**Rationale**: Streamlit's execution model re-runs the entire script on each interaction.
Keeping `app.py` as a thin orchestrator and isolating logic in importable modules makes
unit testing possible without invoking Streamlit itself.

**Alternatives considered**:
- Flat single-file app — rejected because DataService and component logic cannot be unit
  tested without running Streamlit.
- Multi-page Streamlit app — rejected because all content fits on one page; multi-page
  adds navigation complexity without user benefit.

---

### 2. State Management for Filters

**Decision**: Use `st.session_state` to persist filter selections across reruns. Filter
widgets (sidebar) write to session state; `DataService` reads session state to produce
the filtered DataFrame.

**Rationale**: Streamlit reruns the full script on every widget interaction. Without
session state, filter selections reset on each rerun. `st.session_state` is the
idiomatic Streamlit solution and requires no external state store.

**Alternatives considered**:
- URL query parameters — more complex, not needed for single-user session scope.
- External cache (Redis) — overkill for a single-user dashboard with a 1,000-row dataset.

---

### 3. DataService Pattern

**Decision**: A `DataService` class instantiated once (via `@st.cache_resource`) holds
the loaded DataFrame and exposes methods: `get_filtered_data(filter_state)`,
`get_kpi_summary(df)`, `get_trend_data(df, granularity)`, `get_category_summary(df)`,
`get_region_summary(df)`.

**Rationale**: `@st.cache_resource` ensures the CSV is loaded only once per server
session, not on every rerun. The class encapsulates all data logic, making it fully
unit-testable independent of Streamlit. This satisfies Constitution Principle IV.

**Alternatives considered**:
- `@st.cache_data` on standalone functions — functional but harder to test as a
  cohesive pipeline; mocking is less straightforward.
- Module-level globals — not thread-safe and not independently testable.

---

### 4. Plotly Chart Rendering in Streamlit

**Decision**: Use `st.plotly_chart(fig, use_container_width=True)` for all charts.
Chart preparation functions in `components/charts.py` return Plotly `Figure` objects;
`app.py` renders them.

**Rationale**: Separating figure construction from rendering allows unit tests to assert
on figure data without Streamlit. `use_container_width=True` ensures responsive layout.

**Alternatives considered**:
- `st.line_chart` / `st.bar_chart` — simpler but insufficient customization (no
  tooltips, sorting, axis labels required by spec).
- Altair/Matplotlib — not in the constitution's approved stack.

---

### 5. Daily vs. Monthly Granularity Toggle

**Decision**: Implement as a `st.radio` widget in the sidebar (alongside filters) with
options "Daily" / "Monthly". `DataService.get_trend_data(df, granularity)` resamples
the DataFrame using Pandas `resample('D')` or `resample('MS')` accordingly.

**Rationale**: `st.radio` is compact and visually clear for a binary choice. Pandas
`resample` is the idiomatic approach for time-series aggregation.

---

### 6. Dual KPI Display (Overall + Filtered)

**Decision**: `DataService` is initialized with the full DataFrame. KPI methods accept
a DataFrame argument; `app.py` calls them twice — once with the full DF, once with the
filtered DF — and passes both values to `kpi_cards.py` for rendering.

**Rationale**: Keeps KPI logic stateless and testable. The component receives two
values and decides how to render them (show filtered value below overall when they differ).

---

### 7. Docker / Deployment

**Decision**: Single-stage `Dockerfile` based on `python:3.11-slim`. Copies `dashboard/`,
`data/`, and `pyproject.toml`. Runs `uv pip install` then `streamlit run dashboard/app.py`.
Port 8501 exposed. No build-time secrets; all config via environment variables.

**Rationale**: Minimal image size; reproducible build; aligns with Constitution Principle V.
Cloud vendor (AWS/GCP/Azure) is not specified here — the Dockerfile is vendor-agnostic.

---

### 8. Integration Testing Strategy

**Decision**: Integration tests in `tests/integration/test_data_pipeline.py` use the
real `data/sales-data.csv` file (not a mock) and exercise the full chain: CSV load →
`DataService` → filtered KPI values → chart-ready DataFrames. Assertions verify
known expected values (Total Sales ~$650K–$700K, Total Orders = 482).

**Rationale**: Constitution Principle IV requires "real or realistic API responses (not
mocked schemas)." Using the real CSV satisfies this. Known totals from the PRD give
deterministic assertions.
