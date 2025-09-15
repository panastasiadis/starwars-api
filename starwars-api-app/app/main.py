from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from .api.router import router
from .exceptions import add_exception_handlers

description = """
Star Wars API is a simple API for managing the Star Wars universe.
"""

app = FastAPI(
    title="Star Wars API",
    description=description,
    docs_url=None,
    redoc_url=None,
    version="0.1.0",
)

app.include_router(router)
add_exception_handlers(app)


@app.get("/")
async def root() -> dict:
    """Root endpoint returning an introduction message."""
    return {"message": "Welcome to the Star Wars API!"}


@app.get("/docs", include_in_schema=False)
async def scalar_docs():
    """Serve Scalar API documentation dynamically."""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
