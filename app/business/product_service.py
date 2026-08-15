from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging

from app.data.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.schemas.common_schema import ErrorResponse

class ProductService:
    def __init__(self, db: Session):
        # Veritabanı bağlantısını alıp Repository sınıfını başlatıyorum.
        self.repository = ProductRepository(db)

    def get_all_products(self):
        # Artık db'yi yollamama gerek yok, repository kendi içinde hallediyor
        return self.repository.get_products()

    def get_product_by_id(self, product_id: int):
        product = self.repository.get_product_by_id(product_id)
        if not product:
            logging.warning(f"Ürün bulunamadı! ID: {product_id}")
            raise HTTPException(
                status_code=404, 
                detail=ErrorResponse(success=False, message="Product not found", errors=[f"ID {product_id} bulunamadı"]).model_dump()
            )
        return product

    def create_product(self, product_data: ProductCreate):
        return self.repository.create_product(
            name=product_data.name, 
            price=product_data.price,
            stock=product_data.stock,
            category_id=product_data.category_id
        )

    def update_product(self, product_id: int, product_data: ProductUpdate):
        # Önce ürün var mı diye kontrol ediyorum
        self.get_product_by_id(product_id) 
        
        return self.repository.update_product(
            product_id=product_id, 
            new_name=product_data.name, 
            new_price=product_data.price,
            new_stock=product_data.stock,
            new_category_id=product_data.category_id
        )

    def delete_product(self, product_id: int):
        # sınıfın kendi kontrol fonksiyonunu çağırıyorum
        self.get_product_by_id(product_id) 
        return self.repository.delete_product(product_id)