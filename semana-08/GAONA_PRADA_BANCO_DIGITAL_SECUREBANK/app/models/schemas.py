from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AccountTypeEnum(str, Enum):
    """Tipos de cuentas bancarias"""
    SAVINGS = "savings"
    CHECKING = "checking"

class TransactionTypeEnum(str, Enum):
    """Tipos de transacciones bancarias"""
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

class AccountBase(BaseModel):
    """Esquema base para cuentas bancarias"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_id": "ACC12345",
                "customer_name": "Juan Perez",
                "balance": 1000.0,
                "account_type": "savings"
            }
        }
    )

    account_id: str = Field(
        ...,
        description="Identificador único de la cuenta",
        min_length=8,
        max_length=8,
        pattern="^ACC[0-9]{5}$",
        examples=["ACC12345", "ACC67890"]
    )
    customer_name: str = Field(
        ...,
        description="Nombre completo del titular de la cuenta",
        min_length=5,
        max_length=100,
        examples=["Juan Perez", "Maria Gomez"]
    )
    balance: float = Field(
        ...,
        description="Saldo actual de la cuenta en USD",
        ge=0.0,
        examples=[1000.0, 2500.75]
    )
    account_type: AccountTypeEnum = Field(
        ...,
        description="Tipo de cuenta bancaria",
        examples=["savings", "checking"]
    )

class AccountCreate(AccountBase):
    """Esquema para crear cuentas"""
    pass

class AccountUpdate(BaseModel):
    """Esquema para actualizar cuentas"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_name": "Juan Perez Actualizado",
                "account_type": "checking",
                "balance": 1500.0
            }
        }
    )
    customer_name: Optional[str] = Field(None, min_length=5, max_length=100)
    account_type: Optional[AccountTypeEnum] = None
    balance: Optional[float] = Field(None, ge=0.0)

class AccountResponse(AccountBase):
    """Esquema de respuesta para cuentas"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_id": "ACC12345",
                "customer_name": "Juan Perez",
                "balance": 1000.0,
                "account_type": "savings",
                "created_at": "2025-10-03T09:00:00",
                "updated_at": "2025-10-03T09:00:00",
                "status": "active"
            }
        }
    )
    id: int = Field(..., description="ID único generado", examples=[1, 2])
    created_at: datetime = Field(..., description="Fecha de creación", examples=["2025-10-03T09:00:00"])
    updated_at: datetime = Field(..., description="Fecha de última actualización", examples=["2025-10-03T09:00:00"])
    status: str = Field(..., description="Estado de la cuenta", examples=["active", "inactive"])

class TransactionBase(BaseModel):
    """Esquema base para transacciones bancarias"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id": "TXN12345",
                "account_id": "ACC12345",
                "amount": 500.0,
                "transaction_type": "transfer",
                "metodo_pago": "tarjeta"
            }
        }
    )
    transaction_id: str = Field(
        ...,
        description="Identificador único de la transacción",
        min_length=8,
        max_length=8,
        pattern="^TXN[0-9]{5}$",
        examples=["TXN12345", "TXN67890"]
    )
    account_id: str = Field(
        ...,
        description="Identificador de la cuenta asociada",
        min_length=8,
        max_length=8,
        pattern="^ACC[0-9]{5}$",
        examples=["ACC12345", "ACC67890"]
    )
    amount: float = Field(
        ...,
        description="Monto de la transacción en USD",
        ge=0.0,
        examples=[500.0, 1000.0]
    )
    transaction_type: TransactionTypeEnum = Field(
        ...,
        description="Tipo de transacción",
        examples=["transfer", "deposit", "withdrawal"]
    )
    metodo_pago: str = Field(
        ...,
        description="Método de pago utilizado",
        examples=["tarjeta", "transferencia"]
    )

class TransactionCreate(TransactionBase):
    """Esquema para crear transacciones"""
    pass

class TransactionResponse(TransactionBase):
    """Esquema de respuesta para transacciones"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id": "TXN12345",
                "account_id": "ACC12345",
                "amount": 500.0,
                "transaction_type": "transfer",
                "metodo_pago": "tarjeta",
                "fecha_transaccion": "2025-10-03T09:00:00",
                "status": "completed"
            }
        }
    )
    fecha_transaccion: datetime = Field(..., description="Fecha de la transacción", examples=["2025-10-03T09:00:00"])
    status: str = Field(..., description="Estado de la transacción", examples=["completed", "pending"])

class ListAccountsResponse(BaseModel):
    """Respuesta para lista de cuentas"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "accounts": [
                    {
                        "account_id": "ACC12345",
                        "customer_name": "Juan Perez",
                        "balance": 1000.0,
                        "account_type": "savings",
                        "status": "active"
                    }
                ],
                "total": 1,
                "page": 1,
                "per_page": 10
            }
        }
    )
    accounts: List[AccountResponse] = Field(..., description="Lista de cuentas")
    total: int = Field(..., description="Total de cuentas", examples=[25, 100])
    page: int = Field(..., description="Página actual", examples=[1, 2])
    per_page: int = Field(..., description="Cuentas por página", examples=[10, 20])

class ErrorResponse(BaseModel):
    """Esquema estándar para respuestas de error"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "ACCOUNT_NOT_FOUND",
                "message": "La cuenta con ID ACC99999 no fue encontrada",
                "http_code": 404,
                "timestamp": "2025-10-03T09:00:00"
            }
        }
    )
    error: str = Field(..., description="Código de error")
    message: str = Field(..., description="Mensaje descriptivo del error")
    http_code: int = Field(..., description="Código HTTP del error")
    timestamp: datetime = Field(..., description="Momento del error")