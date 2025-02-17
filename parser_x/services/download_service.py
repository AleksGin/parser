import asyncio
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import aiofiles
from aiohttp import ClientSession


class DownloadService:
    def __init__(
        self,
        upload_url: str,
        path_to_folder: Path,
        http_session: ClientSession,
    ) -> None:
        self.upload_url = upload_url
        self.path_to_folder = path_to_folder
        self.http_session = http_session

    async def download_file(self, item: str) -> None:
        try:
            file_name = Path(urlparse(item).path).name
            if not file_name:
                raise ValueError("Не удалось определить имя файла из URL")

            save_path = self.path_to_folder / file_name

            self.path_to_folder.mkdir(parents=True, exist_ok=True)

            async with self.http_session.get(self.upload_url + item) as response:
                if response.status == 200:
                    async with aiofiles.open(save_path, "wb") as file:
                        await file.write(await response.read())
                else:
                    print(f"Ошибка при загрузке: {response.status} - {response.reason}")
        except Exception as e:
            print(f"Ошибка при скачивании: {e}")

    async def download_some_files(self, items: List[str]) -> None:
        try:
            tasks = [self.download_file(item) for item in items]
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"Ошибка при скачивании: {e}")
