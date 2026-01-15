import uvicorn

if __name__ == "__main__":
    # 🔥 Убираем reload=True — он не нужен в продакшене
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000)
