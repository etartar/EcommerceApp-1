from sqlalchemy.orm import Session
import models  # yazdığımız models.py dosyasını çağırıyorum

# 1. READ (GET) - Tüm ürünleri getir
def get_products(db: Session):
    return db.query(models.ProductDB).all() 

# READ (GET) - ID'ye göre tek ürün getir
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.ProductDB).filter(models.ProductDB.id == product_id).first()

# 2. CREATE (POST) - Yeni ürün ekle
def create_product(db: Session, name: str, price: float):
    # Veritabanına kaydedilecek SQLAlchemy nesnesini oluşturuyorum
    db_product = models.ProductDB(name=name, price=price) 
    db.add(db_product)
    db.commit()
    db.refresh(db_product) # Veritabanında otomatik oluşan ID'yi geri almak için
    return db_product

# 3. UPDATE (PUT) - Ürün güncelle
def update_product(db: Session, product_id: int, new_name: str, new_price: float):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db_product.name = new_name
        db_product.price = new_price
        db.commit()
        db.refresh(db_product)
        return db_product
    return None # Ürün bulunamadıysa None dönüyoruz ki main.py'da hata fırlatabilelim

# 4. DELETE (DELETE) - Ürün sil
def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True # Başarıyla silindiğini main.py'a bildirmek için True dönüyoruz
    return False # Silinecek ürün bulunamadıysa False