import pandas as pd
from typing import List, Dict

USD_TO_IDR = 16000

def _to_dataframe(data: List[Dict]) -> pd.DataFrame:
    try:
        return pd.DataFrame(data)
    except Exception as e:
        raise ValueError(f"[ERROR] Failed to convert data to DataFrame: {e}")


def clean_price(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df["price"] = (
            df["price"]
            .astype(str)
            .str.extract(r"(\d+\.?\d*)")
            .astype(float)
            * USD_TO_IDR
        )
        return df
    except Exception as e:
        raise ValueError(f"[ERROR] Price transformation failed: {e}")


def clean_rating(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df["rating"] = (
            df["rating"]
            .astype(str)
            .str.extract(r"(\d+\.?\d*)")
            .astype(float)
        )
        return df
    except Exception as e:
        raise ValueError(f"[ERROR] Rating transformation failed: {e}")


def clean_colors(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df["colors"] = (
            df["colors"]
            .astype(str)
            .str.extract(r"(\d+)")
            .astype("int64")
        )
        return df
    except Exception as e:
        raise ValueError(f"[ERROR] Colors transformation failed: {e}")


def clean_size(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df["size"] = (
            df["size"]
            .astype(str)
            .str.replace("Size:", "", regex=False)
            .str.strip()
        )
        return df
    except Exception as e:
        raise ValueError(f"[ERROR] Size transformation failed: {e}")


def clean_gender(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df["gender"] = (
            df["gender"]
            .astype(str)
            .str.replace("Gender:", "", regex=False)
            .str.strip()
        )
        return df
    except Exception as e:
        raise ValueError(f"[ERROR] Gender transformation failed: {e}")


def remove_invalid_and_duplicate(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = df.dropna(subset=["title", "price", "rating", "colors", "size", "gender"])
        df = df.drop_duplicates()
        df = df[df["title"] != "Unknown Product"]
        return df
    except Exception as e:
        raise ValueError(f"[ERROR] Data filtering failed: {e}")


def transform_products(data: List[Dict]) -> pd.DataFrame:
    """
    Pipeline transformasi lengkap:
    - list → DataFrame
    - cleaning tiap kolom
    - hapus invalid & duplikat
    """
    df = _to_dataframe(data)

    df = clean_price(df)
    df = clean_rating(df)
    df = clean_colors(df)
    df = clean_size(df)
    df = clean_gender(df)
    df = remove_invalid_and_duplicate(df)
    
    print(f"[SUCCESS] Total data cleaned   : {len(df)}\n")
    print(df.info(), "\n")

    return df