from datetime import datetime
from uuid import uuid4

import pytest
from sqlmodel import Session, SQLModel, create_engine

from ..database.models import Character, Film, Starship


# -------------------------
# Setup in-memory test DB
# -------------------------
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# -------------------------
# Test CRUD for Film
# -------------------------
def test_create_and_query_film(session):
    film = Film(
        id=uuid4(),
        title="A New Hope",
        episode_id=4,
        opening_crawl="It is a period of civil war...",
        director="George Lucas",
        producer="Gary Kurtz, Rick McCallum",
        release_date=datetime(1977, 5, 25),
        swapi_url="https://swapi.dev/api/films/1/",
    )
    session.add(film)
    session.commit()

    db_film = session.get(Film, film.id)
    assert db_film.title == "A New Hope"


# -------------------------
# Test CRUD for Character
# -------------------------
def test_create_and_query_character(session):
    char = Character(
        id=uuid4(),
        name="Luke Skywalker",
        hair_color="Blond",
        skin_color="Fair",
        eye_color="Blue",
        gender="Male",
        birth_year="19BBY",
        swapi_url="https://swapi.dev/api/people/1/",
    )
    session.add(char)
    session.commit()

    db_char = session.get(Character, char.id)
    assert db_char.name == "Luke Skywalker"


# -------------------------
# Test CRUD for Starship
# -------------------------
def test_create_and_query_starship(session):
    ship = Starship(
        id=uuid4(),
        name="X-wing",
        model="T-65",
        manufacturer="Incom Corporation",
        cost_in_credits=149999,
        length=12.5,
        max_atmosphering_speed=1050,
        crew="1",
        passengers=0,
        cargo_capacity=110,
        consumables="1 week",
        hyperdrive_rating=1.0,
        MGLT=100,
        starship_class="Starfighter",
        swapi_url="https://swapi.dev/api/starships/12/",
    )
    session.add(ship)
    session.commit()

    db_ship = session.get(Starship, ship.id)
    assert db_ship.name == "X-wing"


# -------------------------
# Test Film-Character relationship
# -------------------------
def test_film_character_relationship(session):
    film = Film(
        id=uuid4(),
        title="A New Hope",
        episode_id=4,
        opening_crawl="...",
        director="George Lucas",
        producer="Gary Kurtz, Rick McCallum",
        release_date=datetime(1977, 5, 25),
        swapi_url="https://swapi.dev/api/films/1/",
    )
    char = Character(
        id=uuid4(),
        name="Luke Skywalker",
        hair_color="Blond",
        skin_color="Fair",
        eye_color="Blue",
        gender="Male",
        birth_year="19BBY",
        swapi_url="https://swapi.dev/api/people/1/",
    )
    film.characters.append(char)
    session.add(film)
    session.commit()

    db_film = session.get(Film, film.id)
    assert len(db_film.characters) == 1
    assert db_film.characters[0].name == "Luke Skywalker"


# -------------------------
# Test Film-Starship relationship
# -------------------------
def test_film_starship_relationship(session):
    film = Film(
        id=uuid4(),
        title="A New Hope",
        episode_id=4,
        opening_crawl="...",
        director="George Lucas",
        producer="Gary Kurtz, Rick McCallum",
        release_date=datetime(1977, 5, 25),
        swapi_url="https://swapi.dev/api/films/1/",
    )
    ship = Starship(
        id=uuid4(),
        name="X-wing",
        model="T-65",
        manufacturer="Incom Corporation",
        consumables="1 week",
        crew="1",
        starship_class="Starfighter",
        swapi_url="https://swapi.dev/api/starships/12/",
    )
    film.starships.append(ship)
    session.add(film)
    session.commit()

    db_film = session.get(Film, film.id)
    assert len(db_film.starships) == 1
    assert db_film.starships[0].name == "X-wing"


# -------------------------
# Test Starship-Pilot relationship
# -------------------------
def test_starship_pilot_relationship(session):
    char = Character(
        id=uuid4(),
        name="Luke Skywalker",
        hair_color="Blond",
        skin_color="Fair",
        eye_color="Blue",
        gender="Male",
        birth_year="19BBY",
        swapi_url="https://swapi.dev/api/people/1/",
    )
    ship = Starship(
        id=uuid4(),
        name="X-wing",
        model="T-65",
        manufacturer="Incom Corporation",
        consumables="1 week",
        crew="1",
        starship_class="Starfighter",
        swapi_url="https://swapi.dev/api/starships/12/",
    )
    ship.pilots.append(char)
    session.add(ship)
    session.commit()

    db_ship = session.get(Starship, ship.id)
    assert len(db_ship.pilots) == 1
    assert db_ship.pilots[0].name == "Luke Skywalker"
