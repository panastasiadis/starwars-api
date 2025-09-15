from datetime import date
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


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

