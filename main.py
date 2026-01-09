from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional  # ← добавлено Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

# === База данных — теперь в корне проекта ===
DATABASE_URL = "sqlite:///products.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# === Модель товара ===
class ProductDB(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    article = Column(String)
    brand = Column(String)
    name = Column(String)
    name_en = Column(String)
    volume = Column(String)
    price_krw = Column(Integer)
    price_rub = Column(Integer)
    description = Column(String)
    image_url = Column(String)  # Может быть NULL
    refill = Column(Boolean, default=False)
    quantity = Column(Integer, default=10)
    created_at = Column(DateTime)

# === Pydantic-схема — image_url теперь опционален ===
class Product(BaseModel):
    id: int
    article: str
    brand: str
    name: str
    name_en: str
    volume: str
    price_krw: int
    price_rub: int
    description: str
    image_url: Optional[str] = None  # ← Можно None
    quantity: int

    class Config:
        from_attributes = True

app = FastAPI(title="SP Korea API", docs_url="/", redoc_url=None)

# === Разрешаем CORS с любого источника (для разработки) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Создаём таблицы при старте ===
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/products", response_model=List[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(ProductDB).offset(skip).limit(limit).all()
    return products

@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.get("/")
def read_root():
    return {"message": "SP Korea API работает! 🚀", "docs": "/"}
