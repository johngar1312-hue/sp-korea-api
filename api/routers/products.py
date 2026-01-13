# api/routers/products.py

from fastapi import APIRouter
import sqlite3
import os

router = APIRouter(prefix="/api", tags=["products"])

# Определяем BASE_DIR как папку api/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Путь к базе: /home/j/johngaqf/johngaqf.beget.tech/api/data/products.db
DB_PATH = os.path.join(BASE_DIR, "data", "products.db")

# Для отладки — посмотри, куда сохраняется БД
print("📁 Путь к БД:", DB_PATH)

def get_db():
    # Создаём папку data, если её нет
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    # Подключаемся к SQLite
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # чтобы можно было обращаться по имени колонки
    return conn

@router.get("/products")
def get_products():
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Проверяем, существует ли таблица
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='products';
        """)
        table_exists = cursor.fetchone()

        if not table_exists:
            return {"error": "Таблица 'products' не существует. Создайте её через SQL."}

        cursor.execute("""
            SELECT id, article, brand, name, name_en, volume, price_rub, image_url
            FROM products
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        return {"error": f"Ошибка при чтении базы: {str(e)}"}