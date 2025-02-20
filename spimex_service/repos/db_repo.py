from typing import Sequence, Tuple
from sqlalchemy.engine.row import Row
from models import SpimexTradingResut
from sqlalchemy import (
    Result,
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
                func.count(SpimexTradingResut.id).label("total_trade_count"),
            )
            .group_by(SpimexTradingResut.date)
            .order_by(desc(SpimexTradingResut.date))
            .limit(count)
        )
        result = await self.session.execute(stmt)

        return result.all()

    async def load_dynamics(
        self,
        start_date: str,
        end_date: str,
        oil_id: str,
        type_id: str,
        basis_id: str,
    ) -> Result[Tuple]:
        stmt = (
            select(
                SpimexTradingResut.date,
                func.sum(SpimexTradingResut.volume).label("total_volumes"),
                func.sum(SpimexTradingResut.count).label("total_trade_count"),
                func.sum(SpimexTradingResut.total).label("total_trade_sum"),
            )
            .where(
                SpimexTradingResut.oil_id == oil_id,
                SpimexTradingResut.delivery_type_id == type_id,
                SpimexTradingResut.delivery_basis_id == basis_id,
                SpimexTradingResut.date.between(start_date, end_date),
            )
            .group_by(SpimexTradingResut.date)
            .order_by(SpimexTradingResut.date.desc())
        )

        data = await self.session.execute(stmt)
        return data

    async def load_trading_results(self):
        pass
