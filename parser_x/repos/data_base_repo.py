from typing import (
    List,
)

from models import SpimexTraidingResut
from schemas import ParseInfoSchema
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from tools import pydantic_to_sqlalchemy


class DataBaseRepository:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def save_to_db(self, data: List[ParseInfoSchema]):
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
