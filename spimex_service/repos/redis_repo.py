from redis.asyncio import (
    ConnectionPool,
    Redis,
)


class CacheRepository:
    def __init__(self, redis_pool: ConnectionPool):
        self.pool = redis_pool

    async def set_request(self, key: str, value: str):
        async with Redis.from_pool(self.pool) as redis:
            await redis.set(key, value)

    async def get_request_info(self, key: str):
        async with Redis.from_pool(self.pool) as redis:
            info = await redis.get(key)
            if info:
                return info.decode("utf-8")
