from core import settings
from models import Base
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

name = settings.DB_Config.name
host = settings.DB_Config.host
port = settings.DB_Config.port
user = settings.DB_Config.user
password = settings.DB_Config.password

DATABASE_URL: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

engine = create_async_engine(DATABASE_URL)
db_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


async def create_tables() -> None:
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Произошла ошибка при создании таблиц: {e}")
