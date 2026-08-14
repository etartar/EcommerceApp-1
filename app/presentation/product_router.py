from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.data.database import SessionLocal
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.schemas.common_schema import SuccessResponse
from app.business import product_service

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=SuccessResponse)
def get_products(db: Session = Depends(get_db)):
    db_products = product_service.get_all_products(db)
    return SuccessResponse(success=True, data=db_products, message="Urunler listelendi.")

@router.get("/{id}", response_model=SuccessResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = product_service.get_product_by_id(db, id)
    return SuccessResponse(success=True, data=db_product, message="Urun bulundu.")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SuccessResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    db_product = product_service.create_product(db, product_data)
    return SuccessResponse(success=True, data=db_product, message="Urun basariyla eklendi.")

@router.put("/{id}", response_model=SuccessResponse)
def update_product(id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    db_product = product_service.update_product(db, id, product_data)
    return SuccessResponse(success=True, data=db_product, message="Urun guncellendi.")

@router.delete("/{id}", response_model=SuccessResponse)
def delete_product(id: int, db: Session = Depends(get_db)):
    product_service.delete_product(db, id)
    return SuccessResponse(success=True, data={"id": id}, message="Urun silindi.")