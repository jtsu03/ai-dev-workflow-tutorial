# Contract: DataService

**Branch**: `001-sales-dashboard` | **Date**: 2026-03-16
**Module**: `dashboard/services/data_service.py`

## Overview

`DataService` is the single interface between the raw data source (CSV) and all UI
components. No component or utility module reads the CSV directly. This contract defines
the public API that all consumers (app.py, components, tests) depend on.

---

## Class: `DataService`

### Constructor

```python
DataService(data_path: str | Path)
```

**Behavior**:
- Loads the CSV at `data_path` into an internal Pandas DataFrame on construction.
- Validates columns, types, and data integrity (see Data Model validation rules).
- Raises `DataLoadError` if the file is missing or unreadable.
- Raises `DataValidationError` if > 10% of rows are dropped during validation.
- Decorated with `@st.cache_resource` at the call site (not inside the class).

---

### Method: `get_filtered_data`

```python
def get_filtered_data(self, filter_state: FilterState) -> pd.DataFrame
```

**Input**: A `FilterState` dataclass with fields:
- `date_min: datetime.date`
- `date_max: datetime.date`
- `categories: list[str]` — empty list means "all categories"
- `regions: list[str]` — empty list means "all regions"

**Output**: A Pandas DataFrame containing only rows matching all active filter constraints.

**Guarantees**:
- Returns a copy; modifications do not affect the internal DataFrame.
- If all filters are at their defaults, returns the full dataset.
- If the result is empty (zero rows), returns an empty DataFrame (does not raise).

---

### Method: `get_kpi_summary`

```python
def get_kpi_summary(self, df: pd.DataFrame) -> KPISummary
```

**Input**: Any Transaction DataFrame (full or filtered).

**Output**: `KPISummary` dataclass:
- `total_sales: float` — sum of `total_amount`
- `total_orders: int` — row count

**Guarantees**:
- If `df` is empty, returns `KPISummary(total_sales=0.0, total_orders=0)`.
- Result is deterministic for the same input.

---

### Method: `get_trend_data`

```python
def get_trend_data(
    self,
    df: pd.DataFrame,
    granularity: Literal["daily", "monthly"]
) -> list[TrendDataPoint]
```

**Input**: Any Transaction DataFrame + granularity string.

**Output**: List of `TrendDataPoint` sorted ascending by `period`:
- `period: datetime.date` — day (daily) or first day of month (monthly)
- `sales: float` — sum of `total_amount` for the period

**Guarantees**:
- Returns an empty list if `df` is empty.
- No gaps filled — periods with zero sales are omitted.

---

### Method: `get_category_summary`

```python
def get_category_summary(self, df: pd.DataFrame) -> list[SegmentSummary]
```

**Input**: Any Transaction DataFrame.

**Output**: List of `SegmentSummary` sorted **descending** by `total_sales`:
- `label: str` — category name
- `total_sales: float` — sum of `total_amount` for the category
- `total_orders: int` — row count for the category

**Guarantees**:
- All categories present in `df` are included (not filtered to the PRD-defined list).
- Returns empty list if `df` is empty.

---

### Method: `get_region_summary`

```python
def get_region_summary(self, df: pd.DataFrame) -> list[SegmentSummary]
```

Same contract as `get_category_summary` but grouped by `region`.

---

### Method: `get_date_bounds`

```python
def get_date_bounds(self) -> tuple[datetime.date, datetime.date]
```

**Output**: `(min_date, max_date)` of the full (unfiltered) dataset.
**Used by**: `filters.py` to set the default and boundary values for the date range picker.

---

### Method: `get_available_categories`

```python
def get_available_categories(self) -> list[str]
```

**Output**: Sorted list of all unique category values in the full dataset.
**Used by**: `filters.py` to populate the category multi-select widget.

---

### Method: `get_available_regions`

```python
def get_available_regions(self) -> list[str]
```

**Output**: Sorted list of all unique region values in the full dataset.
**Used by**: `filters.py` to populate the region multi-select widget.

---

## Exceptions

| Exception | Raised When |
|-----------|-------------|
| `DataLoadError` | CSV file missing, unreadable, or has incorrect column structure |
| `DataValidationError` | > 10% of rows dropped during validation (Data Integrity First principle) |

Both are subclasses of a project-level `DashboardError` base class.

---

## Usage Pattern (in `app.py`)

```python
# Initialize once per server session
data_service = get_data_service()  # wrapper applying @st.cache_resource

# Get filter state from session
filter_state = st.session_state.filter_state

# Full dataset KPIs (for "overall" display)
full_kpi = data_service.get_kpi_summary(data_service._df)

# Filtered dataset
filtered_df = data_service.get_filtered_data(filter_state)
filtered_kpi = data_service.get_kpi_summary(filtered_df)
trend_data = data_service.get_trend_data(filtered_df, st.session_state.granularity)
category_data = data_service.get_category_summary(filtered_df)
region_data = data_service.get_region_summary(filtered_df)
```
