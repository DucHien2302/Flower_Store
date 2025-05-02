from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CartItemBase(BaseModel):
    ProductID: int
    Quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    Quantity: Optional[int] = None

class CartItemRequest(BaseModel):
    ProductID: int
    Quantity: int
    UserID: int

class CartItemUpdateRequest(BaseModel):
    Quantity: int
    UserID: int

class CartItem(CartItemBase):
    id: int
    CartID: int
    CreatedAt: Optional[datetime] = None  # Change to datetime
    UpdatedAt: Optional[datetime] = None  # Change to datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Chuyển datetime thành chuỗi ISO
        }