# Tasks: ShopSmart Sales Analytics Dashboard

**Input**: Design documents from `specs/001-sales-dashboard/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: After implementation — test tasks follow implementation tasks within each user story phase.

**Organization**: Grouped by user story in strict priority order (P1 → P5). Each story is
independently completable and testable before the next begins.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no shared dependencies)
- **[Story]**: User story label (US1–US5) — required for Phase 3+ tasks
- All tasks include exact file paths

---

## Phase 1: Setup

**Purpose**: Project initialization and folder structure

- [x] T001 Create project folder structure: `dashboard/`, `dashboard/services/`, `dashboard/components/`, `dashboard/utils/`, `tests/`, `tests/unit/`, `tests/integration/`
- [x] T002 Initialize `pyproject.toml` with uv: declare Python 3.11+ and dependencies (streamlit, plotly, pandas, pytest, pytest-cov)
- [x] T003 [P] Create `.env.example` with placeholder env var documentation at repo root
- [x] T004 [P] Create `Dockerfile`: python:3.11-slim base, copy `dashboard/` and `data/`, install via uv, expose port 8501, run `streamlit run dashboard/app.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure every user story depends on — MUST complete before any story begins

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create `DataService` class skeleton with `DataLoadError` and `DataValidationError` exception classes in `dashboard/services/data_service.py`
- [x] T006 [P] Define `FilterState`, `KPISummary`, `TrendDataPoint`, and `SegmentSummary` dataclasses in `dashboard/services/data_service.py`
- [x] T007 [P] Implement `format_currency(value: float) -> str` and `format_count(value: int) -> str` helpers in `dashboard/utils/formatting.py`

**Checkpoint**: Foundation ready — all user story phases can now begin in priority order

---

## Phase 3: User Story 1 — At-a-Glance KPI Overview (Priority: P1) 🎯 MVP

**Goal**: Finance manager opens the dashboard and immediately sees Total Sales and Total
Orders formatted correctly for the full dataset.

**Independent Test**: Run `streamlit run dashboard/app.py`, verify Total Sales ≈ $650K–$700K
and Total Orders = 482 are displayed at the top with correct formatting and no filters active.

### Implementation — User Story 1

- [x] T008 [US1] Implement `DataService.__init__`: load `data/sales-data.csv`, validate columns/types, drop malformed rows (log warnings), raise `DataLoadError` / `DataValidationError` per data-model rules in `dashboard/services/data_service.py`
- [x] T009 [US1] Implement `DataService.get_kpi_summary(df)`: return `KPISummary` with sum of `total_amount` and row count in `dashboard/services/data_service.py`
- [x] T010 [P] [US1] Implement `DataService.get_date_bounds()`, `get_available_categories()`, `get_available_regions()` in `dashboard/services/data_service.py`
- [x] T011 [US1] Implement `kpi_cards` component: render two KPI cards (Total Sales, Total Orders) using formatting utils; accept `overall` and `filtered` KPISummary values; show filtered value only when filters are active in `dashboard/components/kpi_cards.py`
- [x] T012 [US1] Implement `dashboard/app.py` entry point: page config, `@st.cache_resource` DataService initialization, session state initialization, KPI card rendering (dual values: full DF + filtered DF)

### Tests — User Story 1

- [x] T013 [P] [US1] Write unit tests for `DataService.__init__`: valid CSV loads correctly, malformed rows dropped with warning, `DataLoadError` on missing file, `DataValidationError` when >10% rows dropped in `tests/unit/test_data_service.py`
- [x] T014 [P] [US1] Write unit tests for `DataService.get_kpi_summary`: correct totals for full DF, correct totals for empty DF (returns zeros) in `tests/unit/test_data_service.py`
- [x] T015 [P] [US1] Write unit tests for `format_currency` and `format_count`: correct formatting, edge cases (zero, large values) in `tests/unit/test_formatting.py`

**Checkpoint**: KPI cards show correct values — User Story 1 is independently functional ✅

---

## Phase 4: User Story 2 — Sales Trend Over Time (Priority: P2)

**Goal**: CEO sees a line chart of sales over time and can toggle between daily and monthly
granularity.

**Independent Test**: In the running dashboard, verify the trend line chart renders with
data points, hovering shows exact values, and the Daily/Monthly toggle correctly changes
chart granularity.

### Implementation — User Story 2

- [ ] T016 [US2] Implement `DataService.get_trend_data(df, granularity)`: resample by day (`resample("D")`) or month-start (`resample("MS")`), return list of `TrendDataPoint` sorted ascending in `dashboard/services/data_service.py`
- [ ] T017 [US2] Implement `build_trend_chart(trend_data, granularity)`: Plotly line chart with time on x-axis, sales on y-axis, interactive hover tooltips, plain business labels in `dashboard/components/charts.py`
- [ ] T018 [US2] Add trend chart section to `dashboard/app.py`: `st.radio` toggle ("Daily" / "Monthly") stored in session state, call `get_trend_data` with current granularity, render with `st.plotly_chart(..., use_container_width=True)`

