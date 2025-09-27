from .redis_config import cache_manager
import hashlib
from typing import Any

def cache_result(ttl_type: str = 'popular_menus', key_prefix: str = "general"):
    """
    Decorator para cachear resultados de funciones.
    Usa 'ttl_type' específico del dominio de Catering (e.g., 'popular_menus', 'pricing_config').
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Genera clave única basada en función y argumentos
            func_name = func.__name__
            # Excluir el primer argumento (típicamente 'self' o la conexión DB) para el hash,
            # ya que solo necesitamos los parámetros de la consulta.
            args_to_hash = args[1:] if args and func_name.startswith('get_') else args
            args_str = str(args_to_hash) + str(sorted(kwargs.items()))
            key_hash = hashlib.md5(args_str.encode()).hexdigest()[:12]
            
            # Clave de cache personalizada para Catering
            cache_key = f"{key_prefix}:{func_name}:{key_hash}"

            # Intenta obtener del cache
            cached_result = cache_manager.get_cache(cache_key)
            if cached_result is not None:
                # print(f"Cache HIT: {cache_key}") # Descomentar para debug
                return cached_result

            # print(f"Cache MISS: {cache_key}") # Descomentar para debug
            # Si no existe, ejecuta función y guarda resultado
            result = func(*args, **kwargs)
            cache_manager.set_cache(cache_key, result, ttl_type)
            return result
        return wrapper
    return decorator
