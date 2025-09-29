# app/cache/cache_decorators.py
from functools import wraps
from .redis_config import cache_manager
import hashlib

def cache_result(ttl_type: str = 'citas_disponibles', key_prefix: str = ""):
    """Decorator para cachear resultados de funciones específicas de tu Clínica Estética"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs): # Asegúrate de que el wrapper sea async si la función decorada lo es
            # Genera clave única basada en función y parámetros
            func_name = func.__name__
            # Incluye todos los args y kwargs en la clave de cache para asegurar unicidad
            args_str = str(args) + str(sorted(kwargs.items()))
            key_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]
            cache_key = f"{key_prefix}:{func_name}:{key_hash}"

            # Intenta obtener del cache
            cached_result = cache_manager.get_cache(cache_key)
            if cached_result is not None:
                return cached_result

            # Si no existe, ejecuta función y guarda resultado
            result = await func(*args, **kwargs) # Asumiendo que las funciones decoradas son async
            cache_manager.set_cache(cache_key, result, ttl_type)
            return result
        return wrapper
    return decorator