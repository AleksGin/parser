from repos import DataBaseRepository


class SpimexApiService:
    def __init__(self, db_repo: DataBaseRepository) -> None:
        self.db_repo = db_repo

    async def get_last_trading_dates(self): ...

    async def get_dynamics(self): ...

    async def get_trading_results(self): ...
