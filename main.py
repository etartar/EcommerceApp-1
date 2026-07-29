# E-Ticaret API Projesi
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    price: float


productList = []

# 1. GET /products (Tüm ürünleri listele)
@app.get("/products")
def get_products():
    return productList

# 2. GET /products/{id} (Sadece ID'sini verdiğin ürünü getir)
@app.get("/products/{id}")
def get_product(id: int):
    for product in productList:
        if product["id"] == id:
            return product
    return {"hata": "Ürün bulunamadı"}

# 3. POST /products (Yeni ürün ekle)
@app.post("/products")
def create_product(product: Product):
    productList.append(product.model_dump()) 
    return {"mesaj": "Ürün başarıyla eklendi", "ürün": product}

# 4. PUT /products/{id} (Mevcut ürünü güncelle)
@app.put("/products/{id}")
def update_product(id: int, updated_product: Product):
    for index, product in enumerate(productList):
        if product["id"] == id:
            productList[index] = updated_product.model_dump()
            return {"mesaj": "Ürün güncellendi"}
    return {"hata": "Ürün bulunamadı"}

# 5. DELETE /products/{id} (Ürünü sil)
@app.delete("/products/{id}")
def delete_product(id: int):
    for index, product in enumerate(productList):
        if product["id"] == id:
            productList.pop(index)
            return {"mesaj": "Ürün silindi"}
    return {"hata": "Ürün bulunamadı"}

