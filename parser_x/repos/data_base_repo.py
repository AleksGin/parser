from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ParseInfoSchema
from tools import pydantic_to_sqlalchemy


class DataBaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_to_db(self, data: List[ParseInfoSchema]):
        print("Данные получены✅")
        try:
            for item in data:
                sqlalchemy_obj = pydantic_to_sqlalchemy(pydantic_obj=item)
                self.session.add(sqlalchemy_obj)
            await self.session.commit()
            print("Данные успешно добавлены в базу✅")
        except Exception as e:
            print(f"Ошибка при добавлении: {e}")
