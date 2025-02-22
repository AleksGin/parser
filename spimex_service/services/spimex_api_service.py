import json

from repos import (
    CacheRepository,
    SpimexBaseRepository,
)
from schemas import (
    DynamicsDataSchema,
    TradingDateSchema,
)
from tools import redis_form_keys


class SpimexApiService:
    def __init__(
        self,
        db_repo: SpimexBaseRepository,
        cache_repo: CacheRepository,
    ) -> None:
        self.db_repo = db_repo
        self.cache_repo = cache_repo

    async def get_last_trading_dates(
        self,
        count: int,
    ) -> list[TradingDateSchema]:
        cache_key = self._get_cache_key(redis_form_keys.TRADING_DATE, count)

        cached_data = await self._check_in_cache(
            key=cache_key,
            schema=TradingDateSchema,
        )
        if cached_data:
            return cached_data
        else:
            data = await self.db_repo.load_last_trading_dates(count)
            parse_data = [
                TradingDateSchema(date=row[0], total_trade_count=row[1]) for row in data
            ]
            await self._set_to_cache(
                key=cache_key,
                value=parse_data,
            )
            return parse_data

    async def get_dynamics(
        self,
        start_date: str,
        end_date: str,
        oil_id: str,
        type_id: str,
        basis_id: str,
    ) -> list[DynamicsDataSchema]:
        cache_key = self._get_cache_key(
            redis_form_keys.DYNAMICS_KEY,
            start_date,
            end_date,
            oil_id,
            type_id,
            basis_id,
        )

        cached_data = await self._check_in_cache(
            key=cache_key,
            schema=DynamicsDataSchema,
        )
        if cached_data:
            return cached_data
        else:
            data = await self.db_repo.load_dynamics(
                start_date=start_date,
                end_date=end_date,
                oil_id=oil_id,
                type_id=type_id,
                basis_id=basis_id,
            )

            result = [DynamicsDataSchema.model_validate(row) for row in data]
            await self._set_to_cache(key=cache_key, value=result)
            return result

    async def get_trading_results(
        self,
        oil_id: str,
        type_id: str,
        basis_id: str,
    ) -> list[DynamicsDataSchema]:
        cache_key = self._get_cache_key(
            redis_form_keys.LAST_TRADE_DATA_KEY,
            oil_id,
            type_id,
            basis_id,
        )

        cached_data = await self._check_in_cache(
            key=cache_key,
            schema=DynamicsDataSchema,
        )
        if cached_data:
            return cached_data
        else:
            data = await self.db_repo.load_last_trading_results(
                oil_id=oil_id,
                type_id=type_id,
                basis_id=basis_id,
            )

            parse_data = [DynamicsDataSchema.model_validate(*data)]
            await self._set_to_cache(key=cache_key, value=parse_data)
            return parse_data

    async def _set_to_cache(self, key: str, value):
        serialized_value = json.dumps([item.model_dump() for item in value])
        await self.cache_repo.set_request(
            key=key,
            value=serialized_value,
        )

    async def _check_in_cache(self, key, schema):
        cached_data = await self.cache_repo.get_request_info(key=key)
        if cached_data:
            return [schema(**item) for item in json.loads(cached_data)]

    def _get_cache_key(self, key_template: str, *args) -> str:
        return key_template.format(*args)
