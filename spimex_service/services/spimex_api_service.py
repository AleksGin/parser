from repos import SpimexBaseRepository
from schemas import (
    DynamicsDataSchema,
    TradingDateSchema,
)


class SpimexApiService:
    def __init__(self, db_repo: SpimexBaseRepository) -> None:
        self.db_repo = db_repo

    async def get_last_trading_dates(
        self,
        count: int,
    ) -> list[TradingDateSchema]:
        data = await self.db_repo.load_last_trading_dates(count)
        parse_data = [
            TradingDateSchema(date=row[0], total_trade_count=row[1]) for row in data
        ]
        return parse_data

    async def get_dynamics(
        self,
        start_date: str,
        end_date: str,
        oil_id: str,
        type_id: str,
        basis_id: str,
    ) -> list[DynamicsDataSchema]:
        data = await self.db_repo.load_dynamics(
            start_date=start_date,
            end_date=end_date,
            oil_id=oil_id,
            type_id=type_id,
            basis_id=basis_id,
        )
        result = [DynamicsDataSchema.model_validate(row) for row in data]
        return result

    async def get_trading_results(self): ...
