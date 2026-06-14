from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql


def _is_enabled(value: str | None) -> bool:
    """Mengubah nilai konfigurasi string menjadi boolean."""
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def main() -> None:
    """Menjalankan proses ETL dari extract, transform, hingga load."""
    load_dotenv()

    start_page = int(os.getenv("START_PAGE", "1"))
    end_page = int(os.getenv("END_PAGE", "50"))
    csv_output_path = os.getenv("CSV_OUTPUT_PATH", "products.csv")

    raw_products = scrape_main(start_page=start_page, end_page=end_page)
    clean_products = transform_data(raw_products)

    save_to_csv(clean_products, csv_output_path)
    print(f"CSV berhasil dibuat: {csv_output_path}")

    if _is_enabled(os.getenv("LOAD_TO_GOOGLE_SHEETS")):
        spreadsheet_id = os.getenv("GOOGLE_SPREADSHEET_ID")
        worksheet_name = os.getenv("GOOGLE_WORKSHEET_NAME", "Sheet1")
        credentials_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "google-sheets-api.json")

        if not spreadsheet_id:
            raise ValueError("GOOGLE_SPREADSHEET_ID belum diisi di file .env")
        if not Path(credentials_file).exists():
            raise FileNotFoundError(
                f"File credential Google Sheets tidak ditemukan: {credentials_file}"
            )

        save_to_google_sheets(
            clean_products,
            spreadsheet_id=spreadsheet_id,
            worksheet_name=worksheet_name,
            credentials_file=credentials_file,
        )
        print(f"Google Sheets berhasil diperbarui: worksheet '{worksheet_name}'")

    if _is_enabled(os.getenv("LOAD_TO_POSTGRESQL")):
        table_name = os.getenv("POSTGRES_TABLE_NAME", "products")
        connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

        if not connection_string:
            raise ValueError("POSTGRES_CONNECTION_STRING belum diisi di file .env")

        save_to_postgresql(
            clean_products,
            table_name=table_name,
            connection_string=connection_string,
        )
        print(f"PostgreSQL berhasil diperbarui: tabel '{table_name}'")

    print(f"ETL selesai. {len(clean_products)} data bersih berhasil diproses.")


if __name__ == "__main__":
    main()
