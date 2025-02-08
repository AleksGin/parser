import asyncio
from pathlib import Path
import time
from typing import Any

import pandas as pd
from schemas import (
    ParseInfoSchema,
    moscow_now,
)


class AsyncReadAndWriteService:
    def __init__(self, path_to_folder: Path) -> None:
        self.path_to_folder = path_to_folder

    async def parse_excel_file(self, file: Path):
        return await asyncio.to_thread(self._parse_file_sync, file)

    def _parse_file_sync(self, file: Path) -> list[Any]:
        df = pd.read_excel(file, header=7)
        return self._parse_info(df, self._get_date_from_file_name(file.name))

    async def open_and_parse_excel_files(self) -> list[Any]:
        files = list(self.path_to_folder.glob("*.xls"))
        tasks = [self.parse_excel_file(file) for file in files]
        results = await asyncio.gather(*tasks)
        return [item for sublist in results for item in sublist]

    def _parse_info(self, df: pd.DataFrame, date: str) -> list[Any]:
        valid_rows = []

        for _, row in df.iterrows():
            try:
                valid_row = self._get_valid_rows(row=row, date=date)
                if valid_row is not None:
                    valid_rows.append(valid_row)
            except Exception:
                continue
        return valid_rows

    def _get_valid_rows(self, row: pd.Series, date: str) -> ParseInfoSchema | None:
        try:
            if row.iloc[14] != "-":
                exchange_product_id = row.iloc[1]
                exchange_product_name = row.iloc[2]
                oil_id = exchange_product_id[:4]
                delivery_basis_id = exchange_product_id[4:7]
                delivery_type_id = exchange_product_id[-1]
                delivery_basis_name = row.iloc[3]
                volume = row.iloc[4]
                total = row.iloc[5]
                count = row.iloc[14]

                data = ParseInfoSchema(
                    exchange_product_id=exchange_product_id,
                    exchange_product_name=exchange_product_name,
                    oil_id=oil_id,
                    delivery_basis_id=delivery_basis_id,
                    delivery_basis_name=delivery_basis_name,
                    delivery_type_id=delivery_type_id,
                    volume=float(volume),
                    total=float(total),
                    count=int(count),
                    date=date,
                    created_on=moscow_now().strftime("%Y-%m-%d %H:%M:%S"),
                    updated_on=moscow_now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                return data
        except Exception:
            pass

    def _get_date_from_file_name(self, file_name: str) -> str:
        split_file = file_name.split("_")
        year = split_file[2][:4]
        month = split_file[2][4:6]
        day = split_file[2][6:8]
        date = f"{day}.{month}.{year}"
        return date
