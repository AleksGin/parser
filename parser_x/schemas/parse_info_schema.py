from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    ConfigDict,
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

    @property
    def oil_id_getter(self) -> str:
        return self.exchange_product_id[:4]

    @property
    def delivery_basis_id_getter(self) -> str:
        return self.exchange_product_id[4:7]

    @property
    def delivery_type_id_getter(self) -> str:
        return self.exchange_product_id[-1]

