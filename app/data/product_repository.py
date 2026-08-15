from sqlalchemy.orm import Session
from app.models.product import ProductDB

class ProductRepository:
    def __init__(self, db: Session):
        # Veritabanı bağlantısını sınıfın içine  alıyorum
        self.db = db

    # 1. READ (GET) - Tüm ürünleri getir
    def get_products(self):
        return self.db.query(ProductDB).all() 

    # READ (GET) - ID'ye göre tek ürün getir
    def get_product_by_id(self, product_id: int):
        return self.db.query(ProductDB).filter(ProductDB.id == product_id).first()

    # 2. CREATE (POST) - Yeni ürün ekle
    def create_product(self, name: str, price: float):
        # Veritabanına kaydedilecek SQLAlchemy nesnesini oluşturuyorum
        db_product = ProductDB(name=name, price=price) 
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product) # Veritabanında otomatik oluşan ID'yi geri almak için
        return db_product

    # 3. UPDATE (PUT) - Ürün güncelle
    def update_product(self, product_id: int, new_name: str, new_price: float):
        # Artık sınıfın kendi içindeki fonksiyonu self ile çağırıyorum
        db_product = self.get_product_by_id(product_id)

        if db_product:
            db_product.name = new_name
            db_product.price = new_price
            self.db.commit()
            self.db.refresh(db_product)
            return db_product
        return None # Ürün bulunamadıysa None dönüyoruz ki serviste hata fırlatabilelim

    # 4. DELETE (DELETE) - Ürün sil
    def delete_product(self, product_id: int):
        db_product = self.get_product_by_id(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return True # Başarıyla silindiğini servise bildirmek için True dönüyoruz
        return False # Silinecek ürün bulunamadıysa False