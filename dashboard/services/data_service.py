"""DataService: single interface between the CSV data source and all UI components."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Literal

import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class DashboardError(Exception):
    """Base class for all dashboard errors."""


class DataLoadError(DashboardError):
    """Raised when the CSV file cannot be found or read."""


class DataValidationError(DashboardError):
    """Raised when too many rows are dropped during validation (>10%)."""


# ---------------------------------------------------------------------------
# Data model dataclasses
# ---------------------------------------------------------------------------

@dataclass
class FilterState:
    """Active filter constraints applied uniformly to all data views."""
    date_min: date | None = None
    date_max: date | None = None
    categories: list[str] = field(default_factory=list)
    regions: list[str] = field(default_factory=list)


@dataclass
class KPISummary:
    """Aggregated top-line metrics."""
    total_sales: float
    total_orders: int


@dataclass
class TrendDataPoint:
    """A single time-bucketed sales aggregate for the trend line chart."""
    period: date
    sales: float


@dataclass
class SegmentSummary:
    """Aggregated sales and order count for a single category or region."""
    label: str
    total_sales: float
    total_orders: int


# ---------------------------------------------------------------------------
# DataService
# ---------------------------------------------------------------------------

REQUIRED_COLUMNS = {
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
}


class DataService:
    """Encapsulates all data access and transformation for the dashboard."""

    def __init__(self, data_path: str | Path) -> None:
        path = Path(data_path)
        if not path.exists():
            raise DataLoadError(f"Data file not found: {path}")

        try:
            raw = pd.read_csv(path)
        except Exception as exc:
            raise DataLoadError(f"Could not read data file: {exc}") from exc

        missing = REQUIRED_COLUMNS - set(raw.columns)
        if missing:
            raise DataLoadError(f"CSV is missing required columns: {missing}")

        self._df = self._validate(raw)

    # ------------------------------------------------------------------
    # Internal validation
    # ------------------------------------------------------------------

    def _validate(self, df: pd.DataFrame) -> pd.DataFrame:
        original_count = len(df)

        # Parse dates
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        bad_dates = df["date"].isna()
        if bad_dates.any():
            logger.warning("Dropping %d rows with unparseable dates", bad_dates.sum())
        df = df[~bad_dates]

        # Drop rows with invalid total_amount
        bad_amount = df["total_amount"].isna() | (df["total_amount"] <= 0)
        if bad_amount.any():
            logger.warning("Dropping %d rows with invalid total_amount", bad_amount.sum())
        df = df[~bad_amount]

        df["date"] = df["date"].dt.date

        dropped = original_count - len(df)
        if original_count > 0 and dropped / original_count > 0.10:
            raise DataValidationError(
                f"{dropped}/{original_count} rows dropped during validation "
                f"(>{10}% threshold). Check data quality."
            )

        return df.reset_index(drop=True)

    # ------------------------------------------------------------------
    # Metadata helpers (used by filter controls)
    # ------------------------------------------------------------------

    def get_date_bounds(self) -> tuple[date, date]:
        """Return (min_date, max_date) of the full dataset."""
        return self._df["date"].min(), self._df["date"].max()

    def get_available_categories(self) -> list[str]:
        """Sorted list of all unique category values."""
        return sorted(self._df["category"].dropna().unique().tolist())

    def get_available_regions(self) -> list[str]:
        """Sorted list of all unique region values."""
        return sorted(self._df["region"].dropna().unique().tolist())

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def get_filtered_data(self, filter_state: FilterState) -> pd.DataFrame:
        """Return a copy of the DataFrame filtered by the given FilterState."""
        df = self._df.copy()

        if filter_state.date_min is not None:
            df = df[df["date"] >= filter_state.date_min]
        if filter_state.date_max is not None:
            df = df[df["date"] <= filter_state.date_max]
        if filter_state.categories:
            df = df[df["category"].isin(filter_state.categories)]
        if filter_state.regions:
            df = df[df["region"].isin(filter_state.regions)]

        return df.reset_index(drop=True)

    # ------------------------------------------------------------------
    # KPI aggregation
    # ------------------------------------------------------------------

    def get_kpi_summary(self, df: pd.DataFrame) -> KPISummary:
        """Return total sales and order count for the given DataFrame."""
        if df.empty:
            return KPISummary(total_sales=0.0, total_orders=0)
        return KPISummary(
            total_sales=float(df["total_amount"].sum()),
            total_orders=int(len(df)),
        )

    # ------------------------------------------------------------------
    # Trend data
    # ------------------------------------------------------------------

    def get_trend_data(
        self,
        df: pd.DataFrame,
        granularity: Literal["Daily", "Monthly"] = "Monthly",
    ) -> list[TrendDataPoint]:
        """Return time-bucketed sales aggregates sorted by period."""
        if df.empty:
            return []

        ts = df.copy()
        ts["date"] = pd.to_datetime(ts["date"])
        ts = ts.set_index("date")

        rule = "D" if granularity == "Daily" else "MS"
        resampled = ts["total_amount"].resample(rule).sum()

        return [
            TrendDataPoint(period=idx.date(), sales=float(val))
            for idx, val in resampled.items()
            if val > 0
        ]

    # ------------------------------------------------------------------
    # Segment summaries
    # ------------------------------------------------------------------

    def get_category_summary(self, df: pd.DataFrame) -> list[SegmentSummary]:
        """Return sales and order counts by category, sorted descending."""
        return self._segment_summary(df, "category")

    def get_region_summary(self, df: pd.DataFrame) -> list[SegmentSummary]:
        """Return sales and order counts by region, sorted descending."""
        return self._segment_summary(df, "region")

    def _segment_summary(self, df: pd.DataFrame, column: str) -> list[SegmentSummary]:
        if df.empty:
            return []
        grouped = (
            df.groupby(column)
            .agg(total_sales=("total_amount", "sum"), total_orders=("total_amount", "count"))
            .reset_index()
            .sort_values("total_sales", ascending=False)
        )
        return [
            SegmentSummary(
                label=row[column],
                total_sales=float(row["total_sales"]),
                total_orders=int(row["total_orders"]),
            )
            for _, row in grouped.iterrows()
        ]
