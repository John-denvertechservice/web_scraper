import requests
from bs4 import BeautifulSoup
import json
import os
import time      # New: for delays
import random    # New: for randomizing the wait
from datetime import datetime
from database import save_to_db

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
    # We'll scrape the first 3 pages to start
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_scraped_data = []

    print("--- Starting Multi-Page Scrape ---")

    for page_num in range(1, 4):
        url = base_url.format(page_num)
        print(f"Scraping Page {page_num}...")
        
        html = fetch_page(url)
        if html:
            page_data = parse_book(html)
            all_scraped_data.extend(page_data)
            
            # --- BAN EVASION: Politeness Delay ---
            # Wait between 1 and 3 seconds before the next page
            wait_time = random.uniform(1, 3)
            print(f"Waiting {wait_time:.2f} seconds to be polite...")
            time.sleep(wait_time)

    if all_scraped_data:
        # Save to JSON
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        output_file = f"data/raw/multi_scrape_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(all_scraped_data, f, indent=4)
            
        # Save to Database
        save_to_db(all_scraped_data)
        
        print(f"\nSUCCESS: Scraped a total of {len(all_scraped_data)} books.")
        print(f"Data saved to {output_file} and database.db")
    
if __name__ == "__main__":
    main()
