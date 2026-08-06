import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# .env dosyasındaki ayarları sisteme yükler
load_dotenv() 

# Adresi .env dosyasından çekiyoruz
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

# Veritabanı motorunu (engine) oluşturuyoruz
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


# Veritabanında işlem yapmamızı sağlayacak oturum (session) yapısı
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tüm veritabanı tablolarımızın miras alacağı temel sınıf
Base = declarative_base()

# API istekleri boyunca veritabanı bağlantısını açıp kapatacak yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()