import asyncio
from pathlib import Path

from aiohttp import ClientSession
from core import settings
from database import (
    create_sync_tables,
    sync_session,
)
from repos import (
    DataBaseRepository,
    SpimexRepository,
)
from services import (
    SyncDownloadService,
    ReadAndWriteService,
)
from requests import Session


async def main() -> None:
    create_sync_tables()
    print("______СИНХРОННАЯ ВЕРСИЯ______\n\nТаблицы успешно созданы!✅")

    http_session = Session()

    async with ClientSession() as async_session:
        spimex_repo = SpimexRepository(
            http_session=async_session,
            results_url=settings.SPX_Config.results_url,
            path_to_folder=Path(settings.SPX_Config.path_to_folder),
            upload_url=settings.SPX_Config.upload_url,
        )
        print("SpimexRepo инициализирован ✅")
        download_service = SyncDownloadService(
            upload_url=settings.SPX_Config.upload_url,
            path_to_folder=Path(settings.SPX_Config.path_to_folder),
            http_session=http_session,
        )
        print("DownloadService инициализирован ✅")
        sync_read_and_write_service = ReadAndWriteService(
            path_to_folder=Path(settings.SPX_Config.path_to_folder),
        )
        print("SyncReadAndWrite сервис инициализирован ✅")
        files_to_download = await spimex_repo.get_latest_results()
        print("Самый свежий файл скачен ✅")

        download_service.download_some_files(files_to_download)

        data = sync_read_and_write_service.get_data_from_excel_file()

        print(f"Обработано записей: {len(data)} ✅")

        if data:
            print("Данные направлены✅")
            with sync_session() as session:
                db_repo = DataBaseRepository(sync_session=session)
                db_repo.sync_save_to_db(data)


if __name__ == "__main__":
    asyncio.run(main())
