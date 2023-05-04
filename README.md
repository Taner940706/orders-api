# Simple Orders API
## RESTful API for Orders
## Details
### The app is based on FastAPI + SQL Alchemy + SQLITE3 + Alembic + JWT (JSON Web Token) + Pydentic + Starlette. It supports the following operations:
### Authentication (auth):
- POST: auth/ - create users
- POST: token/ - create token for authorization
### Orders
- GET: orders/ - get all orders
- GET: orders/{order_id} - get order by order_id
- POST: orders/order - create order
- PUT: orders/{order_id} - update order by order_id
- DELETE: orders/{order_id} - delete order by order_id
### Products
- GET: products/ - get all products
- GET: products/{product_id} - get product by product_id
- POST: products/product - create product
- PUT: products/{product_id} - update product by product_id
- DELETE: products/{product_id} - delete product by product_id
## ScreenShots
![main](https://user-images.githubusercontent.com/59261346/236229718-5a58f928-e2c3-401d-9f0d-285baa95174b.png)
![auth](https://user-images.githubusercontent.com/59261346/236229817-9e3a73e0-5aae-4cfb-8020-a4e956c9bca9.png)
![token](https://user-images.githubusercontent.com/59261346/236229943-718ccf79-d22f-49ba-ad79-aab4c9cd1e4e.png)
![get_all_orders](https://user-images.githubusercontent.com/59261346/236230021-d9bf5db6-a578-4e89-a37e-2b285c6e4a05.png)
![get order by id](https://user-images.githubusercontent.com/59261346/236230104-de19b74f-720d-464b-9e8e-db7cad2f8147.png)
![post orders](https://user-images.githubusercontent.com/59261346/236230170-18e066c1-ddc3-4be3-9555-b41864f99729.png)
![put order by id](https://user-images.githubusercontent.com/59261346/236230233-f60f0d55-be5c-486d-baa2-b2eb87f84b17.png)
![delete order](https://user-images.githubusercontent.com/59261346/236230293-9654f27c-85a3-4f38-ba66-7aac6aabda71.png)
![get all products](https://user-images.githubusercontent.com/59261346/236230387-b57cba46-c334-4f82-be71-4ad868fc8c62.png)
![get product by id](https://user-images.githubusercontent.com/59261346/236230424-c1d61b09-855c-43f0-9c50-f0d4688eee28.png)
![post products](https://user-images.githubusercontent.com/59261346/236230495-315034cd-215c-490b-be37-2f48931b8871.png)
![put products by id](https://user-images.githubusercontent.com/59261346/236230570-6d81100c-4dac-484e-b223-ec59326a07e9.png)
![delete product](https://user-images.githubusercontent.com/59261346/236230641-b619de6d-c756-4ea8-9c84-8cf6ddbf1d01.png)

