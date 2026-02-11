import pandas as pd
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import Optional
import os

# LOAD TO CSV
def save_to_csv(df: pd.DataFrame, filepath: str = "products.csv") -> None:
    try:
        df.to_csv(filepath, index=False)
        print(f"[SUCCESS] Data berhasil disimpan ke CSV: {filepath}")
    except Exception as e:
        raise IOError(f"Failed to save CSV file: {e}")
    

# LOAD TO GOOGLE SHEETS
def save_to_google_sheets(
    df: pd.DataFrame, 
    spreadsheet_id: str, 
    sheet_name: str = "Sheet1", 
    credentials_path: str = "google-sheets-api.json"
) -> None:
    try:
        if not spreadsheet_id:
            raise ValueError("Spreadsheet ID is required.")
        
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(
                f"Google credentials not found: {credentials_path}"
            )

        creds = Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        service = build("sheets", "v4", credentials=creds)

        values = [df.columns.tolist()] + df.values.tolist()

        body = {"values": values}

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            body=body
        ).execute()
        
        print("[SUCCESS] Data berhasil disimpan ke Google Sheets")

    except Exception as e:
        raise RuntimeError(f"Failed to save data to Google Sheets: {e}")
    
# LOAD TO POSTGRESQL
def save_to_postgresql(
    df: pd.DataFrame,
    table_name: str,
    connection_uri: str,
    if_exists: str = "replace"
) -> None:
    try:
        if not connection_uri:
            raise ValueError("Connection URI is required.")
        
        engine = create_engine(connection_uri)
        df.to_sql(
            table_name,
            engine,
            if_exists=if_exists,
            index=False
        )
        
        engine.dispose()
        
        print(f"[SUCCESS] Data berhasil disimpan ke PostgreSQL (table: {table_name})")
        
    except Exception as e:
        raise RuntimeError(f"Failed to save data to PostgreSQL: {e}")