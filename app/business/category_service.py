from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging
from app.data import category_repository
from app.schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest
from app.schemas.common_schema import ErrorResponse 

def get_all_categories(db: Session):
    return category_repository.get_categories(db)

def get_category_by_id(db: Session, category_id: int):
    category = category_repository.get_category_by_id(db, category_id)
    if not category:
        logging.warning(f"Kategori bulunamadı! ID: {category_id}")
        raise HTTPException(
            status_code=404, 
            detail=ErrorResponse(success=False, message="Category not found", errors=[f"ID {category_id} bulunamadı"]).model_dump()
        )
    return category

def create_category(db: Session, category_data: CreateCategoryRequest):
    
    return category_repository.create_category(db, category_data.name)

def update_category(db: Session, category_id: int, category_data: UpdateCategoryRequest):
   
    get_category_by_id(db, category_id) 
    
    return category_repository.update_category(db, category_id, category_data.name)

def delete_category(db: Session, category_id: int):
    
    get_category_by_id(db, category_id)
    return category_repository.delete_category(db, category_id)