"""Unit tests for formatting utilities."""

from dashboard.utils.formatting import format_currency, format_count


def test_format_currency_basic():
    assert format_currency(650000.0) == "$650,000"


def test_format_currency_zero():
    assert format_currency(0.0) == "$0"


def test_format_currency_large():
    assert format_currency(1_234_567.89) == "$1,234,568"


def test_format_count_basic():
    assert format_count(482) == "482"


def test_format_count_thousands():
    assert format_count(1000) == "1,000"


def test_format_count_zero():
    assert format_count(0) == "0"
