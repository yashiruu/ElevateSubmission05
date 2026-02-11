import pandas as pd
from utils.transform import transform_products


def test_transform_basic_cleaning():
    mock_data = [
        {
            "title": "Test Shirt",
            "price": "$10",
            "rating": "4.5 / 5",
            "colors": "3 Colors",
            "size": "Size: M",
            "gender": "Gender: Men",
            "timestamp": "2026-02-11",
        }
    ]

    df = transform_products(mock_data)

    assert isinstance(df, pd.DataFrame)
    assert df["price"].iloc[0] == 10 * 16000
    assert df["rating"].iloc[0] == 4.5
    assert df["colors"].iloc[0] == 3
    assert df["size"].iloc[0] == "M"
    assert df["gender"].iloc[0] == "Men"


def test_remove_invalid():
    mock_data = [
        {
            "title": "Unknown Product",
            "price": "$10",
            "rating": "4.5",
            "colors": "3 Colors",
            "size": "Size: M",
            "gender": "Gender: Men",
        }
    ]

    df = transform_products(mock_data)

    assert df.empty
