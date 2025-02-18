from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from schemas import ParseInfoSchema
from services import SpimexApiService
from .dependencies import get_spimex_service


router = APIRouter(tags=["SpimexInfo"], prefix="/spimex_api_v1")


@router.get("", response_model=list[ParseInfoSchema])
async def last_trading_dates(
    spimex_service: Annotated[
        SpimexApiService,
        Depends(get_spimex_service),
    ],
    count: int,
):
    last_trading_dates = await spimex_service.get_last_trading_dates(count)
    return last_trading_dates
