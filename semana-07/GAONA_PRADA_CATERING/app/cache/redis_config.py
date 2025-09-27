import redis
import json
from typing import Optional, Any, Dict
import os

# Adaptamos el prefijo al dominio de Catering
CATERING_PREFIX = "catering_"

class DomainCacheConfig:
    """Configuración de cache específica para el dominio de Catering."""
    def __init__(self, domain_prefix: str):
        self.domain_prefix = domain_prefix
        # NOTA: Debes tener un servidor Redis corriendo en localhost:6379 para que esto funcione.
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=True
        )

        # TTL específicos adaptados a datos de Catering
        self.cache_ttl: Dict[str, int] = {
            'popular_menus': 300,       # 5 minutos para menús más solicitados
            'pricing_config': 3600,     # 1 hora para configuraciones de precios estables
            'dietary_references': 86400, # 24 horas para catálogos de dietas (Vegano, Keto, etc.)
            'temp_inventory': 60        # 1 minuto para disponibilidad temporal de stock
        }

    def get_cache_key(self, category: str, identifier: str) -> str:
        """Genera claves de cache con el prefijo 'catering_'."""
        return f"{self.domain_prefix}:{category}:{identifier}"

    def set_cache(self, key: str, value: Any, ttl_type: str = 'popular_menus') -> bool:
        """Almacena datos en cache."""
        try:
            cache_key = self.get_cache_key("data", key)
            serialized_value = json.dumps(value)
            ttl = self.cache_ttl.get(ttl_type, 300)
            return self.redis_client.setex(cache_key, ttl, serialized_value)
        except Exception as e:
            print(f"Error setting cache for {key}: {e}")
            return False

    def get_cache(self, key: str) -> Optional[Any]:
        """Recupera datos del cache."""
        try:
            cache_key = self.get_cache_key("data", key)
            cached_value = self.redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            return None
        except Exception as e:
            print(f"Error getting cache for {key}: {e}")
            return None

    def invalidate_cache(self, pattern: str = None):
        """Invalida cache por patrón o todo el cache del dominio."""
        try:
            if pattern:
                cache_pattern = self.get_cache_key("data", pattern)
                keys = self.redis_client.keys(cache_pattern)
                if keys:
                    self.redis_client.delete(*keys)
            else:
                # Invalida todo el cache de tu dominio
                domain_keys = self.redis_client.keys(f"{self.domain_prefix}:*")
                if domain_keys:
                    self.redis_client.delete(*domain_keys)
        except Exception as e:
            print(f"Error invalidating cache: {e}")

# Instancia específica para tu dominio
cache_manager = DomainCacheConfig(CATERING_PREFIX)