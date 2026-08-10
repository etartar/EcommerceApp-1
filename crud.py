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


# 1. READ (GET) - Tüm kategorileri getir
def get_categories(db: Session):
    return db.query(models.CategoryDB).all()

# READ (GET) - ID'ye göre tek kategori getir
def get_category_by_id(db: Session, category_id: int):
    return db.query(models.CategoryDB).filter(models.CategoryDB.id == category_id).first()

# 2. CREATE (POST) - Yeni kategori ekle
def create_category(db: Session, name: str):
    # Veritabanına kaydedilecek SQLAlchemy nesnesini oluşturuyorum
    db_category = models.CategoryDB(name=name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category) # Veritabanında otomatik oluşan ID'yi geri almak için
    return db_category

# 3. UPDATE (PUT) - Kategori güncelle
def update_category(db: Session, category_id: int, new_name: str):
    db_category = get_category_by_id(db, category_id)

    if db_category:
        db_category.name = new_name
        db.commit()
        db.refresh(db_category)
        return db_category
    return None # Kategori bulunamadıysa None dönüyorum ki main.py'da hata fırlatabileyim

# 4. DELETE (DELETE) - Kategori sil
def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True # Başarıyla silindiğini main.py'a bildirmek için True dönüyorum
    return False # Silinecek kategori bulunamadıysa False