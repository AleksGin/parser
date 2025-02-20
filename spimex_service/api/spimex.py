from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from schemas import (
    TradingDateSchema,
    DynamicsDataSchema,
)
from services import SpimexApiService

from .dependencies import get_spimex_service

router = APIRouter(tags=["SpimexInfo"], prefix="/spimex_api_v1")


@router.get("/last_trading_dates", response_model=list[TradingDateSchema])
async def last_trading_dates(
    spimex_service: Annotated[
        SpimexApiService,
        Depends(get_spimex_service),
    ],
    count: int,
) -> list[TradingDateSchema]:
    last_trading_dates = await spimex_service.get_last_trading_dates(count)
    return last_trading_dates


@router.get("/dynamics_data", response_model=list[DynamicsDataSchema])
async def dynamics_data(
    spimex_service: Annotated[
        SpimexApiService,
        Depends(get_spimex_service),
    ],
    start_date: str,
    end_date: str,
    oil_id: str,
    delivery_typle_id: str,
    delivery_basis_id: str,
): ...
