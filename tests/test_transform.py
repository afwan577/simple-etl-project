import pandas as pd

from utils.transform import (
    transform_data,
    _extract_float,
    _extract_int,
    _clean_price,
    _remove_prefix,
)


def test_extract_float():
    assert _extract_float("Rating: 4.8 / 5") == 4.8


def test_extract_int():
    assert _extract_int("3 Colors") == 3


def test_clean_price():
    assert _clean_price("$10.00") == 160000.0


def test_remove_prefix():
    assert _remove_prefix("Size: XL", "Size") == "XL"


def test_transform_data_cleans_and_converts_columns():
    raw_data = [
        {
            "Title": "T-shirt Alpha",
            "Price": "$10.00",
            "Rating": "Rating: 4.8 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2026-06-14 10:00:00",
        }
    ]

    df = transform_data(raw_data)

    assert len(df) == 1
    assert df.loc[0, "Price"] == 160000.0
    assert df.loc[0, "Rating"] == 4.8
    assert df.loc[0, "Colors"] == 3
    assert df.loc[0, "Size"] == "M"
    assert df.loc[0, "Gender"] == "Men"


def test_transform_data_drops_duplicates_and_nulls():
    raw_data = [
        {
            "Title": "Jacket Beta",
            "Price": "$30.00",
            "Rating": "4.5 / 5",
            "Colors": "2 Colors",
            "Size": "Size: XL",
            "Gender": "Gender: Unisex",
            "timestamp": "2026-06-14 10:00:00",
        },
        {
            "Title": "Jacket Beta",
            "Price": "$30.00",
            "Rating": "4.5 / 5",
            "Colors": "2 Colors",
            "Size": "Size: XL",
            "Gender": "Gender: Unisex",
            "timestamp": "2026-06-14 10:00:00",
        },
    ]

    df = transform_data(raw_data)

    assert len(df) == 1


def test_transform_data_types_are_correct():
    raw_data = [
        {
            "Title": "Pants Gamma",
            "Price": "$25.00",
            "Rating": "4.2 / 5",
            "Colors": "4 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Men",
            "timestamp": "2026-06-14 10:00:00",
        }
    ]

    df = transform_data(raw_data)

    assert pd.api.types.is_string_dtype(df["Title"])
    assert pd.api.types.is_float_dtype(df["Price"])
    assert pd.api.types.is_float_dtype(df["Rating"])
    assert pd.api.types.is_integer_dtype(df["Colors"])