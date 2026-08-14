from sqlalchemy.orm import Session
from app.models.category import CategoryDB

# 1. READ (GET) - Tüm kategorileri getir
def get_categories(db: Session):
    return db.query(CategoryDB).all()

# READ (GET) - ID'ye göre tek kategori getir
def get_category_by_id(db: Session, category_id: int):
    return db.query(CategoryDB).filter(CategoryDB.id == category_id).first()

# 2. CREATE (POST) - Yeni kategori ekle
def create_category(db: Session, name: str):
    # Veritabanına kaydedilecek SQLAlchemy nesnesini oluşturuyorum
    db_category = CategoryDB(name=name)
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
    return None # Kategori bulunamadıysa None dönüyorum ki main.py'da hata fırlatabilelim

# 4. DELETE (DELETE) - Kategori sil
def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()