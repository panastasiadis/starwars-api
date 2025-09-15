from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config import db_settings

# Create a database engine to connect with database
engine = create_async_engine(
    url=db_settings.POSTGRES_URL,
    echo=False,
)


async def get_session():
    """Yield an async database session for dependency injection."""
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
