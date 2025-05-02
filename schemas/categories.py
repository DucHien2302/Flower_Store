from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    Name: str
    Description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True