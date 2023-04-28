from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Orders
from database import SessionLocal
from starlette import status
from .auth import get_current_user
routers = APIRouter()


# session local for database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# orders base model
class OrdersRequest(BaseModel):
    added_date: str


# simplify dependency for get current user
user_dependency = Annotated[dict, Depends(get_current_user)]


# get all orders
@routers.get('/orders', status_code=status.HTTP_200_OK)
async def read_all_orders(user: user_dependency, db: Annotated[Session, Depends(get_db)]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    return db.query(Orders).filter(Orders.owner_id == user.get('id')).all()


# get order by id
@routers.get('/orders/{order_id}', status_code=status.HTTP_200_OK)
async def get_order_by_id(user: user_dependency, db: Annotated[Session, Depends(get_db)], order_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    order_model = db.query(Orders).filter(Orders.id == order_id).filter(Orders.owner_id == user.get('id')).first()
    if order_model is not None:
        return order_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")


# create order
@routers.post('/orders/order', status_code=status.HTTP_201_CREATED)
async def create_order(user: user_dependency, db: Annotated[Session, Depends(get_db)], order_request: OrdersRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    order_model = Orders(**order_request.dict(), owner_id=user.get('id'))
    db.add(order_model)
    db.commit()


# update order by id
@routers.put('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_order_by_id(user: user_dependency, db: Annotated[Session, Depends(get_db)], order_request: OrdersRequest, order_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    order_model = db.query(Orders).filter(Orders.id == order_id).filter(Orders.owner_id == user.get('id')).first()
    if order_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    order_model.added_date = order_request.added_date

    db.add(order_model)
    db.commit()


# delete order by id
@routers.delete('/orders/{order_id}')
async def delete_order_by_id(user: user_dependency, db: Annotated[Session, Depends(get_db)], order_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    order_model = db.query(Orders).filter(Orders.id == order_id).filter(Orders.owner_id == user.get('id')).first()
    if order_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.query(Orders).filter(Orders.id == order_id).filter(Orders.owner_id == user.get('id')).delete()
    db.commit()

