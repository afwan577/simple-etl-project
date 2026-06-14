from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
import pytest

from utils.extract import (
    get_page_url,
    fetch_page,
    _clean_text,
    parse_product_card,
    parse_products,
    scrape_main,
)


def test_get_page_url_page_one():
    assert get_page_url(1) == "https://fashion-studio.dicoding.dev"


def test_get_page_url_other_page():
    assert get_page_url(3) == "https://fashion-studio.dicoding.dev/page3"


def test_get_page_url_invalid_page():
    with pytest.raises(ValueError):
        get_page_url(0)


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

    result = parse_product_card(card, "2026-06-14 10:00:00")

    assert result["Title"] == "T-shirt Alpha"
    assert result["Price"] == "$12.50"
    assert result["Rating"] == "Rating: 4.8 / 5"
    assert result["Colors"] == "3 Colors"
    assert result["Size"] == "Size: M"
    assert result["Gender"] == "Gender: Men"


def test_parse_products_extracts_required_fields():
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

    products = parse_products(html, "2026-06-14 10:00:00")

    assert len(products) == 1
    assert products[0]["Title"] == "T-shirt Alpha"
    assert products[0]["Price"] == "$12.50"


def test_scrape_main():
    fake_products = [
        {
            "Title": "Test",
            "Price": "$10",
            "Rating": "4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "timestamp": "2026-06-14",
        }
    ]

    with patch("utils.extract.fetch_page", return_value="<html></html>"), \
         patch("utils.extract.parse_products", return_value=fake_products):

        result = scrape_main(start_page=1, end_page=1)

        assert len(result) == 1
        assert result[0]["Title"] == "Test"