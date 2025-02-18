# from contextlib import asynccontextmanager
from typing import AsyncGenerator
from models import Base
from core import settings
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.session import AsyncSession


class DataBaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        max_overflow: int = 10,
        pool_size: int = 5,
    ) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def async_create_tables(self) -> None:
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            print(f"Произошла ошибка при создании таблиц: {e}")


db_helper = DataBaseHelper(
    str(settings.DB_Config.url),
    settings.DB_Config.echo,
    settings.DB_Config.echo_pool,
    settings.DB_Config.max_overflow,
    settings.DB_Config.pool_size,
)
