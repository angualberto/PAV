from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, Float, Boolean,
                        ForeignKey, Text)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)  # para soft-delete

class Customer(BaseModel):
    __tablename__ = "customers"
    name = Column(String(120), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)
    orders = relationship("Order", back_populates="customer")

class Supplier(BaseModel):
    __tablename__ = "suppliers"
    name = Column(String(120), nullable=False)
    contact = Column(String(120), nullable=True)

class Product(BaseModel):
    __tablename__ = "products"
    sku = Column(String(40), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    inventory = relationship("Inventory", uselist=False, back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class Inventory(BaseModel):
    __tablename__ = "inventory"
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, unique=True)
    quantity = Column(Integer, default=0, nullable=False)
    product = relationship("Product", back_populates="inventory")

class Order(BaseModel):
    __tablename__ = "orders"
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    total = Column(Float, default=0.0)
    status = Column(String(30), default="OPEN")
    seller = Column(String(80), nullable=True)
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(BaseModel):
    __tablename__ = "order_items"
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
