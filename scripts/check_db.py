import sqlite3
import pandas as pd

def inspect_data():
    conn = sqlite3.connect('data/database.db')
    
    # Query 1: Total count of records
    total = pd.read_sql_query("SELECT COUNT(*) as total FROM books", conn)
    
    # Query 2: Look at the last 5 entries to ensure cleaning worked
    recent = pd.read_sql_query("SELECT * FROM books ORDER BY id DESC LIMIT 5", conn)
    
    print("--- DATABASE HEALTH CHECK ---")
    print(f"Total records in DB: {total['total']}")
    print("\nMost recent 5 entries:")
    print(recent[['id', 'title', 'price_float', 'scraped_at']])
    
    conn.close()

if __name__ == "__main__":
    inspect_data()