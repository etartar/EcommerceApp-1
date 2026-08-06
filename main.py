# E-Ticaret API Projesi
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

from schemas import CreateCategoryRequest, UpdateCategoryRequest, CategoryResponse, SuccessResponse, ErrorResponse

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float


productList = []
categoryList = []

# 1. GET /products (Tüm ürünleri listele)
@app.get("/products")
def get_products():
    return SuccessResponse(success=True, data=productList, message="Urunler listelendi.")

# 2. GET /products/{id} (Sadece ID'sini verdiğin ürünü getir)
@app.get("/products/{id}")
def get_product(id: int):
    for product in productList:
        if product["id"] == id:
            return SuccessResponse(success=True, data=product, message="Urun bulundu.")
    
    logging.warning(f"Urun bulunamadi! ID: {id}")
    raise HTTPException(
        status_code=404, 
        detail=ErrorResponse(message="Product not found", errors=[f"ID {id} bulunamadi"]).model_dump()
    )

# 3. POST /products (Yeni ürün ekle)
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    productList.append(product.model_dump()) 
    return SuccessResponse(success=True, data=product.model_dump(), message="Urun basariyla eklendi.")

# 4. PUT /products/{id} (Mevcut ürünü güncelle)
@app.put("/products/{id}")
def update_product(id: int, updated_product: Product):
    for index, product in enumerate(productList):
        if product["id"] == id:
            productList[index] = updated_product.model_dump()
            
            return SuccessResponse(success=True, data=productList[index], message="Urun guncellendi.")
    
    logging.warning(f"Urun bulunamadi! ID: {id}")
    
    raise HTTPException(
        status_code=404, 
        detail=ErrorResponse(success=False, message="Product not found").model_dump()
    )

# 5. DELETE /products/{id} (Ürünü sil)
@app.delete("/products/{id}")
def delete_product(id: int):
    for index, product in enumerate(productList):
        if product["id"] == id:
            deleted = productList.pop(index)
            
            return SuccessResponse(success=True, data=deleted, message="Urun silindi.")
    
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