### Tests — User Story 2

- [ ] T019 [P] [US2] Write unit tests for `DataService.get_trend_data`: daily output has one point per day, monthly output has one point per month, empty DF returns empty list in `tests/unit/test_data_service.py`
- [ ] T020 [P] [US2] Write unit tests for `build_trend_chart`: returned Figure has correct x/y data, correct axis labels in `tests/unit/test_charts.py`

**Checkpoint**: Trend chart renders and toggles correctly — User Story 2 is independently functional ✅

---

## Phase 5: User Story 3 — Category and Regional Breakdown (Priority: P3)

**Goal**: Marketing director and regional manager see bar charts for category and region,
sorted highest to lowest, with interactive tooltips.

**Independent Test**: In the running dashboard, verify two bar charts appear below the trend
chart — one for categories, one for regions — both sorted descending, all 5 categories and
4 regions represented, hover tooltips show exact values.

### Implementation — User Story 3

- [ ] T021 [US3] Implement `DataService.get_category_summary(df)` and `DataService.get_region_summary(df)`: group by dimension, sum `total_amount`, count rows, return list of `SegmentSummary` sorted descending by `total_sales` in `dashboard/services/data_service.py`
- [ ] T022 [P] [US3] Implement `build_category_chart(summaries)` and `build_region_chart(summaries)`: Plotly horizontal or vertical bar charts, sorted by value, interactive tooltips, plain business labels in `dashboard/components/charts.py`
- [ ] T023 [US3] Add category and region chart sections to `dashboard/app.py`: call summaries on filtered DF, render side-by-side with `st.columns`

### Tests — User Story 3

- [ ] T024 [P] [US3] Write unit tests for `get_category_summary` and `get_region_summary`: correct aggregation, correct sort order, empty DF returns empty list in `tests/unit/test_data_service.py`
- [ ] T025 [P] [US3] Write unit tests for `build_category_chart` and `build_region_chart`: Figure has correct bar count and data values in `tests/unit/test_charts.py`

**Checkpoint**: Both breakdown charts display correctly — User Story 3 is independently functional ✅

---

## Phase 6: User Story 4 — Interactive Filtering (Priority: P4)

**Goal**: Any user can filter by date range, category, and region. All charts and KPIs update
simultaneously. KPI cards show both overall and filtered totals when filters are active.

**Independent Test**: Apply a date range filter and verify all three charts update, the filtered
KPI value changes, and the overall KPI value stays the same. Apply a category filter, verify
intersection with date filter. Clear all filters, verify full dataset restored.

### Implementation — User Story 4

- [ ] T026 [US4] Implement `DataService.get_filtered_data(filter_state)`: apply date range, category list, and region list filters as intersection; return filtered DataFrame copy in `dashboard/services/data_service.py`
- [ ] T027 [US4] Implement sidebar filter controls component: `st.date_input` (date range), `st.multiselect` (categories), `st.multiselect` (regions), `st.button` ("Clear Filters") — all write to `st.session_state.filter_state` in `dashboard/components/filters.py`
- [ ] T028 [US4] Wire filters into `dashboard/app.py`: render `filters` component in `st.sidebar`, pass `filter_state` to `get_filtered_data`, pass filtered DF to all chart and table builders
- [ ] T029 [US4] Update `kpi_cards.py` to conditionally show filtered total below overall total when `filtered_kpi != overall_kpi` in `dashboard/components/kpi_cards.py`

### Tests — User Story 4

- [ ] T030 [P] [US4] Write unit tests for `get_filtered_data`: date range filter, category filter, region filter, combined filters (intersection), empty result when no matching rows in `tests/unit/test_data_service.py`
- [ ] T031 [US4] Write integration test: load real `data/sales-data.csv` → apply filter → assert KPI values change, unfiltered KPI unchanged, category/region summaries reflect filter in `tests/integration/test_data_pipeline.py`

**Checkpoint**: All filters work, KPIs show dual values — User Story 4 is independently functional ✅

---

## Phase 7: User Story 5 — Aggregated Summary Table (Priority: P5)

**Goal**: Analyst sees aggregated sales and order counts by category and by region in tabular
form, reflecting active filters.

**Independent Test**: In the running dashboard, scroll to the summary section and verify a table
is present showing category and region aggregations. Apply a filter and confirm table values
change. Verify values match the corresponding bar charts.

### Implementation — User Story 5

