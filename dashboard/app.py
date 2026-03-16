"""ShopSmart Sales Analytics Dashboard — Streamlit entry point."""

import sys
from pathlib import Path

# Ensure the repo root is on sys.path so `dashboard` is importable
# whether the app is run via `streamlit run dashboard/app.py` or `uv run`.
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from dashboard.services.data_service import (
    DataLoadError,
    DataService,
    DataValidationError,
    FilterState,
)
from dashboard.components.kpi_cards import render_kpi_cards

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="ShopSmart Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Data loading (cached for the server session lifetime)
# ---------------------------------------------------------------------------

DATA_PATH = Path(__file__).parent.parent / "data" / "sales-data.csv"


@st.cache_resource
def get_data_service() -> DataService | None:
    try:
        return DataService(DATA_PATH)
    except DataLoadError as exc:
        st.error(f"❌ Could not load data: {exc}")
        return None
    except DataValidationError as exc:
        st.error(f"❌ Data quality issue: {exc}")
        return None


data_service = get_data_service()

if data_service is None:
    st.stop()

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------

date_min, date_max = data_service.get_date_bounds()

if "filter_state" not in st.session_state:
    st.session_state.filter_state = FilterState(
        date_min=date_min,
        date_max=date_max,
        categories=[],
        regions=[],
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("📊 ShopSmart Sales Dashboard")
st.caption(f"Data loaded from `{DATA_PATH.name}` — freshness: rows through {date_max}")

st.divider()

# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------

filter_state: FilterState = st.session_state.filter_state
filtered_df = data_service.get_filtered_data(filter_state)
full_kpi = data_service.get_kpi_summary(data_service._df)
filtered_kpi = data_service.get_kpi_summary(filtered_df)

render_kpi_cards(overall=full_kpi, filtered=filtered_kpi)
