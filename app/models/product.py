from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.data.database import Base

class ProductDB(Base):
    __tablename__ = "products" # SQL Server'da oluşacak tablonun adı

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), index=True, nullable=False)
    price = Column(Float, nullable=False)

    description = Column(String(250), nullable=True)
  