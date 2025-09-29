# app/cache/redis_config.py
import redis
import json
from typing import Optional, Any
import os

class DomainCacheConfig:
    def __init__(self, domain_prefix: str):
        self.domain_prefix = domain_prefix  # Tu prefijo específico: beauty_
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=True
        )

        # TTL específicos para los datos de Clínica Estética
        self.cache_ttl = {
            'citas_disponibles': 120,   # 2 minutos para disponibilidad de citas (cambia rápidamente)
            'detalle_tratamiento': 600, # 10 minutos para detalles de tratamientos (estables, pero pueden actualizarse)
            'catalogo_servicios': 3600, # 1 hora para el catálogo general de servicios/tratamientos
            'configuracion_clinica': 86400, # 24 horas para configuraciones de la clínica
            'historial_cliente': 300, # 5 minutos para historial de tratamientos de un cliente (se consulta frecuentemente, pero puede crecer)
            'promociones_activas': 300 # 5 minutos para promociones (cambian, pero no tan rápido como las citas)
        }

    def get_cache_key(self, category: str, identifier: str) -> str:
        """Genera claves de cache específicas para tu dominio de Clínica Estética"""
        return f"{self.domain_prefix}:{category}:{identifier}"

    def set_cache(self, key: str, value: Any, ttl_type: str = 'citas_disponibles') -> bool:
        """Almacena datos en cache con TTL específico"""
        try:
            cache_key = self.get_cache_key("data", key)
            serialized_value = json.dumps(value)
            ttl = self.cache_ttl.get(ttl_type, 300) # Valor por defecto si no se encuentra el tipo
            return self.redis_client.setex(cache_key, ttl, serialized_value)
        except Exception as e:
            print(f"Error setting cache for key '{key}': {e}")
            return False

    def get_cache(self, key: str) -> Optional[Any]:
        """Recupera datos del cache"""
        try:
            cache_key = self.get_cache_key("data", key)
            cached_value = self.redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            return None
        except Exception as e:
            print(f"Error getting cache for key '{key}': {e}")
            return None

    def invalidate_cache(self, pattern: str = None):
        """Invalida cache específico o por patrón para Clínica Estética"""
        try:
            if pattern:
                # Buscamos claves que coincidan con el patrón bajo nuestro prefijo de dominio
                cache_pattern = f"{self.domain_prefix}:{pattern}"
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

# Instancia específica para tu dominio de Clínica Estética
cache_manager = DomainCacheConfig("beauty_")