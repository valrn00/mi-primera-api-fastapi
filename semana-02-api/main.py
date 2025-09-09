from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="My API with Pydantic")

# Modelo Pydantic básico
class Product(BaseModel):
    name: str
    price: int  # en centavos para evitar decimales
    available: bool = True  # valor por defecto

# Lista temporal de productos
products: list[dict] = []

# Endpoint raíz
@app.get("/", response_model=dict)
def hello_world() -> dict:
    return {"message": "API with Pydantic!"}

# POST: Crear producto con validación automática
@app.post("/products", response_model=dict)
def create_product(product: Product) -> dict:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return {"message": "Product created", "product": product_dict}

# GET: Listar todos los productos
@app.get("/products", response_model=dict)
def get_products() -> dict:
    return {"products": products, "total": len(products)}

# GET: Ver producto por ID
@app.get("/products/{id}", response_model=dict)
def get_product_by_id(id: int) -> dict:
    for product in products:
        if product["id"] == id:
            return {"product": product}
    return {"error": "Product not found"}

# GET: Buscar productos por nombre
@app.get("/search", response_model=dict)
def search_products(name: str) -> dict:
    results = [p for p in products if name.lower() in p["name"].lower()]
    return {"results": results, "total": len(results)}

# Modelo Pydantic más completo (opcional)
class CompleteUser(BaseModel):
    name: str
    age: int
    email: str
    phone: Optional[str] = None
    active: bool = True

# POST: Crear usuario con validación automática
@app.post("/users", response_model=dict)
def create_user(user: CompleteUser) -> dict:
    return {"user": user.dict(), "valid": True}