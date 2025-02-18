from typing import (
    List,
    Sequence,
)

from models import SpimexTraidingResut
from schemas import ParseInfoSchema
from sqlalchemy import (
    desc,
    insert,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from tools import pydantic_to_sqlalchemy


class DataBaseRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def async_save_to_db(self, data: List[ParseInfoSchema]):
        try:
            if self.session:
                objects = [pydantic_to_sqlalchemy(pydantic_obj=item) for item in data]
                await self.session.execute(
                    insert(SpimexTraidingResut), [obj.__dict__ for obj in objects]
                )
                await self.session.commit()
                print("Данные успешно добавлены в базу✅")

        except Exception as e:
            print(f"Ошибка при добавлении: {e}")

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
