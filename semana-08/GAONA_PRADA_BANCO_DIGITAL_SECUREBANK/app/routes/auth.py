from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.schemas import ErrorResponse
from ..docs.descriptions import RESPONSE_DESCRIPTIONS, RESPONSE_EXAMPLES
from ..database import get_db
from ..auth.auth_handler import create_access_token, authenticate_user
from ..models.db_models import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        401: {
            "model": ErrorResponse,
            "description": RESPONSE_DESCRIPTIONS[401],
            "content": {
                "application/json": {"examples": {"validation": RESPONSE_EXAMPLES["error_validation"]}}
            },
        },
    },
)

@router.post(
    "/login",
    response_model=dict,
    summary="Autenticar usuario",
    description="Autentica un usuario y retorna un token JWT",
    response_description="Token de acceso generado exitosamente",
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autenticar usuario con credenciales."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "INVALID_CREDENTIALS",
                "message": "Credenciales inválidas",
                "http_code": 401,
                "timestamp": datetime.now().isoformat(),
            },
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post(
    "/logout",
    response_model=dict,
    summary="Cerrar sesión",
    description="Invalida el token del usuario (simulado)",
    response_description="Sesión cerrada exitosamente",
)
async def logout():
    """Cerrar sesión del usuario."""
    return {"message": "Sesión cerrada exitosamente"}