from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query

from ..api.dependencies import (
    AsyncSessionDep,
    CharacterServiceDep,
    FilmServiceDep,
    PaginationParamsDep,
    StarshipServiceDep,
)
from ..api.schemas import (
    CharacterRead,
    FilmRead,
    PaginatedCharacterRead,
    PaginatedFilmRead,
    PaginatedStarshipRead,
    StarshipRead,
    SyncResponse,
)
from ..exceptions import exception_handler
from ..services.swapi.sync import sync_swapi

router = APIRouter(prefix="/api")


@router.post("/sync")
@exception_handler(session_arg="session")
async def sync_data(session: AsyncSessionDep) -> SyncResponse:
    """Synchronize local database with SWAPI data."""

    entities_dict = await sync_swapi(session)
    return SyncResponse(
        status="success",
        message="Data synchronized successfully",
        synced_entities=entities_dict,
    )


@router.get("/films")
async def get_films(
    service: FilmServiceDep,
    pagionation: PaginationParamsDep,
    title: Optional[str] = Query(None, description="Filter by title"),
) -> PaginatedFilmRead:
    """Retrieve paginated list of films with optional title filter."""

    result = await service.get_paginated(
        filter_value=title,
        offset=pagionation.offset,
        limit=pagionation.limit,
    )
    return result


@router.get("/characters")
async def get_characters(
    service: CharacterServiceDep,
    pagionation: PaginationParamsDep,
    name: Optional[str] = Query(None, description="Filter by name"),
) -> PaginatedCharacterRead:
    """Retrieve paginated list of characters with optional name filter."""

    result = await service.get_paginated(
        filter_value=name,
        offset=pagionation.offset,
        limit=pagionation.limit,
    )
    return result



@router.get("/starships")
async def get_starships(
    service: StarshipServiceDep,
    pagionation: PaginationParamsDep,
    name: Optional[str] = Query(None, description="Filter by name"),
) -> PaginatedStarshipRead:
    """Retrieve paginated list of starships with optional name filter."""

    result = await service.get_paginated(
        filter_value=name,
        offset=pagionation.offset,
        limit=pagionation.limit,
    )
    return result


