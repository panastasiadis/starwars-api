from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from ..api.schemas import PaginatedResponse, T
from ..database.models import Character, Film, Starship
from ..exceptions import NotFoundError, exception_handler


class GetService:
    """Generic service class for retrieving and paginating database entities."""
    def __init__(self, model, session: AsyncSession, filter_field: str = "name"):
        self.model = model
        self.session = session
        self.filter_field = filter_field

    @exception_handler()
    async def get(self, id: UUID):
        """Retrieve a single entity by its UUID or raise NotFoundError."""
        entity = await self.session.get(self.model, id)
        if not entity:
            raise NotFoundError(
                detail=f"{self.model.__name__} with id `{id}` not found",
            )
        return entity

    @exception_handler()
    async def get_paginated(
        self,
        filter_value: Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> PaginatedResponse[T]:
        """Retrieve a paginated list of entities with optional filtering."""
        query, count_query = await self._build_base_query(filter_value)
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()
        result = await self.session.execute(query.offset(offset).limit(limit))
        items = result.scalars().all()

        return PaginatedResponse[T](
            total=total,
            offset=offset,
            limit=limit,
            items=items,
        )

    async def _build_base_query(self, filter_value: Optional[str] = None):
        """Build a base SQL query and count query with optional filtering by field."""
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)

        if filter_value:
            field = getattr(self.model, self.filter_field, None)
            if field is not None:
                query = query.where(field.ilike(f"%{filter_value}%"))
                count_query = count_query.where(field.ilike(f"%{filter_value}%"))

        return query, count_query

