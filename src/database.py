import sqlite3
import os

DB_PATH = 'data/database.db'

def initialize_db():
    """Creates the database and the books table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create a table for our books
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            price_raw TEXT,
            price_float REAL,
            scraped_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def save_to_db(books_data):
    """Inserts a list of book dictionaries into the database, initializing if needed."""
    # Ensure the table exists before we try to insert data
    initialize_db() 
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for book in books_data:
        clean_price = float(book['price'].replace('Â£', '').replace('£', ''))
        
        # Use INSERT OR IGNORE to prevent the duplicates we saw earlier
        cursor.execute('''
            INSERT OR IGNORE INTO books (title, price_raw, price_float, scraped_at)
            VALUES (?, ?, ?, ?)
        ''', (book['title'], book['price'], clean_price, book['scraped_at']))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()