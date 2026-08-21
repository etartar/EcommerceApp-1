from fastapi import FastAPI
import logging
from app.presentation import product_router, category_router
from app.presentation import auth_router
from app.data.database import engine
from app.data.database import Base
from app.models.user import User # Tablomuzu main.py'nin görmesini sağlıyoruz

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="E-Ticaret API Projesi")
Base.metadata.create_all(bind=engine)

# Yazdığımız router'ları ana uygulamaya bağlıyoruz
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(auth_router.router)