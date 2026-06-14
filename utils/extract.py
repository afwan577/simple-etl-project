from __future__ import annotations

from datetime import datetime
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://fashion-studio.dicoding.dev"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DicodingDataEngineerSubmission/1.0)"
}


def get_page_url(page: int) -> str:
    """Menghasilkan URL halaman katalog Fashion Studio."""
    if page < 1:
        raise ValueError("Nomor halaman harus dimulai dari 1.")
    return BASE_URL if page == 1 else f"{BASE_URL}/page{page}"


def fetch_page(url: str, timeout: int = 20) -> str:
    """Mengambil HTML dari sebuah URL dengan error handling."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise RuntimeError(f"Gagal mengambil halaman {url}: {exc}") from exc


def _clean_text(text: str) -> str:
    return " ".join(text.split()) if text else ""


def parse_product_card(card, timestamp: str) -> Dict[str, str]:
    """Mengurai satu kartu produk menjadi dictionary."""
    try:
        title_el = card.select_one(".product-title") or card.select_one("h3")
        price_el = card.select_one(".price") or card.find(string=lambda text: text and "$" in text)
        details = [_clean_text(item.get_text(" ", strip=True)) for item in card.select("p")]

        rating = ""
        colors = ""
        size = ""
        gender = ""

        for detail in details:
            lower = detail.lower()
            if "rating" in lower or "/ 5" in lower or "invalid rating" in lower:
                rating = detail
            elif "color" in lower:
                colors = detail
            elif "size" in lower:
                size = detail
            elif "gender" in lower:
                gender = detail

        return {
            "Title": _clean_text(title_el.get_text(" ", strip=True)) if title_el else "",
            "Price": _clean_text(price_el.get_text(" ", strip=True) if hasattr(price_el, "get_text") else str(price_el)),
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "timestamp": timestamp,
        }
    except Exception as exc:
        raise RuntimeError(f"Gagal parsing kartu produk: {exc}") from exc


def parse_products(html: str, timestamp: str) -> List[Dict[str, str]]:
    """Mengurai seluruh produk dari HTML halaman."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".collection-card, .product-card, div[class*='card']")
        products = [parse_product_card(card, timestamp) for card in cards]
        return [product for product in products if any(product.values())]
    except Exception as exc:
        raise RuntimeError(f"Gagal mengurai HTML produk: {exc}") from exc


def scrape_main(start_page: int = 1, end_page: int = 50) -> List[Dict[str, str]]:
    """Mengambil data produk Fashion Studio dari halaman 1 sampai 50."""
    if start_page > end_page:
        raise ValueError("start_page tidak boleh lebih besar dari end_page.")

    extracted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_products: List[Dict[str, str]] = []

    for page in range(start_page, end_page + 1):
        try:
            html = fetch_page(get_page_url(page))
            all_products.extend(parse_products(html, extracted_at))
        except Exception as exc:
            # Tetap hentikan pipeline agar reviewer tahu sumber error secara jelas.
            raise RuntimeError(f"Scraping gagal pada halaman {page}: {exc}") from exc

    return all_products
