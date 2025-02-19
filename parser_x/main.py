import asyncio
from pathlib import Path

from aiohttp import ClientSession
from core import settings
from models import db_helper
from repos import (
    DataBaseRepository,
    SpimexRepository,
)
from services import (
    AsyncReadAndWriteService,
    DownloadService,
)


async def main():
    await db_helper.async_create_tables()

    async with ClientSession() as http_session:
        spimex_repo = SpimexRepository(
            http_session=http_session,
            results_url=settings.SPX_Config.results_url,
            path_to_folder=Path(settings.SPX_Config.path_to_folder),
            upload_url=settings.SPX_Config.upload_url,
        )
        print("SpimexRepo инициализирован ✅")
        download_service = DownloadService(
            upload_url=settings.SPX_Config.upload_url,
            path_to_folder=Path(settings.SPX_Config.path_to_folder),
            http_session=http_session,
        )
        print("DownloadService инициализирован ✅")
        async_read_and_write_service = AsyncReadAndWriteService(
            path_to_folder=Path(settings.SPX_Config.path_to_folder),
        )
        print("AsyncReadAndWrite сервис инициализирован ✅")
        files_to_download = await spimex_repo.get_latest_results()
        print("Самый свежий файл скачен ✅")

        await download_service.download_some_files(files_to_download)

        data = await async_read_and_write_service.open_and_parse_excel_files()

        print(f"Обработано записей: {len(data)} ✅")

        if data:
            print("Данные направлены✅")
            async with db_helper.get_session() as session:
                db_repo = DataBaseRepository(session=session)
                await db_repo.save_to_db(data)


if __name__ == "__main__":
    asyncio.run(main())
