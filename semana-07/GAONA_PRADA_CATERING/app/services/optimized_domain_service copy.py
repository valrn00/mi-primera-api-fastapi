from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

# Ajustamos las importaciones (asumiendo que están en el mismo nivel o superior)
from ..services.optimized_domain_service import OptimizedDomainService

# Mock para la función get_db, debe ser reemplazada por tu implementación real
def get_db():
    # Esto es un mock para que el código compile, debe ser la función real de tu BD
    class MockDB:
        def execute(self, *args, **kwargs):
            return []
    yield MockDB()

router = APIRouter(prefix="/catering/optimized", tags=["Optimized Catering"])

@router.get("/menus-disponibles", response_model=List[Dict[str, Any]])
async def get_available_menus_optimized(
    search: Optional[str] = Query(None, description="Término de búsqueda para nombre o descripción del menú"),
    min_stock: int = Query(1, description="Stock mínimo requerido para el ingrediente/menú principal"),
    db: Session = Depends(get_db)
):
    """
    Endpoint optimizado para consultas de menús disponibles. 
    Utiliza el índice compuesto para nombre/descripción/disponibilidad.
    """
    try:
        service = OptimizedDomainService(db, "catering_")
        return await service.get_available_menus(search_term=search, stock_min=min_stock)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en la consulta optimizada de menús.")

@router.get("/stock-alerts", response_model=List[Dict[str, Any]])
async def get_stock_alerts_optimized(db: Session = Depends(get_db)):
    """
    Endpoint optimizado para obtener alertas de stock bajo de ingredientes/menús.
    """
    try:
        service = OptimizedDomainService(db, "catering_")
        return await service.get_inventory_alerts()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en la consulta optimizada de alertas.")
