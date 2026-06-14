from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_to_csv(df: pd.DataFrame, filepath: str = "products.csv") -> Path:
    """Menyimpan data bersih ke CSV."""
    try:
        if df.empty:
            raise ValueError("DataFrame kosong, tidak ada data yang disimpan.")
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        return output_path
    except Exception as exc:
        raise RuntimeError(f"Gagal menyimpan CSV: {exc}") from exc


def save_to_google_sheets(df: pd.DataFrame, spreadsheet_id: str, worksheet_name: str, credentials_file: str):
    """Menyimpan data ke Google Sheets. Opsional untuk target Skilled/Advanced."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet.clear()
        worksheet.update([df.columns.tolist()] + df.astype(str).values.tolist())
        return worksheet
    except Exception as exc:
        raise RuntimeError(f"Gagal menyimpan ke Google Sheets: {exc}") from exc


def save_to_postgresql(df: pd.DataFrame, table_name: str, connection_string: str):
    """Menyimpan data ke PostgreSQL. Opsional untuk target Advanced."""
    try:
        from sqlalchemy import create_engine

        engine = create_engine(connection_string)
        with engine.begin() as connection:
            df.to_sql(table_name, connection, if_exists="replace", index=False)
        return True
    except Exception as exc:
        raise RuntimeError(f"Gagal menyimpan ke PostgreSQL: {exc}") from exc
