from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from models import Orders, Products
from database import engine, SessionLocal
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OrdersRequest(BaseModel):
    added_date: str
    owner: str = Field(min_length=3, max_length=15)


class ProductsRequest(BaseModel):
    product_name: str = Field(min_length=3, max_length=30)
    price: float
    description: str


@app.get('/orders', status_code=status.HTTP_200_OK)
async def read_all_orders(db: Annotated[Session, Depends(get_db)]):
    return db.query(Orders).all()


@app.get('/products/', status_code=status.HTTP_200_OK)
async def read_all_products(db: Annotated[Session, Depends(get_db)]):
    return db.query(Products).all()


@app.get('/orders/{order_id}', status_code=status.HTTP_200_OK)
async def get_order_by_id(db: Annotated[Session, Depends(get_db)], order_id: int):
    order_model = db.query(Orders).filter(Orders.id == order_id).first()
    if order_model is not None:
        return order_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")


@app.get('/products/{product_id}', status_code=status.HTTP_200_OK)
async def get_product_by_id(db: Annotated[Session, Depends(get_db)], product_id: int):
    product_model = db.query(Products).filter(Products.id == product_id).first()
    if product_model is not None:
        return product_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")


@app.post('/orders/order', status_code=status.HTTP_201_CREATED)
async def create_order(db: Annotated[Session, Depends(get_db)], order_request: OrdersRequest):
    order_model = Orders(**order_request.dict())
    db.add(order_model)
    db.commit()


@app.post('/products/product', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[Session, Depends(get_db)], product_request: ProductsRequest):
    product_request = Products(**product_request.dict())
    db.add(product_request)
    db.commit()