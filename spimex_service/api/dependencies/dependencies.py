from typing import Annotated

from fastapi import Depends
from models import db_helper
from repos import DataBaseRepository
from services import SpimexApiService
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_repo(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
) -> DataBaseRepository:
    return DataBaseRepository(session=session)


async def get_spimex_service(
    db_repo: Annotated[
        DataBaseRepository,
        Depends(get_db_repo),
    ],
) -> SpimexApiService:
    return SpimexApiService(db_repo=db_repo)
