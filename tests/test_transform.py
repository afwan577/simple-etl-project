import pandas as pd

from utils.transform import transform_data


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
        },
        {
            "Title": "Unknown Product",
            "Price": "$20.00",
            "Rating": "Invalid Rating",
            "Colors": "5 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Women",
            "timestamp": "2026-06-14 10:00:00",
        },
    ]
    df = transform_data(raw_data)

    assert len(df) == 1
    assert df.loc[0, "Title"] == "T-shirt Alpha"
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
        {
            "Title": None,
            "Price": "$15.00",
            "Rating": "4.0 / 5",
            "Colors": "1 Colors",
            "Size": "Size: S",
            "Gender": "Gender: Women",
            "timestamp": "2026-06-14 10:00:00",
        },
    ]
    df = transform_data(raw_data)
    assert len(df) == 1
    assert df.loc[0, "Title"] == "Jacket Beta"


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
    assert pd.api.types.is_string_dtype(df["Size"])
    assert pd.api.types.is_string_dtype(df["Gender"])
