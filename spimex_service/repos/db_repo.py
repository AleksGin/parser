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
