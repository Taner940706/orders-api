from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Products
from database import SessionLocal
from starlette import status

routers = APIRouter()


# session local for database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# products base model
class ProductsRequest(BaseModel):
    product_name: str = Field(min_length=3, max_length=30)
    price: float
    description: str


# get all products
@routers.get('/products/', status_code=status.HTTP_200_OK)
async def read_all_products(db: Annotated[Session, Depends(get_db)]):
    return db.query(Products).all()


# get product by is
@routers.get('/products/{product_id}', status_code=status.HTTP_200_OK)
async def get_product_by_id(db: Annotated[Session, Depends(get_db)], product_id: int):
    product_model = db.query(Products).filter(Products.id == product_id).first()
    if product_model is not None:
        return product_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")


# create product
@routers.post('/products/product', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[Session, Depends(get_db)], product_request: ProductsRequest):
    product_request = Products(**product_request.dict())
    db.add(product_request)
    db.commit()


# update product by id
@routers.put('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_product_by_id(db: Annotated[Session, Depends(get_db)], product_request: ProductsRequest, product_id: int):
    product_model = db.query(Products).filter(Products.id == product_id).first()
    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!")
    product_model.product_name = product_request.product_name
    product_model.price = product_request.price
    product_model.description = product_request.description

    db.add(product_model)
    db.commit()


# delete product by id
@routers.delete('/products/{product_id}')
async def delete_product_by_id(db: Annotated[Session, Depends(get_db)], product_id: int):
    product_model = db.query(Products).filter(Products.id == product_id).first()
    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.query(Products).filter(Products.id == product_id).delete()
    db.commit()