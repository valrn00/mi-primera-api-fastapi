from fastapi import APIRouter, HTTPException, status
from models.product import ProductCreate, ProductUpdate, ProductResponse
from services.product_service import ProductService
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def get_products():
    return ProductService.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id: int):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return product

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    try:
        new_product = ProductService.create_product(product)
        return new_product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate):
    updated_product = ProductService.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    if not ProductService.delete_product(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return {"detail": "Producto eliminado"}