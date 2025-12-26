import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def scrape_competitors():
    data = []

    urls = [
        ("Competitor A", "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"),
        ("Competitor B", "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html")
    ]

    for name, url in urls:
        print(f"🔎 Scraping {name}...")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Failed to fetch {name}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        product = soup.select_one("article.product_pod")

        if not product:
            print(f"⚠ No product found for {name}")
            continue

        # Service / product name
        service = product.h3.a.get("title", "Unknown")

        # Price cleaning (FIXES Â45.17 issue)
        price_text = product.select_one("p.price_color").text.strip()
        clean_price = re.sub(r"[^\d.]", "", price_text)

        try:
            price = float(clean_price)
        except ValueError:
            print(f"⚠ Invalid price for {name}: {price_text}")
            price = None

        data.append({
            "name": name,
            "service": service,
            "price": price,
            "engagement": 1500
        })

    if not data:
        print("❌ No data scraped. CSV not created.")
        return

    df = pd.DataFrame(data)
    df.to_csv("data/raw_data.csv", index=False, encoding="utf-8")

    print("✅ raw_data.csv created successfully")
    print(df)


if __name__ == "__main__":
    scrape_competitors()
