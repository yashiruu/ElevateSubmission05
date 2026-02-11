import pytest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_page, scrape_all_products


# Mock HTML structure sesuai website submission
MOCK_HTML = """
<div class="product-details">
    <h3>Test Shirt</h3>
    <div>$10.0</div>
    <p>Rating: 4.5 / 5</p>
    <p>3 Colors</p>
    <p>Size: M</p>
    <p>Gender: Men</p>
</div>
"""


@patch("utils.extract.requests.Session.get")
def test_scrape_page_success(mock_get):
    mock_response = MagicMock()
    mock_response.text = MOCK_HTML
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    from utils.extract import _create_session
    session = _create_session()

    result = scrape_page(session, 1)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["title"] == "Test Shirt"
    assert result[0]["price"] == "$10.0"


@patch("utils.extract.scrape_page")
def test_scrape_all_products(mock_scrape_page):
    mock_scrape_page.return_value = [
        {
            "title": "Test",
            "price": "$10",
            "rating": "4.5",
            "colors": "3 Colors",
            "size": "Size: M",
            "gender": "Gender: Men",
        }
    ]

    result = scrape_all_products()

    assert isinstance(result, list)
    assert "timestamp" in result[0]

@patch("utils.extract.scrape_page")
def test_scrape_all_products_no_data(mock_scrape_page):
    mock_scrape_page.return_value = []

    import pytest
    from utils.extract import scrape_all_products

    with pytest.raises(RuntimeError):
        scrape_all_products()