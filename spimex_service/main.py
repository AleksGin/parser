from contextlib import asynccontextmanager

import uvicorn
from api import spimex_info_router
from core import settings
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.include_router(spimex_info_router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.AppConfig.host,
        port=settings.AppConfig.port,
        reload=True,
    )
