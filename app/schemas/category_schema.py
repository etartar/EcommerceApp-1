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
