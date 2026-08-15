from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.data.database import SessionLocal 
from app.schemas.category_schema import CreateCategoryRequest, UpdateCategoryRequest
from app.schemas.common_schema import SuccessResponse
#  CategoryService sınıfını içe aktarıyoruz
from app.business.category_service import CategoryService


router = APIRouter(prefix="/categories", tags=["Categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=SuccessResponse)
def get_categories(db: Session = Depends(get_db)):
    #  nesnemizi veritabanı bağlantısıyla oluşturuyoruz
    service = CategoryService(db)
    # sınıfın metodunu çağırıyoruz
    db_categories = service.get_all_categories()
    return SuccessResponse(success=True, data=db_categories, message="Kategoriler basariyla listelendi.")

@router.get("/{id}", response_model=SuccessResponse)
def get_category(id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    db_category = service.get_category_by_id(id)
    return SuccessResponse(success=True, data=db_category, message="Kategori bulundu.")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
def create_category(category_data: CreateCategoryRequest, db: Session = Depends(get_db)):
    service = CategoryService(db)
    db_category = service.create_category(category_data)
    return SuccessResponse(success=True, data=db_category, message="Kategori basariyla olusturuldu.")

@router.put("/{id}", response_model=SuccessResponse)
def update_category(id: int, category_data: UpdateCategoryRequest, db: Session = Depends(get_db)):
    service = CategoryService(db)
    db_category = service.update_category(id, category_data)
    return SuccessResponse(success=True, data=db_category, message="Kategori basariyla guncellendi")

@router.delete("/{id}", response_model=SuccessResponse)
def delete_category(id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    service.delete_category(id)
    return SuccessResponse(success=True, data={"id": id}, message="Kategori basariyla silindi")