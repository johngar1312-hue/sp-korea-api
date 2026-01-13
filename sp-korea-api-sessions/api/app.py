# api/app.py
from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Путь к базе
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "products.db")

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return jsonify({"status": "API работает", "domain": "johngaqf.beget.tech"})

@app.route("/api/products")
def products():
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='products';
        """)
        table_exists = cursor.fetchone()
        if not table_exists:
            return jsonify({"error": "Таблица 'products' не существует"}), 404

        cursor.execute("""
            SELECT id, article, brand, name, name_en, volume, price_rub, image_url
            FROM products
        """)
        rows = cursor.fetchall()
        conn.close()

        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Для CGI
if __name__ == "__main__":
    app.run()