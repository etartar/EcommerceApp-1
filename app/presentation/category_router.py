from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.data.database import SessionLocal 
from app.schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest
from app.schemas.common_schema import SuccessResponse
from app.business import category_service


router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=SuccessResponse)
def get_categories(db: Session = Depends(get_db)):
    db_categories = category_service.get_all_categories(db)
    return SuccessResponse(success=True, data=db_categories, message="Kategoriler basariyla listelendi.")

@router.get("/{id}", response_model=SuccessResponse)
def get_category(id: int, db: Session = Depends(get_db)):
    db_category = category_service.get_category_by_id(db, id)
    return SuccessResponse(success=True, data=db_category, message="Kategori bulundu.")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
def create_category(category_data: CreateCategoryRequest, db: Session = Depends(get_db)):
    db_category = category_service.create_category(db, category_data)
    return SuccessResponse(success=True, data=db_category, message="Kategori basariyla olusturuldu.")

@router.put("/{id}", response_model=SuccessResponse)
def update_category(id: int, category_data: UpdateCategoryRequest, db: Session = Depends(get_db)):
    db_category = category_service.update_category(db, id, category_data)
    return SuccessResponse(success=True, data=db_category, message="Kategori basariyla guncellendi")

@router.delete("/{id}", response_model=SuccessResponse)
def delete_category(id: int, db: Session = Depends(get_db)):
    category_service.delete_category(db, id)
    return SuccessResponse(success=True, data={"id": id}, message="Kategori basariyla silindi")