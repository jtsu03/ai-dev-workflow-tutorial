# Quickstart: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-16

## Prerequisites

- Python 3.11+
- `uv` installed (`pip install uv` or see https://docs.astral.sh/uv/)
- Git (repo already cloned)

## Local Development Setup

```bash
# 1. Switch to the feature branch
git checkout 001-sales-dashboard

# 2. Install dependencies
uv sync

# 3. Copy environment variable template
cp .env.example .env
# Edit .env if needed (no required vars for CSV-based Phase 1)

# 4. Run the dashboard
uv run streamlit run dashboard/app.py
```

The dashboard opens at http://localhost:8501

## Verify It Works

With the sample dataset, the dashboard should show:

| Metric | Expected Value |
|--------|---------------|
| Total Sales | ~$650,000 – $700,000 |
| Total Orders | 482 |
| Categories shown | Electronics, Accessories, Audio, Wearables, Smart Home |
| Regions shown | North, South, East, West |

Try the following to confirm all features work:
- [ ] Toggle trend chart between Daily and Monthly
- [ ] Select a date range in the sidebar — all charts update
- [ ] Filter by one category — KPI card shows both overall and filtered totals
- [ ] Clear all filters — dashboard returns to full dataset view
- [ ] Verify summary table values match the bar chart values

## Running Tests

```bash
# Run all tests
uv run pytest

# Unit tests only
uv run pytest tests/unit/

# Integration tests only
uv run pytest tests/integration/

# With coverage
uv run pytest --cov=dashboard
```

## Docker Build & Run

```bash
# Build the container image
docker build -t shopsmart-dashboard .

# Run locally on port 8501
docker run -p 8501:8501 shopsmart-dashboard

# With environment variables (for future API-connected builds)
docker run -p 8501:8501 --env-file .env shopsmart-dashboard
```

## Project Layout

```text
dashboard/          ← Streamlit app (entry: app.py)
  services/         ← DataService class (data access + transformation)
  components/       ← UI components (KPI cards, charts, filters, table)
  utils/            ← Formatting helpers
tests/
  unit/             ← DataService, formatting, chart-data unit tests
  integration/      ← Full pipeline tests using real sales-data.csv
data/
  sales-data.csv    ← Source data (~1,000 rows)
```

## Adding a New Chart or Metric

1. Add the aggregation method to `DataService` (with unit test).
2. Add the Plotly figure builder to `components/charts.py` (with unit test).
3. Call both from `app.py` and render with `st.plotly_chart(...)`.
4. Add an integration test assertion to `tests/integration/test_data_pipeline.py`.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `DataLoadError` on startup | `data/sales-data.csv` missing or path wrong | Verify file exists at `data/sales-data.csv` from repo root |
| `DataValidationError` on startup | > 10% of rows are malformed | Check CSV for missing/negative `total_amount` or unparseable `date` values |
| Blank charts after filtering | Filter combination yields 0 rows | Expected behavior — check filter state and clear filters to reset |
| Trend chart shows only one point | Date range spans a single day and granularity is Monthly | Switch to Daily view |
