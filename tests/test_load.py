import pandas as pd
import pytest

from utils.load import save_to_csv


def test_save_to_csv_creates_file(tmp_path):
    df = pd.DataFrame(
        {
            "Title": ["T-shirt Alpha"],
            "Price": [160000.0],
            "Rating": [4.8],
            "Colors": [3],
            "Size": ["M"],
            "Gender": ["Men"],
            "timestamp": ["2026-06-14 10:00:00"],
        }
    )
    output = save_to_csv(df, tmp_path / "products.csv")
    assert output.exists()
    saved = pd.read_csv(output)
    assert saved.loc[0, "Title"] == "T-shirt Alpha"


def test_save_to_csv_rejects_empty_dataframe(tmp_path):
    with pytest.raises(RuntimeError):
        save_to_csv(pd.DataFrame(), tmp_path / "products.csv")
