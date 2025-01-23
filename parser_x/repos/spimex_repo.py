import asyncio
from pathlib import Path
from typing import Any, List

from aiohttp import ClientSession
from bs4 import BeautifulSoup as BS
from bs4 import ResultSet


class SpimexRepository:
    def __init__(
        self,
        http_session: ClientSession,
        results_url: str,
        path_to_folder: Path,
        upload_url: str,
    ) -> None:
        self.http_session = http_session
        self.results_url = results_url
        self.upload_url = upload_url
        self.path_to_folder = path_to_folder
        self.page = "?page=page-{}"

    async def get_range_links_process(
        self,
        start_page: int,
        end_page: int,
    ) -> List[str]:
        if start_page < 1:
            raise ValueError("Стартовая страница должна быть больше или равна 1")

        all_links = []

        for page_number in range(start_page, end_page + 1):
            try:
                html = await self._fetch_page(page_number)
                items = await self._extract_process(
                    html=html,
                    name="a",
                    attrs={"class": "accordeon-inner__item-title link xls"},
                )
                dates = await self._extract_process(
                    html=html,
                    name="div",
                    attrs={"class": "accordeon-inner__item-inner__title"},
                )
                dates = await self._parse_for_date(dates=dates)
                links = await self._parse_html_for_link_and_valid_date_checker(
                    items=items,
                    dates=dates,
                )
                all_links.extend(links)
                print(f"Обработана страница {page_number}: найдено {len(dates)} ссылок")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Ошибка при обработке страницы {page_number}: {e}")

        return all_links

    async def get_specific_one(
        self,
        page_number: int,
        target_date: str,
    ):
        html = await self._fetch_page(page_number=page_number)
        items = await self._extract_process(
            html=html,
            name="a",
            attrs={"class": "accordeon-inner__item-title link xls"},
        )
        dates = await self._extract_process(
            html=html,
            name="div",
            attrs={"class": "accordeon-inner__item-inner__title"},
        )
        dates = await self._parse_for_date(dates)
        specific_one = await self._finder_for_specific_one(
            items=items,
            dates=dates,
            target_date=target_date,
        )

        return specific_one

    async def get_latest_results(self) -> list[Any]:
        html = await self._fetch_page(page_number=1)
        items = await self._extract_process(
            html=html,
            name="a",
            attrs={"class": "accordeon-inner__item-title link xls"},
        )
        latest_result = await self._latest_results_getter(items)

        return latest_result

    async def _latest_results_getter(self, items: ResultSet):
        latest_result = []

        for item in items:
            try:
                link = item.get("href")
                if link and len(link) >= 20:
                    latest_result.append(link)
                    break
            except Exception as e:
                print(f"При поиске что-то пошла не так: {e}")

        return latest_result

    async def _fetch_page(self, page_number: int):
        async with self.http_session.get(
            self.results_url + self.page.format(page_number)
        ) as response:
            response.raise_for_status()
            return await response.text()

    async def _parse_for_date(self, dates: ResultSet):
        dates_from_page = []

        for date in dates:
            try:
                if date:
                    span = date.find("span")
                    if span:
                        dates_from_page.append(span.text.strip())
                    else:
                        break
            except Exception as e:
                print(f"Ошибка при обработке даты: {e}")

        return dates_from_page

    async def _parse_html_for_link_and_valid_date_checker(
        self,
        items: ResultSet,
        dates: List[Any],
    ) -> list[Any]:
        links = []

        for item, date in zip(items, dates):
            try:
                year = int(date[-4::])
                if year >= 2023:
                    link = item.get("href")
                    if link and len(link) >= 20:
                        links.append(link)
                    else:
                        break
                else:
                    print(
                        f"Год в {date} невалиден: год должен быть больше или равен -> 2023"
                    )
            except ValueError:
                print(f"Ошибка извлечения года из даты: {date}")
                continue

        return links

    async def _extract_process(
        self,
        html: str,
        name: str,
        attrs: dict[str, Any],
    ) -> ResultSet:
        soup = BS(html, "html.parser")
        return soup.find_all(name=name, attrs=attrs)

    async def _finder_for_specific_one(
        self,
        items: ResultSet,
        dates: List[Any],
        target_date: str,
    ) -> List[Any]:
        specific_one = []

        for item, date in zip(items, dates):
            try:
                year = int(date[-4::])
                if year >= 2023 and target_date == date:
                    link = item.get("href")
                    if link and len(link) >= 20:
                        specific_one.append(link)
                        print(f"Искомая ссылка по дате: {target_date} найдена!")
                        break
                    else:
                        print("Не найдено!")
                        break
                else:
                    print(
                        f"Год в {date} невалиден: год должен быть больше или равен -> 2023"
                    )
            except ValueError:
                print(f"Ошибка извлечения года из даты: {date}")
                continue

        return specific_one
