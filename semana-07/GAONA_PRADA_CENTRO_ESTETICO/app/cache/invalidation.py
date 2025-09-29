# app/cache/invalidation.py
from .redis_config import cache_manager

class DomainCacheInvalidation:

    @staticmethod
    async def on_tratamiento_update(tratamiento_id: str):
        """Invalida cache cuando se actualiza un tratamiento de la Clínica Estética"""
        # Invalida detalles del tratamiento específico
        cache_manager.invalidate_cache(f"data:tratamientos_:{tratamiento_id}*")
        # Invalida el catálogo completo, ya que puede haber cambiado
        cache_manager.invalidate_cache(f"data:catalogo_:general*") # O el patrón específico de tu catálogo
        print(f"Invalidando cache de tratamiento {tratamiento_id} y catálogo.")

    @staticmethod
    async def on_cita_change(cita_id: str, client_id: Optional[str] = None):
        """Invalida cache cuando se crea, actualiza o cancela una cita."""
        # Invalida la disponibilidad general de citas
        cache_manager.invalidate_cache(f"data:citas_:disponibilidad_general*") # O un patrón más específico de fechas
        # Si la cita afecta a un cliente, invalida su historial
        if client_id:
            cache_manager.invalidate_cache(f"data:cliente:{client_id}:historial*")
        print(f"Invalidando cache de citas para {cita_id} y, opcionalmente, historial de cliente {client_id}.")

    @staticmethod
    async def on_clinica_config_change():
        """Invalida cache de configuración general de la Clínica Estética"""
        cache_manager.invalidate_cache(f"data:clinica_:configuracion_clinica*")
        print("Invalidando cache de configuración de la clínica.")

# Ejemplo de uso en endpoints de actualización (asumiendo que los routers importan estos)
# Este código debería ir en tu router de tratamientos o citas, no directamente aquí.
# Ejemplo conceptual:
"""
# app/routers/beauty_routers.py
from fastapi import APIRouter, Depends, HTTPException
# ... otras importaciones
from app.cache.invalidation import DomainCacheInvalidation
# ...

@router.put("/beauty_tratamientos/{tratamiento_id}")
async def update_tratamiento(tratamiento_id: int, data: dict, db: Session = Depends(get_db)):
    # Lógica para actualizar el tratamiento en la BD
    # await beauty_service.update_tratamiento(tratamiento_id, data)
    await DomainCacheInvalidation.on_tratamiento_update(str(tratamiento_id)) # Importante convertir a str si el ID es int
    return {"message": f"Tratamiento {tratamiento_id} actualizado y cache invalidado."}

@router.post("/beauty_citas/")
async def create_cita(data: dict, db: Session = Depends(get_db)):
    # Lógica para crear la cita en la BD
    # new_cita = await beauty_service.create_cita(data)
    # await DomainCacheInvalidation.on_cita_change(str(new_cita.id), str(new_cita.client_id))
    return {"message": "Cita creada y cache invalidado."}
"""