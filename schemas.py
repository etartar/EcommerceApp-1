from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CreateCategoryRequest(BaseModel):
    """Kategori oluştururken gelen istek (Request) modeli"""
    name: str = Field(..., description="Kategori adı")

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError('Kategori ismi boş bırakılamaz.')
        return value


class UpdateCategoryRequest(BaseModel):
    """Kategori güncellerken gelen istek (Request) modeli"""
    name: str = Field(..., description="Kategori adı")
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError('Kategori ismi boş bırakılamaz.')
        return value


class CategoryResponse(BaseModel):
    """Kullanıcıya dönen kategori (Response) modeli"""
    id: int
    name: str

    model_config = {
        "from_attributes": True  # Database model ayrımı ve serileştirme için
    }


class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category_id: int


class ProductCreate(ProductBase):
    """Ürün oluştururken gelen istek (Request) modeli"""

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError('Ürün ismi boş olamaz.')
        return value

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('Fiyat sıfırdan büyük olmalıdır.')
        return value

    @field_validator('stock')
    @classmethod
    def stock_must_not_be_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError('Stok negatif olamaz.')
        return value

class ProductResponse(ProductBase):
    """Kullanıcıya dönen ürün (Response) modeli"""
    id: int
    
    model_config = {
        "from_attributes": True  # Database model ayrımı ve serileştirme için
    }

class ProductUpdate(BaseModel):
    """Ürün güncellerken kullanılan (Optional) model"""
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and (not value or not value.strip()):
            raise ValueError('Ürün ismi boş bırakılamaz.')
        return value

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and value <= 0:
            raise ValueError('Fiyat sıfırdan büyük olmalıdır.')
        return value

    @field_validator('stock')
    @classmethod
    def stock_must_not_be_negative(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value < 0:
            raise ValueError('Stok negatif olamaz.')
        return value




class SuccessResponse(BaseModel):
    success: bool = True
    data: dict
    message: str = None

class ErrorResponse(BaseModel):
    success: bool = False
    data: dict = None
    message: str
    errors: list = []