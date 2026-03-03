"""
Formatting utilities for consistent number display across StarGuard AI

Provides thousands separators, currency, percentages, and ratio formatting
"""

def format_number(value, decimals=0, prefix="", suffix=""):
    """
    Format number with thousands separator and optional prefix/suffix.

    Args:
        value: Numeric value to format
        decimals: Number of decimal places (default: 0)
        prefix: String to prepend (e.g., "$")
        suffix: String to append (e.g., "%", "×")

    Returns:
        Formatted string with comma separators

    Examples:
        >>> format_number(1234)
        '1,234'
        >>> format_number(1234.5, decimals=1)
        '1,234.5'
        >>> format_number(1234567, prefix="$")
        '$1,234,567'
        >>> format_number(0.85, decimals=1, suffix="%")
        '0.9%'
        >>> format_number(None)
        '—'
    """
    if value is None:
        return "—"

    try:
        formatted = f"{float(value):,.{decimals}f}"
        return f"{prefix}{formatted}{suffix}"
    except (ValueError, TypeError):
        return "—"


def format_currency(value, decimals=0, symbol="$"):
    """
    Format as currency with thousands separator

    Args:
        value: Numeric value to format
        decimals: Number of decimal places (default: 0)
        symbol: Currency symbol (default: "$")

    Returns:
        Formatted currency string

    Examples:
        >>> format_currency(1234)
        '$1,234'
        >>> format_currency(1234.56, decimals=2)
        '$1,234.56'
        >>> format_currency(1000000)
        '$1,000,000'
    """
    if value is None:
        return "—"

    try:
        return format_number(value, decimals, prefix=symbol)
    except Exception:
        return "—"


def format_percentage(value, decimals=1, multiply=True):
    """
    Format as percentage

    Args:
        value: Numeric value to format
        decimals: Number of decimal places (default: 1)
        multiply: If True, multiply by 100 (for 0.1234 → 12.3%)
                 If False, use as-is (for 12.34 → 12.3%)

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.1234)
        '12.3%'
        >>> format_percentage(0.05)
        '5.0%'
        >>> format_percentage(12.34, multiply=False)
        '12.3%'
    """
    if value is None:
        return "—"

    try:
        if multiply:
            display_value = float(value) * 100
        else:
            display_value = float(value)

        return f"{display_value:.{decimals}f}%"
    except (ValueError, TypeError):
        return "—"


def format_ratio(value, decimals=1, suffix="×"):
    """
    Format as ratio or multiplier

    Args:
        value: Numeric value to format
        decimals: Number of decimal places (default: 1)
        suffix: Suffix to append (default: "×")

    Returns:
        Formatted ratio string

    Examples:
        >>> format_ratio(2.5)
        '2.5×'
        >>> format_ratio(10)
        '10.0×'
        >>> format_ratio(1.234, decimals=2)
        '1.23×'
    """
    if value is None:
        return "—"

    try:
        return f"{float(value):.{decimals}f}{suffix}"
    except (ValueError, TypeError):
        return "—"


def format_large_number(value, decimals=1):
    """
    Format large numbers with K/M/B suffixes

    Args:
        value: Numeric value to format
        decimals: Number of decimal places (default: 1)

    Returns:
        Formatted string with suffix

    Examples:
        >>> format_large_number(1234)
        '1.2K'
        >>> format_large_number(1234567)
        '1.2M'
        >>> format_large_number(1234567890)
        '1.2B'
    """
    if value is None:
        return "—"

    try:
        value = float(value)

        if abs(value) >= 1_000_000_000:
            return f"{value / 1_000_000_000:.{decimals}f}B"
        elif abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.{decimals}f}M"
        elif abs(value) >= 1_000:
            return f"{value / 1_000:.{decimals}f}K"
        else:
            return format_number(value, decimals)
    except (ValueError, TypeError):
        return "—"


def format_confidence_score(value, decimals=0):
    """
    Format confidence score as percentage with color coding

    Args:
        value: Confidence score (0-1 or 0-100)
        decimals: Number of decimal places (default: 0)

    Returns:
        Formatted confidence string

    Examples:
        >>> format_confidence_score(0.87)
        '87.0%'
        >>> format_confidence_score(87)
        '87.0%'
    """
    if value is None:
        return "—"

    try:
        if 0 <= value <= 1:
            return format_percentage(value, decimals=decimals, multiply=True)
        else:
            return format_percentage(value, decimals=decimals, multiply=False)
    except (ValueError, TypeError):
        return "—"


# Convenience functions for common StarGuard AI metrics

def format_percent(value, decimals=1):
    """
    Shortcut for percentage formatting (expects 0-1 range, converts to 0-100).
    Alias for format_percentage(value, decimals=decimals, multiply=True).
    """
    return format_percentage(value, decimals=decimals, multiply=True)


def format_member_count(value):
    """Format member count with thousands separator"""
    return format_number(value, decimals=0)


def format_star_rating(value, decimals=1):
    """Format Star Rating (e.g., 3.5, 4.0)"""
    if value is None:
        return "—"
    try:
        return f"{float(value):.{decimals}f}"
    except (ValueError, TypeError):
        return "—"


def format_hedis_rate(value, decimals=1):
    """Format HEDIS rate as percentage"""
    return format_percentage(value, decimals=decimals)


def format_roi_value(value, decimals=1):
    """Format ROI ratio"""
    return format_ratio(value, decimals=decimals)


def format_cost_savings(value):
    """Format cost savings as currency"""
    return format_currency(value, decimals=0)
