import asyncio

import httpx
from sqlalchemy import delete

from ...api.dependencies import AsyncSession
from ...config import SWAPI_BASE_URL
from ...database.models import (
    Character,
    Film,
    FilmCharacterLink,
    FilmStarshipLink,
    Starship,
    StarshipPilotLink,
)
from ...exceptions import SwapiUnavailableError
from ...utils import fetch_json
from .entities import EntityRecord, EntityType


async def clear_swapi_data(session: AsyncSession):
    """Delete all existing SWAPI-related records from the database."""
    await session.execute(delete(FilmCharacterLink))
    await session.execute(delete(FilmStarshipLink))
    await session.execute(delete(StarshipPilotLink))
    await session.execute(delete(Character))
    await session.execute(delete(Starship))
    await session.execute(delete(Film))

    await session.commit()


async def sync_swapi(session: AsyncSession):
    """Sync data from SWAPI into the local database and handle their relationships."""
    await clear_swapi_data(session)

    async with httpx.AsyncClient(base_url=SWAPI_BASE_URL) as client:
        # Fetch all endpoints concurrently
        try:
            responses = await asyncio.gather(
                *(fetch_json(client, entity.endpoint) for entity in EntityType)
            )
        except httpx.HTTPError as e:
            raise SwapiUnavailableError(str(e))
        # Load ORM objects into dicts
        entity_dicts: dict[EntityType, dict[str, EntityRecord]] = {}

        for entity, data_list in zip(EntityType, responses):
            entities = {}
            for data in data_list:
                parsed = entity.parsed_class.from_swapi(data)
                obj = entity.orm_class(**parsed.model_dump())
                session.add(obj)
                entities[data.get("url")] = EntityRecord(orm=obj, parsed=parsed)
            entity_dicts[entity] = entities

        films_dict = entity_dicts[EntityType.FILM]
        characters_dict = entity_dicts[EntityType.CHARACTER]
        starships_dict = entity_dicts[EntityType.STARSHIP]

        #  Build film <-> character + starship relations
        for film_rec in films_dict.values():
            film, film_parsed = film_rec.orm, film_rec.parsed
            film.characters.extend(
                characters_dict[url].orm for url in film_parsed.character_urls
            )
            film.starships.extend(
                starships_dict[url].orm for url in film_parsed.starship_urls
            )

        #  Build starship <-> pilot relations
        for starship_rec in starships_dict.values():
            starship, starship_parsed = starship_rec.orm, starship_rec.parsed
            starship.pilots.extend(
                characters_dict[url].orm for url in starship_parsed.pilot_urls
            )

        await session.commit()

        return {
            "films": len(films_dict),
            "characters": len(characters_dict),
            "starships": len(starships_dict),
        }
