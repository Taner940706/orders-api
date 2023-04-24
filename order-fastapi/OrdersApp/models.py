from database import Base
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Float


class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    added_date = Column(DateTime)
    owner_id = Column(Integer, ForeignKey('users.id'))


class Products(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    price = Column(Float)
    description = Column(String)

    
class OrderDetails(Base):

    __tablename__ = 'orderdetails'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))