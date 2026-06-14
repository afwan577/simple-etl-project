from unittest.mock import Mock, patch
import pytest
from bs4 import BeautifulSoup

from utils.extract import (
    fetch_page,
    _clean_text,
    parse_product_card,
    scrape_main,
)


def test_fetch_page_success():
    with patch("utils.extract.requests.get") as mock_get:
        response = Mock()
        response.text = "<html></html>"
        response.raise_for_status.return_value = None

        mock_get.return_value = response

        result = fetch_page("https://example.com")

        assert result == "<html></html>"


def test_clean_text():
    assert _clean_text("  hello   world  ") == "hello world"


def test_parse_product_card():
    html = """
    <div class="collection-card">
        <h3 class="product-title">T-shirt Alpha</h3>
        <span class="price">$12.50</span>
        <p>Rating: 4.8 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    """

    card = BeautifulSoup(html, "html.parser").select_one(".collection-card")

    result = parse_product_card(card, "2026-06-14")

    assert result["Title"] == "T-shirt Alpha"
    assert result["Price"] == "$12.50"
    assert result["Rating"] == "Rating: 4.8 / 5"


def test_scrape_main():
    fake_products = [
        {
            "Title": "Test",
            "Price": "$10",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2026"
        }
    ]

    with patch("utils.extract.fetch_page") as mock_fetch, \
         patch("utils.extract.parse_products") as mock_parse:

        mock_fetch.return_value = "<html></html>"
        mock_parse.return_value = fake_products

        result = scrape_main(start_page=1, end_page=1)

        assert len(result) == 1
        assert result[0]["Title"] == "Test"