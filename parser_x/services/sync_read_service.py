from pathlib import Path
from typing import Any, List

import pandas as pd
from pandas import (
    DataFrame,
    Series,
)
from schemas import (
    ParseInfoSchema,
    moscow_now,
)


class ReadAndWriteService:
    def __init__(self, path_to_folder: Path) -> None:
        self.path_to_folder = path_to_folder

    def open_and_parse_exel_files(self) -> List[Any]:
        all_data = []  # Список для хранения данных всех файлов
        for file in self.path_to_folder.glob(pattern="*.xls"):
            df = pd.read_excel(file, header=7)
            print(f"Обрабатываю файл: {file.name} ✅")
            date = self._get_date_from_file_name(file_name=file.name)
            data = self._parse_info(df=df, date=date)
            all_data.extend(data)
        return all_data

    def get_data_from_excel_file(self) -> List[Any]:
        return self.open_and_parse_exel_files()

    def _parse_info(self, df: DataFrame, date: str) -> list[Any]:
        valid_rows = []

        for _, row in df.iterrows():
            try:
                valid_row = self._get_valid_rows(row=row, date=date)
                if valid_row is not None:
                    valid_rows.append(valid_row)
            except Exception:
                print("Ошибка при обработке строки")
        return valid_rows

    def _get_valid_rows(self, row: Series, date: str) -> ParseInfoSchema | None:
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
            print("Ошибка при обработке строки")

    def _get_date_from_file_name(self, file_name: str) -> str:
        split_file = file_name.split("_")
        year = split_file[2][:4]
        month = split_file[2][4:6]
        day = split_file[2][6:8]
        date = f"{day}.{month}.{year}"
        return date
