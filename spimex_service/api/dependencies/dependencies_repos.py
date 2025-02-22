from typing import Annotated

from fastapi import Depends
from models import db_helper
from redis.asyncio import ConnectionPool
from repos import (
    CacheRepository,
    SpimexBaseRepository,
)
from services import SpimexApiService
from sqlalchemy.ext.asyncio import AsyncSession

from .redis_client import redis_helper


async def get_db_repo(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
) -> SpimexBaseRepository:
    return SpimexBaseRepository(session=session)


async def get_cache_repo(
    pool: Annotated[
        ConnectionPool,
        Depends(redis_helper.get_pool),
    ],
) -> CacheRepository:
    return CacheRepository(redis_pool=pool)


async def get_spimex_service(
    db_repo: Annotated[
        SpimexBaseRepository,
        Depends(get_db_repo),
    ],
    cache_repo: Annotated[
        CacheRepository,
        Depends(get_cache_repo),
    ],
) -> SpimexApiService:
    return SpimexApiService(
        db_repo=db_repo,
        cache_repo=cache_repo,
    )
