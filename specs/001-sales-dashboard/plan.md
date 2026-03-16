# Implementation Plan: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-16 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-sales-dashboard/spec.md`

## Summary

Build a Streamlit sales analytics dashboard for ShopSmart that displays KPI cards (Total
Sales, Total Orders), an interactive sales trend line chart with daily/monthly toggle,
category and regional breakdown bar charts, sidebar filters (date range, category, region),
and an aggregated summary table. Data is loaded from `data/sales-data.csv` via a
`DataService` class. Deployed as a Docker container to a cloud platform.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit, Plotly, Pandas, uv
**Storage**: CSV file — `data/sales-data.csv` (~1,000 rows)
**Testing**: pytest (unit tests for DataService/formatting; integration tests for full pipeline)
**Target Platform**: Cloud platform (AWS/GCP/Azure), containerized via Docker
**Project Type**: Web application (Streamlit dashboard)
**Performance Goals**: Dashboard load < 5 seconds; filter updates visible < 2 seconds
**Constraints**: Single-user per session; stateless app; env-var config only
**Scale/Scope**: ~1,000 transaction records, 5 categories, 4 regions, 12 months of data

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Data Integrity First | ✅ PASS | DataService validates data on load; error state surfaced on failure; freshness timestamp displayed |
| II. Dual-Audience Design | ✅ PASS | KPI cards prominent at top; sidebar filters for power users; summary table for analysts; plain business labels throughout |
| III. API-First Data Access | ⚠️ VIOLATION (justified) | CSV used as primary Phase 1 data source — see Complexity Tracking |
| IV. Test-Verified Data Pipelines | ✅ PASS | DataService fully unit-tested; integration tests cover full CSV → rendered metric pipeline |
| V. Cloud-Native Deployment | ✅ PASS | Dockerized, stateless, env-var config, reproducible build |

## Project Structure

### Documentation (this feature)

```text
specs/001-sales-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── data-service.md
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
dashboard/
├── app.py                  # Streamlit entry point; assembles layout
├── services/
│   └── data_service.py     # DataService class — all data access & transformation
├── components/
│   ├── kpi_cards.py        # KPI card rendering (overall + filtered values)
│   ├── charts.py           # Trend, category, region chart rendering
│   ├── filters.py          # Sidebar filter controls (date range, category, region)
│   └── summary_table.py    # Aggregated summary table component
└── utils/
    └── formatting.py       # Currency and number formatting helpers

tests/
├── unit/
│   ├── test_data_service.py    # DataService loading, filtering, aggregation
│   ├── test_formatting.py      # Currency/number formatting functions
│   └── test_charts.py          # Chart data preparation functions
└── integration/
    └── test_data_pipeline.py   # Full pipeline: CSV load → filter → KPI → chart data

data/
└── sales-data.csv          # Source data (existing, ~1,000 rows)

pyproject.toml              # uv project config with all dependencies
Dockerfile                  # Container build for cloud deployment
.env.example                # Environment variable template
```

**Structure Decision**: Single-project layout with `dashboard/` as the app root and
`tests/` at repository root. This keeps the Streamlit entry point (`app.py`) cleanly
separated from test infrastructure while maintaining a flat, navigable structure.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle III (API-First): CSV used as primary data source | PRD explicitly specifies `data/sales-data.csv` as the Phase 1 data source; live API integration is a Phase 2 item | Requiring a live API in Phase 1 would contradict the PRD, significantly expand scope, and introduce external dependencies that block development |
