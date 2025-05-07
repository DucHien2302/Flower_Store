from sqlalchemy import Date, DateTime, Column, Text, DECIMAL, func, Boolean
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

class Informations(Base):
    __tablename__ = 'Informations'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    full_name = Column(String(64), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(Boolean, nullable=True)
    address = Column(String(512), nullable=True)
    user_id = Column(Integer, nullable=False)

class SysUser(Base):
    __tablename__ = 'SysUser'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), nullable=False)
    password = Column(String(1024), nullable=False)

class Cart(Base):
    __tablename__ = 'Cart'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    amount_total = Column(DECIMAL(10, 2), nullable=False)
    create_at = Column(Date, nullable=False)
    update_at = Column(Date, nullable=False)

class CartDetail(Base):
    __tablename__ = 'CartDetail'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    cart_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(DECIMAL(10, 2), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    ischecked = Column(Boolean, default=False)
    create_at = Column(Date, nullable=False)
    update_at = Column(Date, nullable=False)

class Invoice(Base):
    __tablename__ = 'Invoice'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    create_at = Column(Date, nullable=False)
    amount_total = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Boolean, default=False)

class InvoiceDetail(Base):
    __tablename__ = 'InvoiceDetail'
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(DECIMAL(10, 2), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)

class VnPayment(Base):
    __tablename__ = 'VnPayment'
    Amount = Column(Integer, primary_key=True, index=True)
    BankCode = Column(String(128), nullable=False)
    BankTranNo = Column(String(128), nullable=False)
    CardType = Column(String(128), nullable=False)
    OrderInfo = Column(String(128), nullable=False)
    PayDate = Column(String(128), nullable=False)
    ResponseCode = Column(String(128), nullable=False)
    TmnCode = Column(String(128), nullable=False)
    TransactionNo = Column(String(128), nullable=False)
    TransactionStatus = Column(String(128), nullable=False)
    TxnRef = Column(String(128), nullable=False)