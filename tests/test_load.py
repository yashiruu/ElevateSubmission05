from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql
from unittest.mock import patch, MagicMock
import pandas as pd
import pytest
import os

def test_save_to_csv(tmp_path):
    df = pd.DataFrame({"a": [1, 2]})
    file_path = tmp_path / "test.csv"

    save_to_csv(df, str(file_path))

    assert os.path.exists(file_path)


@patch("utils.load.build")
@patch("utils.load.Credentials.from_service_account_file")
def test_save_to_google_sheets(mock_creds, mock_build):
    df = pd.DataFrame({"a": [1, 2]})

    mock_service = MagicMock()
    mock_build.return_value = mock_service
    mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = {}

    # Buat dummy credential file
    open("google-sheets-api.json", "w").close()

    save_to_google_sheets(
        df,
        spreadsheet_id="dummy_id",
        credentials_path="google-sheets-api.json"
    )

    os.remove("google-sheets-api.json")


@patch("utils.load.create_engine")
def test_save_to_postgresql(mock_engine):
    df = pd.DataFrame({"a": [1, 2]})

    mock_engine_instance = MagicMock()
    mock_engine.return_value = mock_engine_instance

    save_to_postgresql(
        df,
        table_name="test_table",
        connection_uri="postgresql://dummy"
    )

    assert mock_engine.called

def test_google_sheets_missing_credentials():
    df = pd.DataFrame({"a":[1]})

    with pytest.raises(RuntimeError):
        save_to_google_sheets(
            df,
            spreadsheet_id="dummy",
            credentials_path="non_existent.json"
        )

def test_postgresql_missing_connection_uri():
    df = pd.DataFrame({"a":[1]})

    with pytest.raises(RuntimeError):
        save_to_postgresql(
            df,
            table_name="test",
            connection_uri=None
        )