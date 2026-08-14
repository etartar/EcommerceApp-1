from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging
from app.data import product_repository
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.schemas.common_schema import ErrorResponse

def get_all_products(db: Session):
    return product_repository.get_products(db)

def get_product_by_id(db: Session, product_id: int):
    product = product_repository.get_product_by_id(db, product_id)
    if not product:
        logging.warning(f"Ürün bulunamadı! ID: {product_id}")
        raise HTTPException(
            status_code=404, 
            detail=ErrorResponse(success=False, message="Product not found", errors=[f"ID {product_id} bulunamadı"]).model_dump()
        )
    return product

def create_product(db: Session, product_data: ProductCreate):
    return product_repository.create_product(
        db=db, 
        name=product_data.name, 
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id
    )

def update_product(db: Session, product_id: int, product_data: ProductUpdate):
    get_product_by_id(db, product_id) 
    
    return product_repository.update_product(
        db=db, 
        product_id=product_id, 
        new_name=product_data.name, 
        new_price=product_data.price,
        new_stock=product_data.stock,
        new_category_id=product_data.category_id
    )

def delete_product(db: Session, product_id: int):
    get_product_by_id(db, product_id) 
    return product_repository.delete_product(db, product_id)