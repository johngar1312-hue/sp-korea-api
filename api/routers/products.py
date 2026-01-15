from fastapi import APIRouter
import sqlite3
import os

# 🔁 Убираем prefix="/api" из роутера — он будет в main.py
router = APIRouter(tags=["products"])

# 🔥 ФИКС: путь к БД — только через /var/lib/sp-korea/data/products.db
DB_PATH = "/var/lib/sp-korea/data/products.db"

print("📁 Путь к БД:", DB_PATH)

def get_db():
    # Создаём папку, если её нет
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/api/products")
def get_products():
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='products';
        """)
        table_exists = cursor.fetchone()
        if not table_exists:
            return {"error": "Таблица 'products' не существует"}

        cursor.execute("""
            SELECT id, article, brand, name, name_en, volume, price_rub, image_url
            FROM products
        """)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
    except Exception as e:
        return {"error": f"Ошибка при чтении базы: {str(e)}"}
