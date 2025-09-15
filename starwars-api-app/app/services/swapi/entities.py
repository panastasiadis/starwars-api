from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel
from sqlmodel import SQLModel

from ...database.models import Character, Film, Starship
from ...api.schemas import CharacterSWAPICreate, FilmSWAPICreate, StarshipSWAPICreate


class EntityType(Enum):
    """Enumeration of SWAPI entity types with endpoints, schemas, and ORM models."""

    FILM = ("films", FilmSWAPICreate, Film)
    CHARACTER = ("people", CharacterSWAPICreate, Character)
    STARSHIP = ("starships", StarshipSWAPICreate, Starship)

    def __init__(self, endpoint: str, parsed_cls, orm_cls):
        self._endpoint = endpoint
        self._parsed_cls = parsed_cls
        self._orm_cls = orm_cls

    @property
    def endpoint(self) -> str:
        """Return the SWAPI endpoint for this entity type."""
        return self._endpoint

    @property
    def parsed_class(self):
        """Return the Pydantic schema class for parsing SWAPI data."""
        return self._parsed_cls

    @property
    def orm_class(self):
        """Return the SQLAlchemy ORM class for this entity type."""
        return self._orm_cls


@dataclass
class EntityRecord:
    """Container linking ORM and parsed Pydantic objects for an entity."""

    orm: SQLModel
    parsed: BaseModel
