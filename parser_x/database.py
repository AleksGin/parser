from core import settings
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

name = settings.DB_Config.name
host = settings.DB_Config.host
port = settings.DB_Config.port
user = settings.DB_Config.user
password = settings.DB_Config.password

"------------------------------ASYNC_PG------------------------------"

ASYNC_DATABASE_URL: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_db_session = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
)


async def async_create_tables() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Произошла ошибка при создании таблиц: {e}")


"------------------------------SYNC_PG------------------------------"

# SYNC_DATABASE_URL = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"

# sync_engine = create_engine(SYNC_DATABASE_URL)

# sync_session = sessionmaker(
#     sync_engine,
#     autocommit=False,
#     autoflush=False,
# )


# def create_sync_tables():
#     try:
#         with sync_engine.begin() as conn:
#             Base.metadata.create_all(conn)
#     except Exception as e:
#         print(f"Ошибка при создании таблиц (синхронно): {e}")
