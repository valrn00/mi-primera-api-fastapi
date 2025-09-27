import pytest
from app.cache.redis_config import cache_manager, CATERING_PREFIX

# Se asume que Redis está corriendo y accesible para estos tests

@pytest.fixture(autouse=True)
def cleanup_redis():
    """Fixture para limpiar el cache de catering antes y después de cada test."""
    cache_manager.invalidate_cache()
    yield
    cache_manager.invalidate_cache()

class TestCateringCache:

    def test_cache_key_prefix_is_correct(self):
        """Verifica que el prefijo del dominio 'catering_' se aplique correctamente."""
        key = cache_manager.get_cache_key("data", "test_menu")
        assert key.startswith(CATERING_PREFIX)
        assert "catering_:data:test_menu" == key

    def test_cache_set_and_get_popular_menus(self):
        """Verifica que los menús populares se puedan guardar y recuperar."""
        test_key = "popular_list_hash"
        test_data = [{"name": "Menu A", "price": 10.0}]

        # Almacena en cache (usa el TTL 'popular_menus' por defecto)
        assert cache_manager.set_cache(test_key, test_data)

        # Recupera del cache
        cached_data = cache_manager.get_cache(test_key)
        assert cached_data == test_data

    def test_cache_ttl_pricing_config(self):
        """Verifica que se use el TTL específico para la configuración de precios."""
        test_key = "pricing_rules"
        test_data = {"iva": 0.16}
        
        # Almacena con TTL 'pricing_config' (3600 segundos)
        cache_manager.set_cache(test_key, test_data, 'pricing_config')
        
        # Verifica la existencia y el TTL (puede variar ligeramente)
        redis_key = cache_manager.get_cache_key("data", test_key)
        ttl = cache_manager.redis_client.ttl(redis_key)
        
        # El TTL debe estar cerca de 3600, verificamos que esté entre 3500 y 3600
        assert 3500 < ttl <= 3600

    def test_cache_invalidation_by_pattern(self):
        """Verifica que se puedan invalidar caches por patrón específico de menú."""
        cache_manager.set_cache("menu_details:5", {"name": "Menu 5"})
        cache_manager.set_cache("menu_details:6", {"name": "Menu 6"})
        
        # Invalida solo el menu 5
        cache_manager.invalidate_cache("*details:5")
        
        # El menu 5 debe ser MISS
        assert cache_manager.get_cache("menu_details:5") is None
        
        # El menu 6 debe ser HIT
        assert cache_manager.get_cache("menu_details:6") is not None
