from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging
# CategoryRepository sınıfını import ediyoruz
from app.data.category_repository import CategoryRepository
from app.schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest
from app.schemas.common_schema import ErrorResponse 

class CategoryService:
    def __init__(self, db: Session):
        # Veritabanı bağlantısını alıp Repository sınıfını başlatıyorum
        self.repository = CategoryRepository(db)

    def get_all_categories(self):
        # Artık db'yi yollamamıza gerek yok, repository kendi içinde hallediyor
        return self.repository.get_categories()

    def get_category_by_id(self, category_id: int):
        category = self.repository.get_category_by_id(category_id)
        if not category:
            logging.warning(f"Kategori bulunamadı! ID: {category_id}")
            raise HTTPException(
                status_code=404, 
                detail=ErrorResponse(success=False, message="Category not found", errors=[f"ID {category_id} bulunamadı"]).model_dump()
            )
        return category

    def create_category(self, category_data: CreateCategoryRequest):
        return self.repository.create_category(name=category_data.name)

    def update_category(self, category_id: int, category_data: UpdateCategoryRequest):
        # Önce kategori var mı diye sınıfın kendi fonksiyonuyla kontrol ediyorum
        self.get_category_by_id(category_id) 
        
        return self.repository.update_category(
            category_id=category_id, 
            new_name=category_data.name
        )

    def delete_category(self, category_id: int):
        # Kategori var mı diye kontrol ediyorum
        self.get_category_by_id(category_id)
        return self.repository.delete_category(category_id)