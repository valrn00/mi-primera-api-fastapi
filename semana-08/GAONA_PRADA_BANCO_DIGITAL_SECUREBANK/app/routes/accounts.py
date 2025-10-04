from fastapi import APIRouter, HTTPException, Query, Path, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime
from ..models.schemas import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
    ListAccountsResponse,
    ErrorResponse
)
from ..docs.descriptions import (
    ENDPOINT_DESCRIPTIONS,
    RESPONSE_DESCRIPTIONS,
    RESPONSE_EXAMPLES
)

router = APIRouter(
    prefix="/api/v1/accounts",
    tags=["accounts"],
    responses={
        404: {
            "model": ErrorResponse,
            "description": RESPONSE_DESCRIPTIONS[404],
            "content": {
                "application/json": {
                    "examples": {
                        "not_found": RESPONSE_EXAMPLES["error_not_found"]
                    }
                }
            }
        },
        422: {
            "model": ErrorResponse,
            "description": RESPONSE_DESCRIPTIONS[422],
            "content": {
                "application/json": {
                    "examples": {
                        "validation": RESPONSE_EXAMPLES["error_validation"]
                    }
                }
            }
        }
    }
)

# Simulación de base de datos
accounts_db = []
account_id_counter = 1

@router.post(
    "/",
    response_model=AccountResponse,
    status_code=201,
    summary="Crear nueva cuenta bancaria",
    description=ENDPOINT_DESCRIPTIONS["create_account"],
    response_description=RESPONSE_DESCRIPTIONS[201],
    responses={
        201: {
            "model": AccountResponse,
            "description": RESPONSE_DESCRIPTIONS[201],
            "content": {
                "application/json": {
                    "examples": {
                        "created": RESPONSE_EXAMPLES["account_created"]
                    }
                }
            }
        }
    }
)
async def create_account(account: AccountCreate):
    """Crear una nueva cuenta bancaria en SecureBank"""
    global account_id_counter
    if any(a["account_id"] == account.account_id for a in accounts_db):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ACCOUNT_ID_DUPLICATED",
                "message": f"El account_id {account.account_id} ya existe",
                "http_code": 400,
                "timestamp": datetime.now().isoformat()
            }
        )
    new_account = {
        "id": account_id_counter,
        **account.model_dump(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "status": "active"
    }
    accounts_db.append(new_account)
    account_id_counter += 1
    return AccountResponse(**new_account)

@router.get(
    "/",
    response_model=ListAccountsResponse,
    summary="Listar cuentas con paginación",
    description=ENDPOINT_DESCRIPTIONS["list_accounts"],
    response_description=RESPONSE_DESCRIPTIONS[200],
    responses={
        200: {
            "model": ListAccountsResponse,
            "description": RESPONSE_DESCRIPTIONS[200],
            "content": {
                "application/json": {
                    "examples": {
                        "list": RESPONSE_EXAMPLES["account_list"]
                    }
                }
            }
        }
    }
)
async def list_accounts(
    page: int = Query(1, ge=1, description="Número de página", example=1),
    limit: int = Query(10, ge=1, le=100, description="Cuentas por página", example=10),
    account_type: Optional[AccountTypeEnum] = Query(None, description="Filtrar por tipo de cuenta", example="savings"),
    min_balance: Optional[float] = Query(None, ge=0.0, description="Saldo mínimo", example=1000.0),
    search: Optional[str] = Query(None, min_length=3, description="Búsqueda por nombre", example="Juan"),
    sort_by: str = Query("account_id", regex="^(account_id|balance|customer_name)$", description="Campo para ordenar", example="balance"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Dirección del ordenamiento", example="asc")
):
    """Obtener lista paginada de cuentas con filtros"""
    filtered_accounts = accounts_db.copy()
    if account_type:
        filtered_accounts = [a for a in filtered_accounts if a["account_type"] == account_type]
    if min_balance is not None:
        filtered_accounts = [a for a in filtered_accounts if a["balance"] >= min_balance]
    if search:
        search_lower = search.lower()
        filtered_accounts = [a for a in filtered_accounts if search_lower in a["customer_name"].lower()]
    
    reverse_order = sort_order == "desc"
    if sort_by == "account_id":
        filtered_accounts.sort(key=lambda x: x["account_id"], reverse=reverse_order)
    elif sort_by == "balance":
        filtered_accounts.sort(key=lambda x: x["balance"], reverse=reverse_order)
    elif sort_by == "customer_name":
        filtered_accounts.sort(key=lambda x: x["customer_name"], reverse=reverse_order)
    
    start = (page - 1) * limit
    end = start + limit
    paginated_accounts = filtered_accounts[start:end]
    
    return ListAccountsResponse(
        accounts=[AccountResponse(**a) for a in paginated_accounts],
        total=len(filtered_accounts),
        page=page,
        per_page=limit
    )

@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Obtener cuenta por ID",
    description=ENDPOINT_DESCRIPTIONS["get_account"],
    response_description=RESPONSE_DESCRIPTIONS[200]
)
async def get_account(account_id: str = Path(..., description="ID de la cuenta", example="ACC12345")):
    """Obtener detalles de una cuenta específica"""
    for account in accounts_db:
        if account["account_id"] == account_id:
            return AccountResponse(**account)
    raise HTTPException(
        status_code=404,
        detail={
            "error": "ACCOUNT_NOT_FOUND",
            "message": f"La cuenta con ID {account_id} no fue encontrada",
            "http_code": 404,
            "timestamp": datetime.now().isoformat()
        }
    )