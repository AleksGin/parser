from typing import Sequence, Tuple
from sqlalchemy.engine.row import Row
from models import SpimexTradingResut
from sqlalchemy import (
    desc,
    select,
    func,
)
from sqlalchemy.ext.asyncio import AsyncSession


class SpimexBaseRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def load_last_trading_dates(
        self,
        count: int,
    ) -> Sequence[Row[Tuple[str, int]]]:
        stmt = (
            select(
                SpimexTradingResut.date,
                func.count(SpimexTradingResut.id).label("count"),
            )
            .group_by(SpimexTradingResut.date)
            .order_by(desc(SpimexTradingResut.date))
            .limit(count)
        )
        result = await self.session.execute(stmt)

        return result.all()

    async def load__dynamics(
        self,
        start_date: str,
        end_date: str,
        oil_id: str | None = None,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
    ): ...

    async def load_trading_results(self):
        pass
