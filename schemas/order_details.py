from pydantic import BaseModel
from typing import Optional

class OrderDetailBase(BaseModel):
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: int
    unit_price: int

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = None
    unit_price: Optional[int] = None

class OrderDetail(OrderDetailBase):
    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True