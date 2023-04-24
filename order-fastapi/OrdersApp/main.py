from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from models import Orders, Products
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/orders')
async def read_all_orders(db: Annotated[Session, Depends(get_db)]):
    return db.query(Orders).all()


@app.get('/products/')
async def read_all_products(db: Annotated[Session, Depends(get_db)]):
    return db.query(Products).all()


@app.get('/orders/{order_id}')
async def get_order_by_id(db: Annotated[Session, Depends(get_db)], order_id: int):
    order_model = db.query(Orders).filter(Orders.id == order_id).first()
    if order_model is not None:
        return order_model
    raise HTTPException(status_code=404, detail="Order not found!")


@app.get('/products/{product_id}')
async def get_product_by_id(db: Annotated[Session, Depends(get_db)], product_id: int):
    product_model = db.query(Products).filter(Products.id == product_id).first()
    if product_model is not None:
        return product_model
    raise HTTPException(status_code=404, detail="Product not found!")