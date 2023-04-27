from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Orders
from database import SessionLocal
from starlette import status
from .auth import get_current_user
routers = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OrdersRequest(BaseModel):
    added_date: str
    owner: int


user_dependency = Annotated[dict, Depends(get_current_user)]


@routers.get('/orders', status_code=status.HTTP_200_OK)
async def read_all_orders(user: user_dependency, db: Annotated[Session, Depends(get_db)]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    return db.query(Orders).filter(Orders.owner_id == user.get('id')).all()


@routers.get('/orders/{order_id}', status_code=status.HTTP_200_OK)
async def get_order_by_id(user: user_dependency, db: Annotated[Session, Depends(get_db)], order_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    order_model = db.query(Orders).filter(Orders.id == order_id).filter(Orders.owner_id == user.get('id')).first()
    if order_model is not None:
        return order_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")


@routers.post('/orders/order', status_code=status.HTTP_201_CREATED)
async def create_order(user: user_dependency,db: Annotated[Session, Depends(get_db)], order_request: OrdersRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    order_model = Orders(**order_request.dict(), owner_id=user.get('id'))
    db.add(order_model)
    db.commit()


@routers.put('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_order_by_id(user: user_dependency, db: Annotated[Session, Depends(get_db)], order_request: OrdersRequest, order_id: int):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is failed!")
    order_model = db.query(Orders).filter(Orders.id == order_id).filter(Orders.owner_id == user.get('id')).first()
    if order_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")
    order_model.added_date = order_request.added_date
    order_model.owner_id = order_request.owner

    db.add(order_model)
    db.commit()


@routers.delete('/orders/{order_id}')
async def delete_order_by_id(db: Annotated[Session, Depends(get_db)], order_id: int):
    order_model = db.query(Orders).filter(Orders.id == order_id).first()
    if order_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.query(Orders).filter(Orders.id == order_id).delete()
    db.commit()

