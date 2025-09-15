from unittest.mock import AsyncMock, Mock

import httpx
import pytest

from ..utils import fetch_json, parse_float, parse_int, parse_value


# -------------------------
# Test fetch_json
# -------------------------
@pytest.mark.asyncio
async def test_fetch_json_success():
    # Create a synchronous mock response
    mock_response = Mock()
    mock_response.json.return_value = {"key": "value"}  # synchronous
    mock_response.raise_for_status.return_value = None

    # Create async mock client
    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response  # get() is async

    result = await fetch_json(mock_client, "https://fake.url")
    assert result == {"key": "value"}


@pytest.mark.asyncio
async def test_fetch_json_raises():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=None, response=None
    )

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    import pytest

    from app.utils import fetch_json

    with pytest.raises(httpx.HTTPStatusError):
        await fetch_json(mock_client, "https://fake.url")


# -------------------------
# Test parse_int
# -------------------------
def test_parse_int_valid():
    assert parse_int("1,000") == 1000
    assert parse_int("42") == 42


def test_parse_int_invalid():
    assert parse_int("abc") is None
    assert parse_int(None) is None


# -------------------------
# Test parse_float
# -------------------------
def test_parse_float_valid():
    assert parse_float("1,234.56") == 1234.56
    assert parse_float("3.14") == 3.14


def test_parse_float_invalid():
    assert parse_float("abc") is None
    assert parse_float(None) is None


# -------------------------
# Test parse_value
# -------------------------
@pytest.mark.parametrize(
    "value, value_type, expected",
    [
        ("100", "int", 100),
        ("1,000", "int", 1000),
        ("3.14", "float", 3.14),
        ("1,234.56", "float", 1234.56),
        ("unknown", "int", None),
        ("n/a", "float", None),
        ("none", "str", None),
        ("hello", "str", "hello"),
        ("", "str", None),
    ],
)
def test_parse_value(value, value_type, expected):
    assert parse_value(value, value_type) == expected
