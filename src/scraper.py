import requests
from bs4  import BeautifulSoup
import json
import os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
def parse_book(html):
    soup = BeautifulSoup(html, 'html.parser')
    books_data = []
    articles = soup.find_all('article', class_='product_pod')

    for article in articles:
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text

        books_data.append({
            "title": title,
            "price": price,
            "scraped_at": datetime.now().isoformat()
        })
    return books_data

def main():
    target_url = "http://books.toscrape.com/catalogue/page-1.html"
    print(f"Starting scrape of {target_url}...")

    html = fetch_page(target_url)

    if html:
        data = parse_book(html)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        output_file = f"data/raw/scrape_{timestamp}.json"

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Successfully scraped {len(data)} items. Data saved to {output_file}")
    
if __name__ == "__main__":
    main()
