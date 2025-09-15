from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel

from ..utils import parse_value

T = TypeVar("T")


class SyncResponse(BaseModel):
    """Response model for synchronization results."""

    status: str
    message: str = None
    synced_entities: dict[str, int] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    total: int
    offset: int
    limit: int
    items: List[T]


class UUIDRef(BaseModel):
    """Reference model containing UUID."""

    id: UUID


class BaseFilm(BaseModel):
    """Base schema for a film entity."""

    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: date


class BaseCharacter(BaseModel):
    """Base schema for a character entity."""

    name: str
    height: Optional[int] = None
    mass: Optional[int] = None
    hair_color: str
    skin_color: str
    eye_color: str
    gender: str
    birth_year: str


class BaseStarship(BaseModel):
    """Base schema for a starship entity."""

    name: str
    model: str
    manufacturer: str
    cost_in_credits: Optional[int] = None
    length: Optional[float] = None
    max_atmosphering_speed: Optional[int] = None
    crew: str
    passengers: Optional[int] = None
    cargo_capacity: Optional[int] = None
    consumables: Optional[str] = None
    hyperdrive_rating: Optional[float] = None
    MGLT: Optional[int] = None
    starship_class: str


class SWAPIParsedModel(BaseModel, ABC):
    """Abstract base class for parsed SWAPI models."""

    swapi_url: str

    @classmethod
    @abstractmethod
    def from_swapi(cls, data: dict) -> "SWAPIParsedModel":
        """Create an instance from raw SWAPI JSON."""
        raise NotImplementedError("`from_swapi` must be implemented in subclasses")


class FilmSWAPICreate(SWAPIParsedModel, BaseFilm):
    """Schema for creating a film from SWAPI data."""

    character_urls: List[str]
    starship_urls: List[str]

    @classmethod
    def from_swapi(cls, data: dict):
        return cls(
            swapi_url=data["url"],
            title=data.get("title"),
            episode_id=int(data.get("episode_id")),
            opening_crawl=data.get("opening_crawl"),
            director=data.get("director"),
            producer=data.get("producer"),
            release_date=data.get("release_date"),
            character_urls=data.get("characters", []),
            starship_urls=data.get("starships", []),
        )


class CharacterSWAPICreate(SWAPIParsedModel, BaseCharacter):
    """Schema for creating a character from SWAPI data."""

    @classmethod
    def from_swapi(cls, data: dict):
        return cls(
            swapi_url=data["url"],
            name=data["name"],
            height=parse_value(data["height"], "int"),
            mass=parse_value(data["mass"], "int"),
            hair_color=data.get("hair_color"),
            skin_color=data.get("skin_color"),
            eye_color=data.get("eye_color"),
            birth_year=data.get("birth_year"),
            gender=data.get("gender"),
        )


class StarshipSWAPICreate(SWAPIParsedModel, BaseStarship):
    """Schema for creating a starship from SWAPI data."""

    pilot_urls: List[str]

    @classmethod
    def from_swapi(cls, data: dict):
        return cls(
            swapi_url=data["url"],
            name=data["name"],
            model=data["model"],
            manufacturer=data["manufacturer"],
            cost_in_credits=parse_value(data.get("cost_in_credits"), "int"),
            length=parse_value(data.get("length"), "float"),
            max_atmosphering_speed=parse_value(
                data.get("max_atmosphering_speed"), "int"
            ),
            crew=data.get("crew"),
            passengers=parse_value(data.get("passengers"), "int"),
            cargo_capacity=parse_value(data.get("cargo_capacity"), "int"),
            consumables=data.get("consumables"),
            hyperdrive_rating=parse_value(data.get("hyperdrive_rating"), "float"),
            MGLT=parse_value(data.get("MGLT"), "int"),
            starship_class=data["starship_class"],
            pilot_urls=data.get("pilots", []),
        )


class FilmRead(BaseFilm):
    """Read schema for film with relations."""

    id: UUID
    characters: List[UUIDRef]
    starships: List[UUIDRef]


class CharacterRead(BaseCharacter):
    """Read schema for character with relations."""

    films: List[UUIDRef]
    starships: List[UUIDRef]


class StarshipRead(BaseStarship):
    """Read schema for starship with relations."""

    id: UUID
    pilots: List[UUIDRef]
    films: List[UUIDRef]


class PaginatedFilmRead(PaginatedResponse[FilmRead]):
    """Paginated response for films."""

    items: List[FilmRead]


class PaginatedCharacterRead(PaginatedResponse[CharacterRead]):
    """Paginated response for characters."""

    items: List[CharacterRead]


class PaginatedStarshipRead(PaginatedResponse[StarshipRead]):
    """Paginated response for starships."""

    items: List[StarshipRead]
