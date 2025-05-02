from pydantic import BaseModel
from typing import Optional, List
from schemas.products import Product

class CartBase(BaseModel):
    user_id: int
    status: str = "Pending"  

class CartCreate(CartBase):
    pass

class CartUpdate(BaseModel):
    user_id: Optional[int] = None

class Cart(CartBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    class Config:
        from_attributes = True