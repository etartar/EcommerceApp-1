# E-Ticaret API Projesi
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List
import logging
from sqlalchemy.orm import Session

# Kendi yazdığım dosyalar
import crud
from schemas import CreateCategoryRequest, UpdateCategoryRequest, CategoryResponse, SuccessResponse, ErrorResponse
from database import SessionLocal 

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Veritabanı Session bağımlılığı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Product(BaseModel):
    id: int
    name: str
    price: float

class ProductCreate(BaseModel):
    name: str
    price: float

# productList'i sildim çünkü veritabanına bağladım
categoryList = []

# 1. GET /products (Tüm ürünleri getir)
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = crud.get_products(db)
    return SuccessResponse(success=True, data=db_products, message="Urunler listelendi.")


# 2. GET /products/{id} (Sadece ID'sini verdiğin ürünü getir)
@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, id)
    if db_product:
        return SuccessResponse(success=True, data=db_product, message="Urun bulundu.")
    
    logging.warning(f"Urun bulunamadi! ID: {id}")
    raise HTTPException(
        status_code=404, 
        detail=ErrorResponse(success=False, message="Product not found", errors=[f"ID {id} bulunamadi"]).model_dump()
    )


# 3. POST /products (Yeni ürün ekle)
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.create_product(db=db, name=product.name, price=product.price)
    return SuccessResponse(success=True, data=db_product, message="Urun basariyla eklendi.")


# 4. PUT /products/{id} (Mevcut ürünü güncelle)
@app.put("/products/{id}")
def update_product(id: int, updated_product: ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db=db, product_id=id, new_name=updated_product.name, new_price=updated_product.price)
    if db_product:
        return SuccessResponse(success=True, data=db_product, message="Urun guncellendi.")
        
    logging.warning(f"Urun bulunamadi! ID: {id}")
    raise HTTPException(
        status_code=404, 
        detail=ErrorResponse(success=False, message="Product not found").model_dump()
    )


# 5. DELETE /products/{id} (Ürünü sil)
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db=db, product_id=id)
    if success:
        return SuccessResponse(success=True, data={"id": id}, message="Urun silindi.")
        
    logging.warning(f"Urun bulunamadi! ID: {id}")
    raise HTTPException(
        status_code=404, 
        detail=ErrorResponse(success=False, message="Product not found").model_dump()
    )


# 1. GET /categories (Tüm kategorileri listele)
@app.get("/categories")
def get_categories():
    
    return SuccessResponse(success=True, data=categoryList, message="Kategoriler basariyla listelendi.")


# 2. GET /categories/{id} (ID'ye göre kategori getir)
@app.get("/categories/{id}")
def get_category(id: int):
    for category in categoryList:
        if category["id"] == id:
            # Başarılı durum entegrasyonu
            return SuccessResponse(success=True, data=category, message="Kategori bulundu.")

    logging.warning(f"Kategori bulunamadi! ID: {id}")
    raise HTTPException(
        status_code=404, 
        detail=ErrorResponse(success=False, message="Category not found").model_dump()
    )

# 3. POST /categories (Yeni kategori ekle)
@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(category_data: CreateCategoryRequest):
    for category in categoryList:
        if category["name"] == category_data.name:
            logging.warning(f"Ayni isimde kategori ekleme denemesi: {category_data.name}")
          
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    success=False, 
                    message=f"'{category_data.name}' isminde bir kategori zaten mevcut."
                ).model_dump()
            )
            
    new_id = len(categoryList) + 1
    new_category = {
        "id": new_id,
        "name": category_data.name,
        "description": category_data.description
    }
    categoryList.append(new_category)
    
    # Başarılı durum entegrasyonu
    return SuccessResponse(success=True, data=new_category, message="Kategori basariyla olusturuldu.")


# 4. PUT /categories/{id} (Kategori güncelle)
@app.put("/categories/{id}")
def update_category(id: int, category_data: UpdateCategoryRequest):
    for index, category in enumerate(categoryList):
        if category["id"] == id:
            updated_category = {
                "id": id,
                "name": category_data.name,
                "description": category_data.description
            }
            categoryList[index] = updated_category
            
            # Başarılı durum entegrasyonu
            return SuccessResponse(success=True, data=updated_category, message="Kategori basariyla guncellendi")
            
    logging.warning(f"Guncellenecek kategori bulunamadi! ID: {id}")
   
    raise HTTPException(
        status_code=404, 
        detail=ErrorResponse(success=False, message="Category not found").model_dump()
    )


# 5. DELETE /categories/{id} (Kategori sil)
@app.delete("/categories/{id}")
def delete_category(id: int):
    for index, category in enumerate(categoryList):
        if category["id"] == id:
            deleted_category = categoryList.pop(index)
            
            # Başarılı durum entegrasyonu
            return SuccessResponse(success=True, data=deleted_category, message="Kategori basariyla silindi")
            
    logging.warning(f"Silinecek kategori bulunamadi! ID: {id}")
    # hata entegrasyonu
    raise HTTPException(
        status_code=404, 
        detail=ErrorResponse(success=False, message="Category not found").model_dump()
    )