from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import products, temp_cart

app = FastAPI(title="SP Korea API", description="API для товаров и временных корзин")

# Настройка CORS — ДОЛЖНА БЫТЬ ПЕРВОЙ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все домены (временно)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Корневой маршрут
@app.get("/")
async def read_root():
    return {
        "message": "SP Korea API работает! 🚀",
        "endpoints": [
            "/api/products",
            "/api/temp-cart/{cart_id}",
            "/api/session/{session_id}"
        ]
    }

# Подключаем роуты
app.include_router(products.router)
app.include_router(temp_cart.router)
