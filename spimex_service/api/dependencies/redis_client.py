import asyncio
from datetime import (
    datetime,
    timedelta,
)

import redis.asyncio as redis
from core import settings
from redis.asyncio import Redis


class RedisHelper:
    def __init__(self, url: str):
        self.pool = redis.ConnectionPool.from_url(url=url)

    async def get_pool(self) -> redis.ConnectionPool:
        return self.pool

    async def schedule_cache_clear(self):
        while True:
            now = datetime.now()
            target_time = now.replace(
                hour=14,
                minute=11,
                second=0,
                microsecond=0,
            )

            if now >= target_time:
                target_time += timedelta(days=1)

            sleep_time = (target_time - now).total_seconds()
            print(
                f"[INFO] Очистка Redis запланирована через {sleep_time // 60:.0f} минут"
            )

            await asyncio.sleep(sleep_time)

            try:
                async with Redis.from_pool(self.pool) as redis:
                    print("[INFO] Очистка Redis...")
                    await redis.flushdb()
                    print("[INFO] Redis очищен")
            except Exception as e:
                print(f"[ERROR] Ошибка при очистке Redis: {e}")


redis_helper = RedisHelper(str(settings.Redis_Config.url))
