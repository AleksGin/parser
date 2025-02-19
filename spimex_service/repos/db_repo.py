from typing import Sequence
from sqlalchemy import desc, select
from models import SpimexTraidingResut
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
    ) -> Sequence[SpimexTraidingResut]:
        stmt = (
            select(SpimexTraidingResut)
            .order_by(desc(SpimexTraidingResut.date))
            .limit(count)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def load__dynamics(self):
        pass

    async def load_trading_results(self):
        pass
