"""Unit tests for DataService loading and KPI aggregation."""

import pytest
import pandas as pd
from pathlib import Path
from datetime import date

from dashboard.services.data_service import (
    DataService,
    DataLoadError,
    DataValidationError,
    FilterState,
    KPISummary,
)

REAL_DATA = Path(__file__).parent.parent.parent / "data" / "sales-data.csv"


# ---------------------------------------------------------------------------
# __init__ / loading
# ---------------------------------------------------------------------------

def test_loads_real_csv():
    svc = DataService(REAL_DATA)
    assert len(svc._df) > 0


def test_raises_data_load_error_for_missing_file(tmp_path):
    with pytest.raises(DataLoadError):
        DataService(tmp_path / "nonexistent.csv")


def test_drops_rows_with_invalid_total_amount(tmp_path):
    csv = tmp_path / "data.csv"
    # 20 rows: 18 valid, 1 negative, 1 blank — stays under the 10% drop threshold
    header = "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
    good = "".join(
        f"2024-01-{i:02d},ORD-{i:03d},Widget,Electronics,North,1,10.0,10.0\n"
        for i in range(1, 19)
    )
    bad = (
        "2024-01-19,ORD-019,Widget,Electronics,North,1,10.0,-5.0\n"
        "2024-01-20,ORD-020,Widget,Electronics,North,1,10.0,\n"
    )
    csv.write_text(header + good + bad)
    svc = DataService(csv)
    assert len(svc._df) == 18


def test_raises_validation_error_when_too_many_rows_dropped(tmp_path):
    csv = tmp_path / "data.csv"
    rows = ["date,order_id,product,category,region,quantity,unit_price,total_amount"]
    rows.append("2024-01-01,ORD-001,Widget,Electronics,North,1,10.0,10.0")
    for i in range(2, 12):
        rows.append(f"2024-01-{i:02d},ORD-{i:03d},Widget,Electronics,North,1,10.0,-1.0")
    csv.write_text("\n".join(rows))
    with pytest.raises(DataValidationError):
        DataService(csv)


# ---------------------------------------------------------------------------
# get_kpi_summary
# ---------------------------------------------------------------------------

def test_kpi_summary_correct_totals():
    svc = DataService(REAL_DATA)
    kpi = svc.get_kpi_summary(svc._df)
    assert kpi.total_orders == 482
    assert abs(kpi.total_sales - 116_500.21) < 1.0


def test_kpi_summary_empty_df():
    svc = DataService(REAL_DATA)
    kpi = svc.get_kpi_summary(pd.DataFrame(columns=svc._df.columns))
    assert kpi == KPISummary(total_sales=0.0, total_orders=0)
