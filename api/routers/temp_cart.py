from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, List
import json
import os
from datetime import datetime

# Модель данных для товара в корзине
class CartItem(BaseModel):
    id: int
    quantity: int

# Путь к папке с временными корзинами
TEMP_CART_DIR = "data/temp_cart"
if not os.path.exists(TEMP_CART_DIR):
    os.makedirs(TEMP_CART_DIR)

# Временное хранилище корзин (в продакшене использовать Redis)
TEMP_CARTS: Dict[str, dict] = {}

# Загрузка корзин из файлов при старте
def load_temp_carts():
    for filename in os.listdir(TEMP_CART_DIR):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(TEMP_CART_DIR, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cart_id = filename.replace(".json", "")
                    TEMP_CARTS[cart_id] = data
            except Exception as e:
                print(f"⚠️ Ошибка загрузки корзины {filename}: {e}")

load_temp_carts()

router = APIRouter(prefix="/api", tags=["temp_cart"])

@router.post("/temp-cart/{cart_id}")
async def save_temp_cart(cart_id: str, items: List[CartItem] = Body(...)):
    """
    Сохраняет временную корзину по уникальному ID.
    Вызывается из Web App при оформлении заказа.
    """
    cart_data = {
        "cart_id": cart_id,
        "items": [item.dict() for item in items],
        "created_at": datetime.utcnow().isoformat()
    }
    TEMP_CARTS[cart_id] = cart_data
    
    # Сохраняем в файл
    try:
        with open(os.path.join(TEMP_CART_DIR, f"{cart_id}.json"), "w", encoding="utf-8") as f:
            json.dump(cart_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения: {e}")

    return {"status": "saved", "cart_id": cart_id}

@router.get("/temp-cart/{cart_id}")
async def get_temp_cart(cart_id: str):
    """
    Возвращает временную корзину по ID.
    Вызывается ботом при /start order_<cart_id>.
    """
    cart = TEMP_CARTS.get(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Корзина не найдена")
    return cart