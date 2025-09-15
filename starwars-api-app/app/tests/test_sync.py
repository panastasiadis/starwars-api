from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.swapi.sync import (
    SwapiUnavailableError,
    clear_swapi_data,
    sync_swapi,
)

# -------------------------
# Test clear_swapi_data
# -------------------------


@pytest.mark.asyncio
async def test_clear_swapi_data_calls_deletes_and_commit():
    mock_session = AsyncMock()

    await clear_swapi_data(mock_session)

    # Should call execute for all six tables
    assert mock_session.execute.call_count == 6

    # Ensure commit is called once
    mock_session.commit.assert_awaited_once()


# -------------------------
# Helper function to create mock execute results
# -------------------------


def make_mock_execute(items):
    """Returns an AsyncMock that mimics session.execute."""
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = items
    mock_result.scalar_one.return_value = len(items)
    return AsyncMock(return_value=mock_result)


# -------------------------
# Test sync_swapi happy path
# -------------------------


@pytest.mark.asyncio
@patch("app.services.swapi.sync.fetch_json")
async def test_sync_swapi_happy_path(mock_fetch_json):
    mock_session = AsyncMock()

    # Minimal mock SWAPI data
    mock_fetch_json.side_effect = [
        [
            {
                "url": "film1",
                "title": "A New Hope",
                "episode_id": 4,
                "opening_crawl": "",
                "director": "Lucas",
                "producer": "Gary",
                "release_date": "1977-05-25",
                "characters": ["char1"],
                "starships": ["starship1"],
            }
        ],
        [
            {
                "url": "char1",
                "name": "Luke",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
            }
        ],
        [
            {
                "url": "starship1",
                "name": "X-wing",
                "model": "T-65",
                "manufacturer": "Incom",
                "crew": "1",
                "consumables": "1 week",
                "starship_class": "fighter",
            }
        ],
    ]

    # Mock execute to handle any query
    mock_session.execute = make_mock_execute(items=[1])  # dummy items
    mock_session.commit = AsyncMock()
    mock_session.add = AsyncMock()

    result = await sync_swapi(mock_session)

    # Check returned counts
    assert result == {"films": 1, "characters": 1, "starships": 1}

    # Ensure session.add was called for each entity
    assert mock_session.add.call_count == 3

    # Commit was called at least once
    mock_session.commit.assert_awaited()


# -------------------------
# Test sync_swapi with network error
# -------------------------


@pytest.mark.asyncio
@patch("app.services.swapi.sync.fetch_json", new_callable=AsyncMock)
async def test_sync_swapi_raises_on_fetch_error(mock_fetch):
    mock_session = AsyncMock()
    mock_fetch.side_effect = httpx.HTTPError("Network error")

    with pytest.raises(SwapiUnavailableError):
        await sync_swapi(mock_session)


# -------------------------
# Test relationship building
# -------------------------


@pytest.mark.asyncio
@patch("app.services.swapi.sync.fetch_json")
async def test_sync_swapi_builds_relationships(mock_fetch_json):
    mock_session = AsyncMock()

    # Mock data with multiple relationships
    mock_fetch_json.side_effect = [
        [
            {
                "url": "film1",
                "title": "A New Hope",
                "episode_id": 4,
                "opening_crawl": "",
                "director": "Lucas",
                "producer": "Gary",
                "release_date": "1977-05-25",
                "characters": ["char1"],
                "starships": ["starship1"],
            }
        ],
        [
            {
                "url": "char1",
                "name": "Luke",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
            }
        ],
        [
            {
                "url": "starship1",
                "name": "X-wing",
                "model": "T-65",
                "manufacturer": "Incom",
                "crew": "1",
                "consumables": "1 week",
                "starship_class": "fighter",
                "pilots": ["char1"],
            }
        ],
    ]

    # Mock execute to handle any query
    mock_session.execute = make_mock_execute(items=[1])  # dummy items
    mock_session.commit = AsyncMock()
    mock_session.add = AsyncMock()

    result = await sync_swapi(mock_session)

    # Validate counts
    assert result == {"films": 1, "characters": 1, "starships": 1}

    # session.add should have been called for each entity
    assert mock_session.add.call_count == 3

    # commit was called at least once
    mock_session.commit.assert_awaited()
