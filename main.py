from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# -----------------
# Solo se inicializa la aplicación una vez
# -----------------
app = FastAPI(title="My Enhanced API - Week 2")

# -----------------
# Definición de modelos de datos para Pydantic
# -----------------
class Product(BaseModel):
    name: str
    price: int
    available: bool = True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Successful operation"

class ProductListResponse(BaseModel):
    products: List[dict]
    total: int
    message: str = "List retrieved"

# -----------------
# Almacenamiento temporal para productos
# -----------------
products = []

# -----------------
# Todos tus endpoints, combinados y actualizados
# -----------------

# Endpoint principal
@app.get("/")
def hello_world() -> dict:
    return {"message": "Week 2 API with Pydantic and Type Hints!"}

# Endpoint para crear un nuevo producto con response_model
@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)

    return ProductResponse(**product_dict, message="Product created")

# Endpoint para ver todos los productos con response_model
@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

# Endpoints con Parámetros de Ruta
@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/categories/{category}/products/{product_id}")
def product_by_category(category: str, product_id: int) -> dict:
    return {
        "category": category,
        "product_id": product_id,
        "message": f"Searching product {product_id} in {category}"
    }

# Endpoint con Parámetros de Query
@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None,
    available: Optional[bool] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    if available is not None:
        results = [p for p in results if p["available"] == available]

    return {"results": results, "total": len(results)}

# Nota: Se han eliminado los endpoints antiguos y se han reemplazado con la nueva lógica.