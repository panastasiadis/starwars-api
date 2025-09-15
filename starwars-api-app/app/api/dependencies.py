from typing import Annotated

from fastapi import Depends

from ..database.session import AsyncSession, get_session
from ..services.get_services import (
    CharacterGetService,
    FilmGetService,
    StarshipGetService,
)


# Async database session dependency
AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_film_service(session: AsyncSessionDep) -> FilmGetService:
    """Provide FilmGetService with injected session."""

    return FilmGetService(session)


def get_character_service(session: AsyncSessionDep) -> CharacterGetService:
    """Provide CharacterGetService with injected session."""

    return CharacterGetService(session)


def get_starship_service(session: AsyncSessionDep) -> StarshipGetService:
    """Provide StarshipGetService with injected session."""

    return StarshipGetService(session)

FilmServiceDep = Annotated[FilmGetService, Depends(get_film_service)]
CharacterServiceDep = Annotated[CharacterGetService, Depends(get_character_service)]
StarshipServiceDep = Annotated[StarshipGetService, Depends(get_starship_service)]
