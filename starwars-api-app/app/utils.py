from typing import Optional


def parse_int(value: str) -> Optional[int]:
    """Convert string to int if possible, else None."""
    try:
        return int(value.replace(",", ""))  # handle "1,000" style numbers
    except (ValueError, AttributeError):
        return None


def parse_float(value: str) -> Optional[float]:
    """Convert string to float if possible, else None."""
    try:
        return float(value.replace(",", ""))
    except (ValueError, AttributeError):
        return None


def parse_value(value: str, value_type: str):
    """Parse a string to int, float, or return original/None
    based on value_type and content."""
    if value in (None, "", "unknown", "n/a", "none"):
        return None
    if value_type == "int":
        return parse_int(value)
    if value_type == "float":
        return parse_float(value)
    return value
