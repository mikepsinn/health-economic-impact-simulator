"""Formatting utilities for report generation."""

def format_currency(amount: float, precision: int = 2) -> str:
    """Format currency with appropriate scale (B/T) and commas."""
    if abs(amount) >= 1e12:
        return f"${amount/1e12:,.{precision}f}T"
    elif abs(amount) >= 1e9:
        return f"${amount/1e9:,.{precision}f}B"
    elif abs(amount) >= 1e6:
        return f"${amount/1e6:,.{precision}f}M"
    else:
        return f"${amount:,.{precision}f}"

def format_percentage(value: float, precision: int = 1) -> str:
    """Format percentage with specified precision."""
    return f"{value:.{precision}f}%"

def format_number(value: float, precision: int = 0) -> str:
    """Format number with commas and specified precision."""
    return f"{value:,.{precision}f}"

def format_equation(equation: str) -> str:
    """Format equation in markdown code block."""
    return f"```\n{equation}\n```" 