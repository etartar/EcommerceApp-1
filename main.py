# E-Ticaret API Projesi
from fastapi import FastAPI
from pydantic import BaseModel
from schemas import CreateCategoryRequest
from fastapi import HTTPException
from fastapi import status
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

from schemas import CreateCategoryRequest, UpdateCategoryRequest, CategoryResponse

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
    return productList

# 2. GET /products/{id} (Sadece ID'sini verdiğin ürünü getir)
@app.get("/products/{id}")
def get_product(id: int):
    # 1. Aşama: Ürünü arıyoruz
    for product in productList:
        if product["id"] == id:
            return {"success": True, "data": product, "message": "Urun bulundu."}
    
    # 2. Aşama: Döngü bitti ama ürün bulunamadıysa 
    logging.warning(f"Urun bulunamadi! ID: {id}")
    raise HTTPException(status_code=404, detail="Product not found")

# 3. POST /products (Yeni ürün ekle)
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    productList.append(product.model_dump()) 
    return {"success": True, "data": product.model_dump(), "message": "Urun basariyla eklendi."}

# 4. PUT /products/{id} (Mevcut ürünü güncelle)
@app.put("/products/{id}")
def update_product(id: int, updated_product: Product):
    for index, product in enumerate(productList):
        if product["id"] == id:
            productList[index] = updated_product.model_dump()
            return {"success": True, "data": productList[index], "message": "Urun guncellendi."}
    
    # Döngü bittiyse ürün yoktur, log atıp hata fırlatıyoruz:
    logging.warning(f"Urun bulunamadi! ID: {id}")
    raise HTTPException(status_code=404, detail="Product not found")

# 5. DELETE /products/{id} (Ürünü sil)
@app.delete("/products/{id}")
def delete_product(id: int):
    for index, product in enumerate(productList):
        if product["id"] == id:
            deleted = productList.pop(index)
            return {"success": True, "data": deleted, "message": "Urun silindi."}
    
    # Döngü bittiyse ürün yoktur, log atıp hata fırlatıyoruz:
    logging.warning(f"Urun bulunamadi! ID: {id}")
    raise HTTPException(status_code=404, detail="Product not found")


# 1. GET /categories (Tüm kategorileri listele)
@app.get("/categories", response_model=List[CategoryResponse])
def get_categories():
    return categoryList
# 2. GET /categories/{id} (ID'ye göre kategori getir)
@app.get("/categories/{id}")
def get_category(id: int):
    for category in categoryList:
        if category["id"] == id:
            return {"success": True, "data": category, "message": "Kategori bulundu."}

    # Kategori bulunamazsa 
    logging.warning(f"Kategori bulunamadi! ID: {id}")
    raise HTTPException(status_code=404, detail="Category not found")


# 3. POST /categories (Yeni kategori ekle)
@app.post("/categories",status_code=status.HTTP_201_CREATED)
def create_category(category_data: CreateCategoryRequest):
    for category in categoryList:
        if category["name"] == category_data.name:
            logging.warning(f"Ayni isimde kategori ekleme denemesi: {category_data.name}")
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False, 
                    "data": None, 
                    "message": f"'{category_data.name}' isminde bir kategori zaten mevcut.", 
                    "errors": []
                }
            )
            
    new_id = len(categoryList) + 1
    new_category = {
        "id": new_id,
        "name": category_data.name,
        "description": category_data.description
    }
    categoryList.append(new_category)
    
    #standart başarılı response şablonu
    return {
        "success": True, 
        "data": new_category, 
        "message": "Kategori basariyla olusturuldu."
    }

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
            
          
            return {
                "success": True, 
                "data": updated_category, 
                "message": "Kategori basariyla guncellendi"
            }
            
    # Eğer for döngüsü biter ve o ID'yi bulamazsa hata fırlatıyoruz
    logging.warning(f"Guncellenecek kategori bulunamadi! ID: {id}")
    raise HTTPException(
        status_code=404, 
        detail={"success": False, "data": None, "message": "Category not found", "errors": []}
    )
        
# 5. DELETE /categories/{id} (Kategori sil)
@app.delete("/categories/{id}")
def delete_category(id: int):
    for index, category in enumerate(categoryList):
        if category["id"] == id:
            deleted_category = categoryList.pop(index)
            
            # Silinen veriyi ve başarı mesajını dönüyoruz
            return {
                "success": True, 
                "data": deleted_category, 
                "message": "Kategori basariyla silindi"
            }
            
    # Eğer silinecek ID listede yoksa
    logging.warning(f"Silinecek kategori bulunamadi! ID: {id}")
    raise HTTPException(
        status_code=404, 
        detail={"success": False, "data": None, "message": "Category not found", "errors": []}
    )
