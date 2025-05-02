from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from schemas.products import Product

class OrderBase(BaseModel):
    user_id: Optional[int] = None
    order_date: Optional[date] = None
    total_amount: Optional[int] = None
    status: str = "Pending"
    shipping_address: Optional[str] = None
    delivery_date: Optional[date] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    status: Optional[str] = None
    shipping_address: Optional[str] = None
    delivery_date: Optional[date] = None

class Order(OrderBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True