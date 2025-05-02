from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from config.db import get_db
from models.models import User as UserModel, Orders as OrderModel, OrderDetails as OrderDetailModel, Products as ProductModel
from schemas.orders import Order, OrderCreate, OrderUpdate
from schemas.order_details import OrderDetail
from schemas.products import Product as ProductSchema
from controller import orders as order_controller
from controller import order_details as order_detail_controller
from controller import products as product_controller

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

async def get_current_user(db: Session = Depends(get_db)) -> UserModel:
    user = db.query(UserModel).filter(UserModel.id == 1).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/", response_model=List[Dict[str, Any]], summary="Get user's orders")
async def get_orders(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Lấy danh sách đơn hàng của người dùng hiện tại.
    """
    orders = order_controller.get_orders_by_user_id(db, user_id=current_user.id)
    result = []
    for order in orders:
        order_details = order_detail_controller.get_order_details_by_order_id(db, order_id=order.id)
        details_with_products = []
        for detail in order_details:
            product = product_controller.get_product_by_id(db, product_id=detail.product_id)
            if product:
                details_with_products.append({
                    "detail_id": detail.id,
                    "quantity": detail.quantity,
                    "unit_price": detail.unit_price,
                    "product": ProductSchema.from_orm(product)
                })
        result.append({
            "order_id": order.id,
            "user_id": order.user_id,
            "order_date": order.order_date,
            "total_amount": order.total_amount,
            "status": order.status,
            "shipping_address": order.shipping_address,
            "delivery_date": order.delivery_date,
            "details": details_with_products
        })
    return result

@router.get("/{order_id}", response_model=Dict[str, Any], summary="Get order details by ID")
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Lấy chi tiết đơn hàng theo ID.
    """
    order = order_controller.get_order_by_id(db, order_id=order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    
    order_details = order_detail_controller.get_order_details_by_order_id(db, order_id=order_id)
    details_with_products = []
    for detail in order_details:
        product = product_controller.get_product_by_id(db, product_id=detail.product_id)
        if product:
            details_with_products.append({
                "detail_id": detail.id,
                "quantity": detail.quantity,
                "unit_price": detail.unit_price,
                "product": ProductSchema.from_orm(product)
            })
    
    return {
        "order_id": order.id,
        "user_id": order.user_id,
        "order_date": order.order_date,
        "total_amount": order.total_amount,
        "status": order.status,
        "shipping_address": order.shipping_address,
        "delivery_date": order.delivery_date,
        "details": details_with_products
    }

@router.put("/{order_id}", response_model=Order, summary="Update order")
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Cập nhật thông tin đơn hàng (ví dụ: status, shipping_address).
    """
    order = order_controller.get_order_by_id(db, order_id=order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    
    return order_controller.update_order(db, order_id=order_id, order_data=order_data)

@router.delete("/{order_id}", status_code=status.HTTP_200_OK, summary="Delete order")
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Xóa đơn hàng.
    """
    order = order_controller.get_order_by_id(db, order_id=order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    
    order_controller.delete_order(db, order_id=order_id)
    return {"message": "Order deleted successfully"}