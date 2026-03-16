"""KPI card components for Total Sales and Total Orders."""

import streamlit as st

from dashboard.services.data_service import KPISummary
from dashboard.utils.formatting import format_currency, format_count


def render_kpi_cards(overall: KPISummary, filtered: KPISummary) -> None:
    """Render Total Sales and Total Orders KPI cards.

    When filters are active and filtered totals differ from overall totals,
    both values are shown so users never lose sight of the full picture.
    """
    filters_active = (
        overall.total_sales != filtered.total_sales
        or overall.total_orders != filtered.total_orders
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Total Sales",
            value=format_currency(overall.total_sales),
            delta=format_currency(filtered.total_sales) + " filtered"
            if filters_active
            else None,
        )

    with col2:
        st.metric(
            label="Total Orders",
            value=format_count(overall.total_orders),
            delta=format_count(filtered.total_orders) + " filtered"
            if filters_active
            else None,
        )
