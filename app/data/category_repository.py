from sqlalchemy.orm import Session
from app.models.category import CategoryDB

class CategoryRepository:
    def __init__(self, db: Session):
        # Veritabanı bağlantısını sınıfın kendisine alıyoruz
        self.db = db

    # 1. READ (GET) - Tüm kategorileri getir
    def get_categories(self):
        return self.db.query(CategoryDB).all()

    # READ (GET) - ID'ye göre tek kategori getir
    def get_category_by_id(self, category_id: int):
        return self.db.query(CategoryDB).filter(CategoryDB.id == category_id).first()

    # 2. CREATE (POST) - Yeni kategori ekle
    def create_category(self, name: str):
        # Veritabanına kaydedilecek SQLAlchemy nesnesini oluşturuyorum
        db_category = CategoryDB(name=name)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category) # Veritabanında otomatik oluşan ID'yi geri almak için
        return db_category

    # 3. UPDATE (PUT) - Kategori güncelle
    def update_category(self, category_id: int, new_name: str):
        # Sınıf içindeki diğer fonksiyonu çağırırken self kullanıyorum
        db_category = self.get_category_by_id(category_id)
        
        if db_category:
            db_category.name = new_name
            self.db.commit()
            self.db.refresh(db_category)
            return db_category
        return None # Kategori bulunamadıysa None dönüyorum ki service'te hata fırlatabilelim

    # 4. DELETE (DELETE) - Kategori sil
    def delete_category(self, category_id: int):
        db_category = self.get_category_by_id(category_id)
        if db_category:
            self.db.delete(db_category)
            self.db.commit()
            return True # Başarıyla silindiğini bildirmek için True dönüyorum
        return False # Silinecek kategori bulunamadıysa False