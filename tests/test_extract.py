from utils.extract import get_page_url, parse_products


def test_get_page_url_page_one():
    assert get_page_url(1) == "https://fashion-studio.dicoding.dev"


def test_get_page_url_other_page():
    assert get_page_url(3) == "https://fashion-studio.dicoding.dev/page3"


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
    assert products[0]["Rating"] == "Rating: 4.8 / 5"
    assert products[0]["Colors"] == "3 Colors"
    assert products[0]["Size"] == "Size: M"
    assert products[0]["Gender"] == "Gender: Men"
    assert products[0]["timestamp"] == "2026-06-14 10:00:00"
