from fastapi import APIRouter, Query

from ..api.dependencies import AsyncSessionDep


from ..exceptions import exception_handler
from ..services.swapi.sync import sync_swapi

router = APIRouter(prefix="/api")


@router.post("/sync")
@exception_handler(session_arg="session")
async def sync_data(session: AsyncSessionDep) -> SyncResponse:
    """Synchronize local database with SWAPI data."""

    entities_dict = await sync_swapi(session)
    return SyncResponse(
        status="success",
        message="Data synchronized successfully",
        synced_entities=entities_dict,
    )


