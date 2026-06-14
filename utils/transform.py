from __future__ import annotations

import re
from typing import Iterable, Mapping

import pandas as pd

EXCHANGE_RATE = 16000
INVALID_TITLES = {"unknown product", ""}


def _extract_float(value) -> float | None:
    text = str(value)
    match = re.search(r"\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def _extract_int(value) -> int | None:
    text = str(value)
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def _clean_price(value) -> float | None:
    text = str(value).replace(",", "")
    number = _extract_float(text)
    return number * EXCHANGE_RATE if number is not None else None


def _remove_prefix(value, prefix: str) -> str:
    text = str(value).strip()
    return re.sub(rf"^{prefix}\s*:\s*", "", text, flags=re.IGNORECASE).strip()


def transform_data(raw_data: Iterable[Mapping]) -> pd.DataFrame:
    """Membersihkan dan mengubah tipe data hasil scraping."""
    try:
        df = pd.DataFrame(list(raw_data))
        expected_columns = ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]
        for column in expected_columns:
            if column not in df.columns:
                df[column] = None

        df = df[expected_columns].copy()
        df["Title"] = df["Title"].astype(str).str.strip()
        df["Price"] = df["Price"].apply(_clean_price)
        df["Rating"] = df["Rating"].apply(_extract_float)
        df["Colors"] = df["Colors"].apply(_extract_int)
        df["Size"] = df["Size"].apply(lambda value: _remove_prefix(value, "Size"))
        df["Gender"] = df["Gender"].apply(lambda value: _remove_prefix(value, "Gender"))
        df["timestamp"] = df["timestamp"].astype(str).str.strip()

        df.replace({"": pd.NA, "None": pd.NA, "nan": pd.NA}, inplace=True)
        df.dropna(inplace=True)
        df = df[~df["Title"].str.lower().isin(INVALID_TITLES)]
        df.drop_duplicates(inplace=True)

        df = df.astype(
            {
                "Title": "string",
                "Price": "float64",
                "Rating": "float64",
                "Colors": "int64",
                "Size": "string",
                "Gender": "string",
                "timestamp": "string",
            }
        )
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as exc:
        raise RuntimeError(f"Transformasi data gagal: {exc}") from exc
