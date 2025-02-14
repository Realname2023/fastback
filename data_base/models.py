from typing import List
from sqlalchemy import DateTime, ForeignKey, String, Text, BigInteger, func, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Adminer(Base):
    __tablename__ = 'admins'

    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)  # Хэш пароля
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String(150), nullable=True)
    full_name: Mapped[str] = mapped_column(String(500), nullable=False)

    clients: Mapped['Client'] = relationship(back_populates="user", lazy="selectin")

    def __str__(self):
        return self.full_name
    

class City(Base):
    __tablename__ = 'cities'

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    verbose_name: Mapped[str] = mapped_column(String(500), nullable=True)

    goods: Mapped[List['Good']] = relationship(back_populates="city", lazy="selectin")

    def __str__(self):
        return self.name



class Client(Base):
    __tablename__ = 'clients'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'), unique=True)
    org_name: Mapped[str] = mapped_column(Text, nullable=True)
    client_city: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)
    is_contract: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user: Mapped['User'] = relationship(back_populates='clients', lazy="selectin")

    def __str__(self):
        return self.org_name


class Category(Base):
    __tablename__ = 'categories'

    photo: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    verbose_name: Mapped[str] = mapped_column(String(500), nullable=True)

    goods: Mapped[List['Good']] = relationship(back_populates="category", lazy="selectin")

    def __str__(self):
        return self.name



class Good(Base):
    __tablename__ = 'goods'  

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    city_id: Mapped[int] = mapped_column(ForeignKey('cities.id', ondelete='CASCADE'))
    photo: Mapped[str] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    verbose_name: Mapped[str] = mapped_column(String(500), nullable=True)
    unit: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_delivery: Mapped[bool] = mapped_column(Boolean, default=False)
    is_arenda: Mapped[bool] = mapped_column(Boolean, default=False)
    price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    delivery_price: Mapped[int] = mapped_column(BigInteger, nullable=True)
    arenda_contract:Mapped[int] = mapped_column(BigInteger, nullable=True)
    delivery_terms: Mapped[str] = mapped_column(Text, nullable=True)
    arenda_terms: Mapped[str] = mapped_column(Text, nullable=True)
    b_id: Mapped[str] = mapped_column(String(50))

    city: Mapped['City'] = relationship(back_populates="goods", lazy="selectin")
    category: Mapped['Category'] = relationship(back_populates="goods", lazy="selectin")

    def __str__(self):
        return self.name

   
class Cart(Base):
    __tablename__ = 'carts'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    good_id: Mapped[int] = mapped_column(ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int] = mapped_column(BigInteger)
    arenda_time: Mapped[int] = mapped_column(Integer, nullable=True)
    is_arenda: Mapped[bool] = mapped_column(Boolean, default=False)
    is_delivery: Mapped[bool] = mapped_column(Boolean, default=False)
    is_contract: Mapped[bool] = mapped_column(Boolean, default=False)
    total_price: Mapped[int] = mapped_column(BigInteger)
    
    user: Mapped['User'] = relationship(backref='carts', lazy="selectin")
    good: Mapped['Good'] = relationship(backref='carts', lazy="selectin")

    def __str__(self) -> str:
        return self.user.full_name


class Order(Base):
    __tablename__ = 'orders'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    order_text: Mapped[str] = mapped_column(Text)
    
    user: Mapped['User'] = relationship(backref='orders', lazy="selectin")

# class Actions(Base):
#     __tablename__ = 'actions'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     photo: Mapped[str] = mapped_column(String(1000))
#     text: Mapped[str] = mapped_column(Text)
