import asyncio
from pathlib import Path

from aiohttp import ClientSession
from core import settings
from database import (
    create_tables,
    db_session,
)
from repos import (
    DataBaseRepository,
    SpimexRepository,
)
from services import (
    DownloadService,
    ReadAndWriteService,
)


async def main():
    await create_tables()
    print("Таблицы успешно созданы!✅")

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
        read_and_write_service = ReadAndWriteService(
            path_to_folder=Path(settings.SPX_Config.path_to_folder),
        )
        print("ReadAndWrite сервис инициализирован ✅")

        files_to_download = await spimex_repo.get_latest_results()
        print("Самый свежий файл скачен ✅")

        for file in files_to_download:
            await download_service.download_file(file)

        data = read_and_write_service.get_data_from_excel_file()
        print(f"Обработано записей: {len(data)} ✅")

        if data:
            print("Данные направлены✅")
            async with db_session() as session:
                db_repo = DataBaseRepository(session=session)
                await db_repo.save_to_db(data)


if __name__ == "__main__":
    asyncio.run(main())
