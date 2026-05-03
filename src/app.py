import sqlite3
import os
from flask import Flask, render_template

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')


def get_books():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        "SELECT title, price_float, scraped_at FROM books ORDER BY price_float DESC"
    )
    books = cursor.fetchall()
    conn.close()
    return books


@app.route('/')
def index():
    books = get_books()
    return render_template('index.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
