from models import SpimexTradingResut
from sqlalchemy import desc, distinct, select
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
    ) -> list[str]:
        stmt = (
            select(distinct(SpimexTradingResut.date))
            .order_by(desc(SpimexTradingResut.date))
            .limit(count)
        )
        result = await self.session.scalars(stmt)

        return list(result.all())

    # async def load__dynamics(self, start_date: str, end_date: str) -> Sequence[SpimexBaseRepository]:
    #     stmt = (
    #         select(SpimexBaseRepository)
    #         .or
    #     )

    async def load_trading_results(self):
        pass
