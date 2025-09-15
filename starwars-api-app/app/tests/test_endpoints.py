from unittest.mock import AsyncMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api.schemas import (
    CharacterRead,
    FilmRead,
    PaginatedCharacterRead,
    PaginatedFilmRead,
    PaginatedStarshipRead,
    StarshipRead,
    UUIDRef,
)
from app.main import app

client = TestClient(app)


# -----------------------------
# /api/sync
# -----------------------------
def test_sync_data():
    mock_response = {"films": 3, "characters": 10, "starships": 5}

    with patch("app.api.router.sync_swapi", new_callable=AsyncMock) as mock_sync:
        mock_sync.return_value = mock_response

        response = client.post("/api/sync")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["synced_entities"]["films"] == 3


# -----------------------------
# /api/films
# -----------------------------
def test_get_films():
    mock_film = FilmRead(
        id=uuid4(),
        title="A New Hope",
        episode_id=4,
        opening_crawl="Some crawl text",
        director="George Lucas",
        producer="Gary Kurtz",
        release_date="1977-05-25",
        characters=[],
        starships=[],
    )
    mock_paginated = PaginatedFilmRead(
        total=1,
        offset=0,
        limit=10,
        items=[mock_film],
    )

    with patch(
        "app.services.get_services.FilmGetService.get_paginated", new_callable=AsyncMock
    ) as mock_pg:
        mock_pg.return_value = mock_paginated

        response = client.get("/api/films?title=A+New+Hope")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "A New Hope"


def test_get_film_by_id():
    film_id = uuid4()
    mock_film = FilmRead(
        id=film_id,
        title="Empire Strikes Back",
        episode_id=5,
        opening_crawl="Some crawl text",
        director="Irvin Kershner",
        producer="Gary Kurtz",
        release_date="1980-05-17",
        characters=[UUIDRef(id=uuid4())],
        starships=[UUIDRef(id=uuid4())],
    )

    with patch(
        "app.services.get_services.FilmGetService.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_film

        response = client.get(f"/api/films/{film_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Empire Strikes Back"


# -----------------------------
# /api/characters
# -----------------------------
def test_get_characters():
    mock_char = CharacterRead(
        id=uuid4(),
        name="Luke Skywalker",
        height=172,
        mass=77,
        hair_color="Blond",
        skin_color="Fair",
        eye_color="Blue",
        gender="Male",
        birth_year="19BBY",
        films=[],
        starships=[],
    )
    mock_paginated = PaginatedCharacterRead(
        total=1,
        offset=0,
        limit=10,
        items=[mock_char],
    )

    with patch(
        "app.services.get_services.CharacterGetService.get_paginated",
        new_callable=AsyncMock,
    ) as mock_pg:
        mock_pg.return_value = mock_paginated

        response = client.get("/api/characters?name=Luke")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "Luke Skywalker"


def test_get_character_by_id():
    char_id = uuid4()
    mock_char = CharacterRead(
        id=char_id,
        name="Leia Organa",
        height=150,
        mass=49,
        hair_color="Brown",
        skin_color="Light",
        eye_color="Brown",
        gender="Female",
        birth_year="19BBY",
        films=[],
        starships=[],
    )

    with patch(
        "app.services.get_services.CharacterGetService.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_char

        response = client.get(f"/api/characters/{char_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Leia Organa"


# -----------------------------
# /api/starships
# -----------------------------
def test_get_starships():
    mock_ship = StarshipRead(
        id=uuid4(),
        name="X-wing",
        model="T-65 X-wing",
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
        pilots=[],
        films=[],
    )
    mock_paginated = PaginatedStarshipRead(
        total=1,
        offset=0,
        limit=10,
        items=[mock_ship],
    )

    with patch(
        "app.services.get_services.StarshipGetService.get_paginated",
        new_callable=AsyncMock,
    ) as mock_pg:
        mock_pg.return_value = mock_paginated

        response = client.get("/api/starships?name=X-wing")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["name"] == "X-wing"


def test_get_starship_by_id():
    ship_id = uuid4()
    mock_ship = StarshipRead(
        id=ship_id,
        name="TIE Fighter",
        model="Twin Ion Engine/Ln",
        manufacturer="Sienar Fleet Systems",
        cost_in_credits=75000,
        length=6.3,
        max_atmosphering_speed=1200,
        crew="1",
        passengers=0,
        cargo_capacity=65,
        consumables="2 days",
        hyperdrive_rating=1.0,
        MGLT=90,
        starship_class="Starfighter",
        pilots=[],
        films=[],
    )

    with patch(
        "app.services.get_services.StarshipGetService.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_ship

        response = client.get(f"/api/starships/{ship_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "TIE Fighter"
