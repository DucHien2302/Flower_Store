from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from pydantic import BaseModel

from config.db import get_db
from models.models import User as UserModel, Cart as CartModel, CartItems as CartItemModel, Products as ProductModel
from schemas.cart import Cart
from schemas.cart_item import CartItem, CartItemCreate, CartItemUpdate, CartItemRequest, CartItemUpdateRequest
from schemas.products import Product as ProductSchema
from schemas.orders import Order
from controller import cart as cart_controller
from controller import cart_item as cart_items_controller
from controller import products as product_controller
from controller import orders as order_controller

router = APIRouter(
    prefix="/cart",
    tags=["Shopping Cart"],
)

def get_or_create_user_cart(db: Session, user_id: int) -> CartModel:
    """
    Lấy hoặc tạo giỏ hàng chưa thanh toán cho người dùng.
    """
    db_cart = cart_controller.get_cart_by_user_id(db, user_id=user_id)
    if not db_cart:
        db_cart = cart_controller.create_cart(db, user_id=user_id)
    return db_cart

@router.post("/items", response_model=CartItem, status_code=status.HTTP_201_CREATED, summary="Add an item to the cart")
async def add_item(
    item_data: CartItemRequest,  # Nhận ProductID, Quantity, UserID trong body
    db: Session = Depends(get_db)
):
    """
    Thêm một sản phẩm vào giỏ hàng của người dùng.
    Nếu sản phẩm đã có, số lượng sẽ được cộng dồn.
    """
    user = db.query(UserModel).filter(UserModel.id == item_data.UserID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_cart = get_or_create_user_cart(db, user_id=item_data.UserID)
    if db_cart.Status == "Paid":
        raise HTTPException(status_code=400, detail="Cannot add items to a paid cart")

    item_to_add = CartItemCreate(
        ProductID=item_data.ProductID,
        Quantity=item_data.Quantity
    )
    return cart_items_controller.add_item_to_cart(db, cart_id=db_cart.id, item_data=item_to_add)

@router.get("/", response_model=Dict[str, Any], summary="Get the user's cart details")
async def get_cart(
    UserID: int,  # Nhận UserID từ query
    db: Session = Depends(get_db)
):
    """
    Lấy thông tin chi tiết giỏ hàng của người dùng, bao gồm danh sách sản phẩm.
    """
    user = db.query(UserModel).filter(UserModel.id == UserID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_cart = get_or_create_user_cart(db, user_id=UserID)
    cart_items = cart_items_controller.get_items_in_cart(db, cart_id=db_cart.id)

    product_ids = [item.ProductID for item in cart_items]
    products = db.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()
    product_dict = {p.id: p for p in products}

    items_with_details = []
    total_price = 0
    for item in cart_items:
        product = product_dict.get(item.ProductID)
        if product:
            subtotal = product.Price * item.Quantity
            item_detail = {
                "item_id": item.id,
                "Quantity": item.Quantity,
                "product": ProductSchema.from_orm(product),
                "subtotal": subtotal
            }
            items_with_details.append(item_detail)
            total_price += subtotal

    return {
        "CartID": db_cart.id,
        "UserID": db_cart.UserID,
        "Status": db_cart.Status,
        "items": items_with_details,
        "total_price": total_price
    }

@router.put("/items/{item_id}", response_model=CartItem, summary="Update item quantity in the cart")
async def update_item_quantity(
    item_id: int,
    item_data: CartItemUpdateRequest,  # Nhận Quantity, UserID trong body
    db: Session = Depends(get_db)
):
    """
    Cập nhật số lượng của một sản phẩm trong giỏ hàng.
    """
    user = db.query(UserModel).filter(UserModel.id == item_data.UserID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_cart = get_or_create_user_cart(db, user_id=item_data.UserID)
    if db_cart.Status == "Paid":
        raise HTTPException(status_code=400, detail="Cannot update items in a paid cart")

    cart_item = db.query(CartItemModel).filter(
        CartItemModel.id == item_id,
        CartItemModel.CartID == db_cart.id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found in user's cart")

    item_update = CartItemUpdate(Quantity=item_data.Quantity)
    return cart_items_controller.update_cart_item(db, item_id=item_id, item_data=item_update)

@router.delete("/items/{item_id}", status_code=status.HTTP_200_OK, summary="Remove an item from the cart")
async def remove_item(
    item_id: int,
    UserID: int,  # Nhận UserID từ query
    db: Session = Depends(get_db)
):
    """
    Xóa một sản phẩm khỏi giỏ hàng.
    """
    user = db.query(UserModel).filter(UserModel.id == UserID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_cart = get_or_create_user_cart(db, user_id=UserID)
    if db_cart.Status == "Paid":
        raise HTTPException(status_code=400, detail="Cannot delete items from a paid cart")

    cart_item = db.query(CartItemModel).filter(
        CartItemModel.id == item_id,
        CartItemModel.CartID == db_cart.id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found in user's cart")

    cart_items_controller.delete_cart_item(db, item_id=item_id)
    return {"message": "Item removed successfully"}

@router.post("/checkout", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED, summary="Checkout and create an order")
async def checkout_cart(
    UserID: int,  
    db: Session = Depends(get_db)
):
    """
    Thanh toán giỏ hàng, đánh dấu là đã thanh toán và tạo đơn hàng mới.
    """
    user = db.query(UserModel).filter(UserModel.id == UserID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_cart = get_or_create_user_cart(db, user_id=UserID)
    if db_cart.Status == "Paid":
        raise HTTPException(status_code=400, detail="Cart already paid")

    cart_items = cart_items_controller.get_items_in_cart(db, cart_id=db_cart.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    try:
        db_order = order_controller.create_order(db, user_id=UserID, cart_id=db_cart.id)
        db_cart.Status = "Paid"
        db.commit()
        db.refresh(db_cart)

        new_cart = cart_controller.create_cart(db, user_id=UserID)

        return {
            "message": "Checkout successful",
            "order": Order.from_orm(db_order),
            "CartID": db_cart.id,
            "cart_status": db_cart.Status,
            "new_cart_id": new_cart.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error during checkout: {str(e)}")