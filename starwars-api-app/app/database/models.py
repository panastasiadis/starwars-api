from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import BigInteger, Column, Field, Relationship, SQLModel


class FilmCharacterLink(SQLModel, table=True):
    """Link table for many-to-many relationship between films and characters."""

    film_id: UUID = Field(
        default_factory=uuid4,
        foreign_key="film.id",
        primary_key=True,
    )
    character_id: UUID = Field(
        default_factory=uuid4,
        foreign_key="character.id",
        primary_key=True,
    )


class FilmStarshipLink(SQLModel, table=True):
    """Link table for many-to-many relationship between films and starships."""

    film_id: UUID = Field(
        default_factory=uuid4,
        foreign_key="film.id",
        primary_key=True,
    )
    starship_id: UUID = Field(
        default_factory=uuid4,
        foreign_key="starship.id",
        primary_key=True,
    )


class StarshipPilotLink(SQLModel, table=True):
    """Link table for many-to-many relationship between starships and pilots."""

    starship_id: UUID = Field(
        default_factory=uuid4,
        foreign_key="starship.id",
        primary_key=True,
    )
    pilot_id: UUID = Field(
        default_factory=uuid4,
        foreign_key="character.id",
        primary_key=True,
    )


class Character(SQLModel, table=True):
    """Database model for Star Wars characters."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    height: Optional[int] = None
    mass: Optional[int] = None
    hair_color: str
    skin_color: str
    eye_color: str
    gender: str
    birth_year: str
    swapi_url: str

    films: List["Film"] = Relationship(
        back_populates="characters",
        link_model=FilmCharacterLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    starships: List["Starship"] = Relationship(
        back_populates="pilots",
        link_model=StarshipPilotLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Starship(SQLModel, table=True):
    """Database model for Star Wars starships."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    model: str
    manufacturer: str
    cost_in_credits: Optional[int] = Field(default=None, sa_column=Column(BigInteger))
    length: Optional[float] = None
    max_atmosphering_speed: Optional[int] = None
    crew: str
    passengers: Optional[int] = Field(default=None, sa_column=Column(BigInteger))
    cargo_capacity: Optional[int] = Field(default=None, sa_column=Column(BigInteger))
    consumables: str
    hyperdrive_rating: Optional[float] = None
    MGLT: Optional[int] = None
    starship_class: str
    swapi_url: str

    films: List["Film"] = Relationship(
        back_populates="starships",
        link_model=FilmStarshipLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    pilots: List[Character] = Relationship(
        back_populates="starships",
        link_model=StarshipPilotLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Film(SQLModel, table=True):
    """Database model for Star Wars films."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    episode_id: int
    opening_crawl: str
    director: str
    producer: str
    release_date: datetime
    swapi_url: str

    characters: List[Character] = Relationship(
        back_populates="films",
        link_model=FilmCharacterLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    starships: List[Starship] = Relationship(
        back_populates="films",
        link_model=FilmStarshipLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )
