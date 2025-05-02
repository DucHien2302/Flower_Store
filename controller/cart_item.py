from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.models import CartItems, Products
from schemas.cart_item import CartItemCreate, CartItemUpdate

def add_item_to_cart(db: Session, cart_id: int, item_data: CartItemCreate) -> CartItems:
    product = db.query(Products).filter(Products.id == item_data.ProductID).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_item = db.query(CartItems).filter(
        CartItems.CartID == cart_id,
        CartItems.ProductID == item_data.ProductID
    ).first()

    if existing_item:
        existing_item.Quantity += item_data.Quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    db_item = CartItems(
        CartID=cart_id,
        ProductID=item_data.ProductID,
        Quantity=item_data.Quantity
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items_in_cart(db: Session, cart_id: int) -> List[CartItems]:
    return db.query(CartItems).filter(CartItems.CartID == cart_id).all()

def update_cart_item(db: Session, item_id: int, item_data: CartItemUpdate) -> CartItems:
    db_item = db.query(CartItems).filter(CartItems.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if item_data.Quantity is not None:
        db_item.Quantity = item_data.Quantity
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_cart_item(db: Session, item_id: int):
    db_item = db.query(CartItems).filter(CartItems.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(db_item)
    db.commit()