from sqlalchemy import (Column, ForeignKey, Integer, String, Table,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    description = Column(String)

    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    orders = relationship("Order", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    street = Column(String)
    city = Column(String)
    postal_code = Column(String)

    # Связь многие-к-одному с пользователем
    user = relationship("User", back_populates="addresses")

    # Связь один-ко-многим с заказами
    orders = relationship("Order", back_populates="delivery_address")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)

    # Связь многие-ко-многим с заказами
    orders = relationship("Order", secondary=order_product, back_populates="products")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))
    total_amount = Column(Integer)

    # Связь многие-к-одному с пользователем
    user = relationship("User", back_populates="orders")

    # Связь многие-к-одному с адресом доставки
    delivery_address = relationship("Address", back_populates="orders")

    # Связь многие-ко-многим с продуктами
    products = relationship("Product", secondary=order_product, back_populates="orders")
