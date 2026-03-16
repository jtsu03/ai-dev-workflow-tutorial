# Data Model: ShopSmart Sales Analytics Dashboard

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-16

## Entities

### Transaction

Represents a single sales record loaded from `data/sales-data.csv`.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `date` | `datetime.date` | Transaction date | Must be parseable; rows with invalid dates dropped with warning |
| `order_id` | `str` | Unique order identifier | Non-empty string |
| `product` | `str` | Product name | Non-empty string |
| `category` | `str` | Product category | One of: Electronics, Accessories, Audio, Wearables, Smart Home |
| `region` | `str` | Geographic region | One of: North, South, East, West |
| `quantity` | `int` | Units sold | Positive integer |
| `unit_price` | `float` | Price per unit (USD) | Positive float |
| `total_amount` | `float` | Total transaction value (USD) | Positive float; validated against `quantity × unit_price` |

**Runtime representation**: A Pandas `DataFrame` with the columns above. Loaded once by
`DataService` on startup; all downstream processing operates on views/copies of this DataFrame.

---

### FilterState

Represents the current set of active filter constraints applied to the Transaction dataset.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `date_min` | `datetime.date` | Min date in dataset | Start of selected date range (inclusive) |
| `date_max` | `datetime.date` | Max date in dataset | End of selected date range (inclusive) |
| `categories` | `list[str]` | All categories | Selected product categories; empty list = no filter |
| `regions` | `list[str]` | All regions | Selected geographic regions; empty list = no filter |

**Stored in**: `st.session_state` under key `filter_state`.
**Applied by**: `DataService.get_filtered_data(filter_state)` which returns a filtered copy
of the Transaction DataFrame.

---

### KPISummary

Aggregated top-line metrics derived from a Transaction DataFrame (filtered or unfiltered).

| Field | Type | Description |
|-------|------|-------------|
| `total_sales` | `float` | Sum of `total_amount` across all rows |
| `total_orders` | `int` | Count of rows (transactions) |

**Produced by**: `DataService.get_kpi_summary(df: DataFrame) -> KPISummary`
**Used by**: `kpi_cards.py` — called twice (full DF + filtered DF) to render dual values.

---

### TrendDataPoint

A single time-bucketed sales aggregate for the trend line chart.

| Field | Type | Description |
|-------|------|-------------|
| `period` | `datetime.date` | Start of the time bucket (day or month) |
| `sales` | `float` | Sum of `total_amount` for the period |

**Produced by**: `DataService.get_trend_data(df, granularity: Literal["daily", "monthly"]) -> list[TrendDataPoint]`
**Granularity**: `"daily"` uses `resample("D")`; `"monthly"` uses `resample("MS")`.

---

### SegmentSummary

Aggregated sales and order count for a single dimension value (category or region).

| Field | Type | Description |
|-------|------|-------------|
| `label` | `str` | Segment name (e.g., "Electronics", "North") |
| `total_sales` | `float` | Sum of `total_amount` for this segment |
| `total_orders` | `int` | Count of transactions for this segment |

**Produced by**:
- `DataService.get_category_summary(df) -> list[SegmentSummary]` — sorted descending by `total_sales`
- `DataService.get_region_summary(df) -> list[SegmentSummary]` — sorted descending by `total_sales`

**Used by**: `charts.py` (bar charts) and `summary_table.py` (aggregated table).

---

## Data Flow

```text
data/sales-data.csv
        │
        ▼
DataService.__init__()
  • Loads CSV into raw DataFrame
  • Validates columns and types
  • Drops/logs malformed rows
  • Caches via @st.cache_resource
        │
        ├─── get_filtered_data(FilterState) ──► filtered DataFrame
        │           │
        │           ├─── get_kpi_summary()      ──► KPISummary (filtered)
        │           ├─── get_trend_data()        ──► list[TrendDataPoint]
        │           ├─── get_category_summary()  ──► list[SegmentSummary]
        │           └─── get_region_summary()    ──► list[SegmentSummary]
        │
        └─── get_kpi_summary(full_df) ──► KPISummary (unfiltered, for dual KPI display)
```

---

## Validation Rules

- Rows where `total_amount` is null, zero, or negative are dropped and logged as warnings.
- Rows where `date` cannot be parsed are dropped and logged as warnings.
- If more than 10% of rows are dropped during validation, the dashboard surfaces an error
  state (Constitution Principle I: Data Integrity First).
- Unknown category or region values are accepted (not dropped) but flagged in a warning
  banner so users are aware of unexpected data.
