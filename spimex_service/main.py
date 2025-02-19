from fastapi import FastAPI
import uvicorn
from core import settings
from api import spimex_info_router



app = FastAPI()

app.include_router(spimex_info_router)


if __name__ == "__main__":
    uvicorn.run(
        app="fastapi_app:app",
        host=settings.AppConfig.host,
        port=settings.AppConfig.port,
        reload=True,
    )
