import pandas as pd
import glob
import os

def get_latest_scrape():
    list_of_files = glob.glob('data/raw/*.json')
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)

def generate_summary():
    latest_file = get_latest_scrape()
    if not latest_file:
        print("No data files found to report on.")
        return
    print(f"Generating report from {latest_file}")
    df = pd.read_json(latest_file)
    df['price_clean'] = df['price'].str.replace('Â£', '').str.replace('£', '').astype(float)

    total_books = len(df)
    avg_price = df['price_clean'].mean()
    most_expensive = df.loc[df['price'].idxmax()]
    print("-" * 30)
    print(f"DAILY BOOK REPORT")
    print("-" * 30)
    print(f"Total Books Scraped: {total_books}")
    print(f"Average Price: £{avg_price:.2f}")
    print(f"Most Expensive: {most_expensive['title']} (£{most_expensive['price_clean']})")
    print("-" * 30)
if __name__ ==  "__main__":
    generate_summary()
