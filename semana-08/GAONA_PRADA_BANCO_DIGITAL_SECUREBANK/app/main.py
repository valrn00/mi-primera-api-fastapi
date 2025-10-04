from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .routers import accounts, transactions, auth
from .docs.descriptions import TAGS_METADATA

# Crear tablas en la base de datos SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SecureBank Digital API",
    description="API para la gestión de cuentas y transacciones en el banco digital SecureBank",
    version="1.0.0",
    contact={
        "name": "Equipo SecureBank",
        "email": "dev@securebank.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=TAGS_METADATA,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Incluir routers
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(auth.router)

def custom_openapi():
    """Personalizar el esquema OpenAPI para incluir metadatos específicos de SecureBank."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=TAGS_METADATA,
        contact=app.contact,
        license_info=app.license_info,
    )
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

@app.get("/health", tags=["system"])
async def health_check(db: Session = Depends(get_db)):
    """Endpoint para verificar el estado de la API."""
    try:
        # Verificar conexión a la base de datos
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}