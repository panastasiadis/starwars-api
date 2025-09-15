# StarWars API

A FastAPI-based asynchronous REST API for Star Wars data, featuring films, characters, and starships. Data is synchronized from the public SWAPI and stored in a PostgreSQL database. The project uses SQLModel ORM, Alembic for migrations, and is containerized with Docker.

## Features

- **Async FastAPI** backend
- **PostgreSQL** database (via Docker)
- **SQLModel** ORM
- **Alembic** migrations
- **SWAPI sync** endpoint
- **Paginated endpoints** for films, characters, starships
- **Typed responses** with Pydantic schemas
- **Unit tests** with pytest and httpx

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/starwars-api.git
cd starwars-api
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your database credentials:

```sh
cp .env.example .env
# Edit .env with your settings (see example below)
```

Example `.env`:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=starwars_db
```

### 3. Build and start with Docker Compose

```sh
docker compose up --build
```

This will start both the PostgreSQL database and the FastAPI app.

### 4. Apply database migrations

Open a shell in the API container:

```sh
docker compose exec srv-starwars-api bash
```

Run Alembic migrations:

```sh
uv run alembic upgrade head
```

### 5. Sync Star Wars data

Use the `/api/sync` endpoint to fetch and store SWAPI data:

```sh
curl -X POST http://localhost:8000/api/sync
```

## Usage

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Example endpoints:
  - `GET /api/films`
  - `GET /api/characters`
  - `GET /api/starships`
  - `POST /api/sync`

## Running Tests

Tests are located in `starwars-api-app/app/tests/`.

To run all tests:

```sh
docker compose exec srv-starwars-api bash
uv run pytest --cov=app
```
