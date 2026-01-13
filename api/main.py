from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import products, temp_cart  # ✅ Импортируем оба роутера

app = FastAPI(title="SP Korea API", description="API для товаров и временных корзин")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажи домены: ['https://sp-korea-web-app.vercel.app']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Корневой маршрут — важен для Render
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

# Подключаем маршруты
app.include_router(products.router)      # /api/products
app.include_router(temp_cart.router)    # /api/temp-cart/{id}
