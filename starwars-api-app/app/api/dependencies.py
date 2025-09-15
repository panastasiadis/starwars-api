from typing import Annotated

from fastapi import Depends

from ..database.session import AsyncSession, get_session

# Async database session dependency
AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]


