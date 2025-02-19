from typing import Annotated

from fastapi import Depends
from models import db_helper
from repos import SpimexBaseRepository
from services import SpimexApiService
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_repo(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
) -> SpimexBaseRepository:
    return SpimexBaseRepository(session=session)


async def get_spimex_service(
    db_repo: Annotated[
        SpimexBaseRepository,
        Depends(get_db_repo),
    ],
) -> SpimexApiService:
    return SpimexApiService(db_repo=db_repo)
