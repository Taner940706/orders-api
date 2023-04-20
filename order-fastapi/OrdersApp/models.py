from database import Base
from sqlalchemy import Column, DateTime, String, Integer

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    added_date = Column(DateTime)