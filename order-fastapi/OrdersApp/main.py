from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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


@app.get('/orders/')
def read_all_orders(db: Annotated[Session, Depends(get_db)]):
    return db.query(Orders).all()


@app.get('/products/')
def read_all_products(db: Annotated[Session, Depends(get_db)]):
    return db.query(Products).all()
