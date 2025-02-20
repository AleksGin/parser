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


@router.get(
    "/last_trading_dates",
    response_model=list[TradingDateSchema],
)
async def last_trading_dates(
    spimex_service: Annotated[
        SpimexApiService,
        Depends(get_spimex_service),
    ],
    count: int,
) -> list[TradingDateSchema]:
    last_trading_dates = await spimex_service.get_last_trading_dates(count)
    return last_trading_dates


@router.get(
    "/dynamics_data",
    response_model=list[DynamicsDataSchema],
)
async def dynamics_data(
    spimex_service: Annotated[
        SpimexApiService,
        Depends(get_spimex_service),
    ],
    start_date: str,
    end_date: str,
    oil_id: str,
    type_id: str,
    basis_id: str,
) -> list[DynamicsDataSchema]:
    dynamics_data = await spimex_service.get_dynamics(
        start_date=start_date,
        end_date=end_date,
        oil_id=oil_id,
        type_id=type_id,
        basis_id=basis_id,
    )
    return dynamics_data
