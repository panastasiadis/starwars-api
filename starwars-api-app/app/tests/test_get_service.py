from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.api.schemas import PaginatedResponse
from app.database.models import Character, Film, Starship
from app.services.get_services import (
    CharacterGetService,
    FilmGetService,
    GetService,
    NotFoundError,
    StarshipGetService,
)

# -------------------------
# Unit tests using AsyncMock
# -------------------------


@pytest.mark.asyncio
async def test_get_returns_entity():
    mock_session = AsyncMock()
    entity_id = uuid4()
    mock_entity = Character(id=entity_id, name="Luke Skywalker")
    mock_session.get.return_value = mock_entity

    service = GetService(Character, session=mock_session)
    result = await service.get(entity_id)

    assert result == mock_entity
    mock_session.get.assert_awaited_once_with(Character, entity_id)


@pytest.mark.asyncio
async def test_get_raises_not_found():
    mock_session = AsyncMock()
    entity_id = uuid4()
    mock_session.get.return_value = None

    service = GetService(Character, session=mock_session)
    with pytest.raises(NotFoundError):
        await service.get(entity_id)


@pytest.mark.asyncio
async def test_get_paginated_returns_items():
    # Sample items
    items = [Character(id=uuid4(), name="Luke"), Character(id=uuid4(), name="Leia")]

    # Mock result object returned by session.execute()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = items
    mock_result.scalar_one.return_value = len(items)

    # Mock AsyncSession
    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result  # awaitable returns result

    service = GetService(Character, session=mock_session)

    # Call get_paginated
    result = await service.get_paginated(offset=0, limit=10)

    # Assertions
    assert isinstance(result, PaginatedResponse)
    assert result.total == len(items)
    assert result.items == items

    mock_session.execute.assert_called()  # ensure execute was called


# -------------------------
# Test subclasses
# -------------------------


def test_film_get_service_subclass():
    mock_session = AsyncMock()
    service = FilmGetService(session=mock_session)
    assert service.model == Film
    assert service.filter_field == "title"


def test_character_get_service_subclass():
    mock_session = AsyncMock()
    service = CharacterGetService(session=mock_session)
    assert service.model == Character
    assert service.filter_field == "name"


def test_starship_get_service_subclass():
    mock_session = AsyncMock()
    service = StarshipGetService(session=mock_session)
    assert service.model == Starship
    assert service.filter_field == "name"