- [ ] T032 [US5] Implement `summary_table` component: accept two `list[SegmentSummary]` (categories + regions), render as two formatted `st.dataframe` tables with `total_sales` as currency and `total_orders` with comma separators in `dashboard/components/summary_table.py`
- [ ] T033 [US5] Add summary table section to `dashboard/app.py`: call `get_category_summary` and `get_region_summary` on filtered DF, pass to `summary_table` component

### Tests — User Story 5

- [ ] T034 [P] [US5] Write unit tests for `summary_table`: correct column count, formatted values, empty list renders gracefully in `tests/unit/test_summary_table.py`
- [ ] T035 [US5] Extend integration test in `tests/integration/test_data_pipeline.py`: assert summary table data (category + region summaries) matches chart data under same filter state

**Checkpoint**: Summary table present and filter-responsive — User Story 5 is independently functional ✅

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that apply across all user stories

- [ ] T036 Add data freshness timestamp to `dashboard/app.py`: display load time of `data/sales-data.csv` prominently (Constitution Principle I requirement)
- [ ] T037 [P] Add error state handling to `dashboard/app.py`: catch `DataLoadError` and `DataValidationError`, display user-friendly error message with `st.error()` instead of crashing
- [ ] T038 [P] Audit all chart labels, axis titles, and tooltip text across `dashboard/components/charts.py` and `dashboard/components/kpi_cards.py` to confirm plain business language (no code identifiers like `total_amount`)
- [ ] T039 [P] Run quickstart.md validation: load dashboard, verify Total Sales ≈ $650K–$700K, Total Orders = 482, all 5 categories and 4 regions shown, all filters functional
- [ ] T040 [P] Build Docker image and run smoke test: `docker build -t shopsmart-dashboard .` then `docker run -p 8501:8501 shopsmart-dashboard` and verify dashboard loads at localhost:8501

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately; [P] tasks run in parallel
- **Foundational (Phase 2)**: Depends on Phase 1 — T005 before T006/T007; T006 and T007 parallel
- **US1 (Phase 3)**: Depends on Phase 2 — T008 → T009 → T010/T011 parallel → T012; tests T013/T014/T015 parallel after T008/T009
- **US2 (Phase 4)**: Depends on US1 checkpoint — T016 → T017 → T018; tests T019/T020 parallel after T016/T017
- **US3 (Phase 5)**: Depends on US2 checkpoint — T021 → T022/T023 parallel; tests T024/T025 parallel after T021/T022
- **US4 (Phase 6)**: Depends on US3 checkpoint — T026 → T027 → T028 → T029; T030 parallel after T026; T031 after T028
- **US5 (Phase 7)**: Depends on US4 checkpoint — T032 → T033; T034 parallel after T032; T035 after T033
- **Polish (Phase 8)**: Depends on US5 checkpoint — all [P] tasks parallel; T036/T037 first

### Within Each User Story

- DataService methods before components
- Components before app.py wiring
- Integration tests after app.py wiring

---

## Parallel Opportunities

### Phase 3 (US1) — Example parallel launch

```bash
# After T008 (DataService.__init__) completes:
Task A: T009 get_kpi_summary()           → dashboard/services/data_service.py
Task B: T010 get_date_bounds() etc.       → dashboard/services/data_service.py  [P]
Task C: T013 unit tests for __init__      → tests/unit/test_data_service.py      [P]

# After T009 completes:
Task A: T011 kpi_cards component          → dashboard/components/kpi_cards.py
Task B: T014 unit tests for get_kpi_summary → tests/unit/test_data_service.py   [P]
Task C: T015 unit tests for formatting    → tests/unit/test_formatting.py        [P]
```

### Phase 6 (US4) — Example parallel launch

```bash
# After T026 (get_filtered_data) completes:
Task A: T027 sidebar filters component   → dashboard/components/filters.py
Task B: T030 unit tests for filtering    → tests/unit/test_data_service.py      [P]
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 (Setup)
2. Complete Phase 2 (Foundational)
3. Complete Phase 3 (US1 — KPI cards)
4. **STOP and VALIDATE**: Open dashboard, confirm Total Sales ≈ $650K–$700K and Total Orders = 482
5. Demo to stakeholders if needed

### Incremental Delivery

1. Setup + Foundational → skeleton ready
2. US1 complete → KPI cards working (MVP)
3. US2 complete → trend chart added (demo-ready)
4. US3 complete → breakdowns added (full read-only dashboard)
5. US4 complete → filters working (self-service analytics)
6. US5 complete → summary table added (full feature)
7. Polish → production-ready

---

## Notes

- [P] tasks = can be worked in parallel (different files, no blocking dependencies)
- [USn] label maps each task to its user story for traceability
- Each story has a Checkpoint — validate independently before moving to next
- Tests are written after implementation within each story phase
- Commit after each task or logical group with a message referencing the Jira ticket
- Do not start a new story phase until the previous checkpoint passes
