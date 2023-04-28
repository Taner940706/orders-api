from fastapi import FastAPI
import models
from database import engine
from routers import auth, orders, products

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# include routers
app.include_router(auth.routers)
app.include_router(orders.routers)
app.include_router(products.routers)
