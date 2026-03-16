"""Number and currency formatting helpers."""


def format_currency(value: float) -> str:
    """Format a float as a USD currency string, e.g. 650000.0 → '$650,000'."""
    return f"${value:,.0f}"


def format_count(value: int) -> str:
    """Format an integer with comma separators, e.g. 1000 → '1,000'."""
    return f"{value:,}"
