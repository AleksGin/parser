from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
)

MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def moscow_now() -> datetime:
    return datetime.now(MOSCOW_TZ)


class ParseInfoSchema(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: float
    total: float
    count: int
    date: str
    created_on: str
    updated_on: str

    @computed_field
    def oil_id_getter(self) -> str:
        return self.exchange_product_id[:4]

    @computed_field
    def delivery_basis_id_getter(self) -> str:
        return self.exchange_product_id[4:7]

    @computed_field
    def delivery_type_id_getter(self) -> str:
        return self.exchange_product_id[-1]

    model_config = ConfigDict(from_attributes=True)


class TradingDateSchema(BaseModel):
    date: str
    total_trade_count: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "date": "DD-MM-YYYY",
                "total_trade_count": 999,
            }
        }
    }


class DynamicsDataSchema(TradingDateSchema):
    total_volumes: int
    total_trade_sum: int

    model_config = ConfigDict(from_attributes=True)
