import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

BASE_URL = "https://fashion-studio.dicoding.dev"
TOTAL_PAGES = 50
    
def _create_session() -> requests.Session:
    """
    Membuat session requests agar lebih efisien
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (compatible; ETL-Bot/1.0)"
        }
    )
    return session

def scrape_page(session: requests.Session, page: int) -> List[Dict]:
    """
    Mengambil data produk dari satu halaman website
    """
    products = []
    url = f"{BASE_URL}/page{page}" if page != 1 else BASE_URL

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch page {page}: {e}")
        return products

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="product-details")
    
    for card in cards:
        try:
            data = [
                el for el in card.find_all(recursive=False)
            ]
            
            if len(data) != 6:
                print(f"[WARNING] Unexpected structure: {len(data)} elements")
                continue
            
            products.append(
                {
                    "title": data[0].get_text(strip=True),
                    "price": data[1].get_text(strip=True),
                    "rating": data[2].get_text(strip=True),
                    "colors": data[3].get_text(strip=True),
                    "size": data[4].get_text(strip=True),
                    "gender": data[5].get_text(strip=True),
                }
            )

        except AttributeError as e:
            print(f"[WARNING] Skipped one product due to parsing issue: {e}")
            continue

    return products


def scrape_all_products() -> List[Dict]:
    session = _create_session()
    all_products: List[Dict] = []
    timestamp = datetime.utcnow().isoformat()

    try:
        for page in range(1, TOTAL_PAGES + 1):
            page_products = scrape_page(session, page)
            
            if not page_products:
                print(f"[WARNING] Page {page} returned 0 products.")

            for product in page_products:
                product["timestamp"] = timestamp

            all_products.extend(page_products)
    finally:
        session.close()

    if not all_products:
        raise RuntimeError("No data extracted from website.")

    return all_products