from .redis_config import cache_manager, CATERING_PREFIX

class CateringCacheInvalidation:

    @staticmethod
    async def on_menu_update(menu_id: int):
        """
        Invalida cache cuando se actualiza un Menú específico.
        Estrategia específica de Catering:
        1. Invalida el menú individual (si estuviera cacheado).
        2. Invalida la lista general de menús populares, forzando una regeneración.
        """
        
        # 1. Invalida cache de la clave individual del Menú (si existe)
        cache_manager.invalidate_cache(f"menu_details:{menu_id}")

        # 2. Invalida la lista general de menús populares, ya que un cambio de precio 
        #    o disponibilidad en un menú afecta la lista.
        cache_manager.invalidate_cache("*menu_list*")
        
        print(f"Cache invalidado para Menú ID: {menu_id} y listas populares.")

    @staticmethod
    async def on_pricing_configuration_change():
        """Invalida cache de configuración de precios."""
        cache_manager.invalidate_cache("*config*")

# --- EJEMPLO DE USO EN UN ROUTER DE ACTUALIZACIÓN ---
# from fastapi import APIRouter
# update_router = APIRouter(prefix="/cateringmenus", tags=["Menus CRUD"])

# @update_router.put("/{menu_id}")
# async def update_menu(menu_id: int, data: dict):
#     # Lógica para actualizar el menú en la DB
#     # ...
#     
#     # Invalida caches relacionados
#     await CateringCacheInvalidation.on_menu_update(menu_id)
#     return {"message": "Menú actualizado y cache invalidado"}