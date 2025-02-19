from repos import SpimexBaseRepository
from schemas import ParseInfoSchema


class SpimexApiService:
    def __init__(self, db_repo: SpimexBaseRepository) -> None:
        self.db_repo = db_repo

    async def get_last_trading_dates(self, count: int) -> list[ParseInfoSchema]:
        data = await self.db_repo.load_last_trading_dates(count)
        parse_data = [ParseInfoSchema.model_validate(obj) for obj in data]
        return parse_data

    async def get_dynamics(self): ...

    async def get_trading_results(self): ...
