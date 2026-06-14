import pandas as pd
from unittest.mock import Mock, MagicMock, patch

from utils.load import (
    save_to_google_sheets,
    save_to_postgresql,
)

def test_save_to_google_sheets():
    df = pd.DataFrame({"Title": ["Test"]})

    mock_worksheet = Mock()
    mock_spreadsheet = Mock()
    mock_client = Mock()

    mock_spreadsheet.worksheet.return_value = mock_worksheet
    mock_client.open_by_key.return_value = mock_spreadsheet

    with patch("gspread.authorize", return_value=mock_client), \
         patch("google.oauth2.service_account.Credentials.from_service_account_file"):

        result = save_to_google_sheets(
            df,
            "spreadsheet-id",
            "Sheet1",
            "credentials.json"
        )

        assert result == mock_worksheet
        mock_worksheet.clear.assert_called_once()


def test_save_to_postgresql():
    df = pd.DataFrame({"Title": ["Test"]})

    mock_engine = MagicMock()
    mock_connection = MagicMock()

    with patch("sqlalchemy.create_engine", return_value=mock_engine):
        mock_engine.begin.return_value.__enter__.return_value = mock_connection

        with patch.object(df, "to_sql") as mock_to_sql:
            result = save_to_postgresql(
                df,
                "products",
                "postgresql://test"
            )

            assert result is True
            mock_to_sql.assert_called_once()