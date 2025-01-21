import asyncio
from parser.core import settings
from models import Base, SpimexTraidingResut
from aiohttp import ClientSession


async def fetch_data():
    async with ClientSession() as session:
        url = settings.SPX_Config.url
        print(url)
        async with session.get(url) as response:
            return await response.json()

if __name__ == "__main__":
    asyncio.run(fetch_data())