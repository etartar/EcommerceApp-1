from sqlalchemy import Column, Integer, String, Float
from database import Base

class ProductDB(Base):
    __tablename__ = "products" # SQL Server'da oluşacak tablonun adı

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)