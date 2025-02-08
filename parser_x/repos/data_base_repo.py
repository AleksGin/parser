import time
from typing import List

from models import SpimexTraidingResut
from schemas import ParseInfoSchema
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from tools import pydantic_to_sqlalchemy


class DataBaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_to_db(self, data: List[ParseInfoSchema]):
        print("Данные получены✅")
        try:
            start = time.time()
            objects = [pydantic_to_sqlalchemy(pydantic_obj=item) for item in data]
            await self.session.execute(
                insert(SpimexTraidingResut), [obj.__dict__ for obj in objects]
            )
            await self.session.commit()
            end = time.time()
            print("Данные успешно добавлены в базу✅")
            print(f"Время {end - start} секунд")

        except Exception as e:
            print(f"Ошибка при добавлении: {e}")


# с циклом fore - Время 0.028119802474975586 секунд

# с execute - Время 0.015104055404663086 секунд

# с циклом for для 5 страниц - Время 0.7572510242462158 секунд

# с execute - Время 0.38246703147888184 секунд
