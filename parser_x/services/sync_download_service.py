from pathlib import Path
from typing import List
from urllib.parse import urlparse

from requests import Session


class SyncDownloadService:
    def __init__(self, upload_url: str, path_to_folder: Path, http_session: Session):
        self.upload_url = upload_url
        self.path_to_folder = path_to_folder
        self.http_session = http_session

    def download_file(self, item: str):
        try:
            file_name = Path(urlparse(item).path).name
            save_path = self.path_to_folder / file_name
            self.path_to_folder.mkdir(parents=True, exist_ok=True)

            response = self.http_session.get(self.upload_url + item, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    file.write(response.content)
                # print(f"Файл {file_name} скачан!")
            else:
                print(f"Ошибка: {response.status_code}")

        except Exception as e:
            print(f"Ошибка скачивания: {e}")

    def download_some_files(self, items: List[str]):
        for item in items:
            self.download_file(item)
