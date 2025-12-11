import uuid
from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Связующая таблица для заказов и продуктов
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    orders = relationship("Order", back_populates="user", lazy="selectin")

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id}, street='{self.street}', city='{self.city}')"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship(
        "Order", secondary=order_product, back_populates="products", lazy="selectin"
    )

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders", lazy="selectin")
    delivery_address = relationship("Address", lazy="selectin")
    products = relationship(
        "Product", secondary=order_product, back_populates="orders", lazy="selectin"
    )

    def __repr__(self):
        return f"Order(id={self.id}, total_amount={self.total_amount}, status='{self.status}')"
