from typing import List

from models import SpimexTraidingResut
from schemas import ParseInfoSchema
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from tools import pydantic_to_sqlalchemy


class DataBaseRepository:
    def __init__(
        self,
        async_session: AsyncSession | None = None,
        sync_session: Session | None = None,
    ):
        self.async_session = async_session
        self.sync_session = sync_session

    async def async_save_to_db(self, data: List[ParseInfoSchema]):
        try:
            if self.async_session:
                objects = [pydantic_to_sqlalchemy(pydantic_obj=item) for item in data]
                await self.async_session.execute(
                    insert(SpimexTraidingResut), [obj.__dict__ for obj in objects]
                )
                await self.async_session.commit()
                print("Данные успешно добавлены в базу✅")

        except Exception as e:
            print(f"Ошибка при добавлении: {e}")

    def sync_save_to_db(self, data: List[ParseInfoSchema]):
        try:
            if self.sync_session:
                objects = [pydantic_to_sqlalchemy(pydantic_obj=item) for item in data]
                self.sync_session.execute(
                    insert(SpimexTraidingResut), [obj.__dict__ for obj in objects]
                )
                self.sync_session.commit()
                print("Данные успешно добавлены в базу✅")
        except Exception as e:
            print(f"Ошибка при добавлении: {e}")
