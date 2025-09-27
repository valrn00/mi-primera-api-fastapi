from typing import List, Dict
from ..cache.cache_decorators import cache_result

router = APIRouter(prefix="/catering", tags=["Catering Optimizado"])

# --- Simulación de Servicio de Menús ---
# En una aplicación real, esto interactuaría con la base de datos (DB).
class MenuService:
    @staticmethod
    def get_popular_menus() -> List[Dict]:
        """Simula una consulta lenta de menús populares."""
        # En un escenario real, esto sería una consulta compleja con JOINs y ORDER BY count
        import time
        time.sleep(0.5) # Simula latencia de 500ms
        
        return [
            {"id": 1, "name": "Menú Gourmet de Bodas", "price": 95.00, "popularity": 98},
            {"id": 2, "name": "Menú Ejecutivo Vegano", "price": 45.00, "popularity": 85},
            {"id": 3, "name": "Menú Infantil Temático", "price": 20.00, "popularity": 70},
        ]
        
    @staticmethod
    def get_pricing_configuration() -> Dict:
        """Simula una consulta de datos de configuración estables."""
        return {
            "iva_rate": 0.16,
            "service_charge": 0.05,
            "min_guests_discount": 50
        }

# --- Endpoints Optimizados con Caching ---

@router.get("/menus/populares", response_model=List[Dict])
@cache_result(ttl_type='popular_menus', key_prefix='menu_list')
def get_menus_frecuentes_cached():
    """
    Optimización: Obtiene los menús más populares. Cacha por 5 minutos.
    Si se consulta 100 veces en 5 minutos, solo golpea la DB una vez.
    """
    return MenuService.get_popular_menus()

@router.get("/configuracion/precios", response_model=Dict)
@cache_result(ttl_type='pricing_config', key_prefix='config')
def get_configuracion_precios_cached():
    """
    Optimización: Obtiene la configuración de precios. Cacha por 1 hora.
    Datos estables que no cambian a menudo.
    """
    return MenuService.get_pricing_configuration()
