from sqlalchemy import Column, Integer, String
from app.data.database import Base

class CategoryDB(Base):
    __tablename__ = "categories" # SQL Server'da oluşacak tablonun adı

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), index=True, nullable=False)