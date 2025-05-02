from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.models import Cart

def get_cart_by_user_id(db: Session, user_id: int) -> Cart:
    return db.query(Cart).filter(Cart.UserID == user_id, Cart.Status == 'Pending').first()

def create_cart(db: Session, user_id: int) -> Cart:
    db_cart = Cart(UserID=user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart