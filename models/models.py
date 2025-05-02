from sqlalchemy import Date, DateTime, Table,Column, Text, DECIMAL, func, Boolean
from sqlalchemy.types import Integer,String
from config.db import meta
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))


class Flower(Base):
    __tablename__ = 'flowers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    # image_url sẽ lưu đường dẫn tương đối tới file trên server, ví dụ: /media/flower_images/abc.jpg
    image_url = Column(String(255), nullable=True)
    flower_type = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
class FlowerTypes(Base):
    __tablename__ = 'FlowerTypes'
    id = Column(Integer, primary_key=True, index = True)
    Name = Column(String(255), nullable = False)
    Description  = Column(String(255), nullable = True)

class Categories(Base):
    __tablename__ = 'Categories'
    id = Column(Integer, primary_key=True, index = True)
    Name = Column(String(255), nullable = False)
    Description  = Column(String(255), nullable = True)

class Products(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255), nullable=False)
    Description = Column(Text, nullable=True)
    Price = Column(Integer, nullable=False)
    DiscountedPrice = Column(Integer, nullable=True)
    StockQuantity = Column(Integer, default=0)
    CategoryID = Column(Integer, nullable=True)
    ImageURL = Column(String(255), nullable=True)
    IsFreeship = Column(Boolean, default=False)
    FlowerTypeID = Column(Integer, nullable=False)

class Cart(Base):
    __tablename__ = 'Cart'
    id = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, nullable=False)
    Status = Column(String(20), nullable=False, default='Pending')
    CreatedAt = Column(DateTime, server_default=func.current_timestamp())
    UpdatedAt = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class CartItems(Base):
    __tablename__ = 'CartItems'
    id = Column(Integer, primary_key=True, index=True)
    CartID = Column(Integer, nullable=False)
    ProductID = Column(Integer, nullable=False)
    Quantity = Column(Integer, nullable=False, default=1)
    CreatedAt = Column(DateTime, server_default=func.current_timestamp())
    UpdatedAt = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # UserID, có thể null theo thiết kế
    order_date = Column(Date, server_default=func.curdate())
    total_amount = Column(Integer, nullable=True)
    status = Column(String(50), nullable=False, default='Pending')
    shipping_address = Column(Text, nullable=True)
    delivery_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

# Model cho OrderDetails
class OrderDetails(Base):
    __tablename__ = 'OrderDetails'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=True)  # OrderID, có thể null theo thiết kế
    product_id = Column(Integer, nullable=True)  # ProductID
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
