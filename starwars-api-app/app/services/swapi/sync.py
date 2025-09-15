from sqlalchemy import delete

from ...api.dependencies import AsyncSession
from ...database.models import (
    Character,
    Film,
    FilmCharacterLink,
    FilmStarshipLink,
    Starship,
    StarshipPilotLink,
)


async def clear_swapi_data(session: AsyncSession):
    """Delete all existing SWAPI-related records from the database."""
    await session.execute(delete(FilmCharacterLink))
    await session.execute(delete(FilmStarshipLink))
    await session.execute(delete(StarshipPilotLink))
    await session.execute(delete(Character))
    await session.execute(delete(Starship))
    await session.execute(delete(Film))

    await session.commit()


