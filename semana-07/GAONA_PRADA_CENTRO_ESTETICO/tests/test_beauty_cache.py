# tests/test_beauty_cache.py
import pytest
from app.cache.redis_config import cache_manager, DomainCacheConfig
from app.cache.cache_decorators import cache_result
from unittest.mock import AsyncMock, patch

# Mock del cliente Redis para evitar conexiones reales durante los tests
@pytest.fixture(autouse=True)
def mock_redis_client():
    with patch('redis.Redis') as mock_redis:
        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.get.return_value = None
        mock_redis_instance.setex.return_value = True
        mock_redis_instance.keys.return_value = []
        mock_redis_instance.delete.return_value = 0
        yield

class TestBeautyCache:

    # Re-inicializar cache_manager para cada test con el mock
    @pytest.fixture(autouse=True)
    def setup_cache_manager(self):
        global cache_manager
        cache_manager = DomainCacheConfig("beauty_")
        yield

    def test_cache_basic_functionality_beauty(self, mock_redis_client):
        """Verifica funcionalidad básica del cache para Clínica Estética."""
        test_key = "test_tratamiento_101"
        test_data = {"id": 101, "nombre": "Peeling Químico", "precio": 120.00}

        # Almacena en cache
        assert cache_manager.set_cache(test_key, test_data, 'detalle_tratamiento')
        mock_redis_client.get.return_value = json.dumps(test_data) # Simular que se guarda

        # Recupera del cache
        cached_data = cache_manager.get_cache(test_key)
        assert cached_data == test_data
        
        # Verifica que se llamó a setex con el TTL correcto
        expected_ttl = cache_manager.cache_ttl['detalle_tratamiento']
        mock_redis_client.setex.assert_called_with(f"beauty_:data:{test_key}", expected_ttl, json.dumps(test_data))

        # Limpia
        cache_manager.invalidate_cache("data:test_tratamiento_101")
        mock_redis_client.delete.assert_called_with(f"beauty_:data:test_tratamiento_101")


    @pytest.mark.asyncio
    async def test_cache_decorator_beauty(self, mock_redis_client):
        """Verifica que el decorador de cache funciona para un endpoint de Clínica Estética."""
        
        @cache_result(ttl_type='citas_disponibles', key_prefix='citas_')
        async def mock_get_citas_disponibles_db(fecha: str):
            # Simula una llamada a la base de datos
            return [{"fecha": fecha, "hora": "10:00", "tratamiento": "Facial"}]

        fecha_test = "2025-10-15"
        
        # Primera llamada (miss de cache)
        result1 = await mock_get_citas_disponibles_db(fecha=fecha_test)
        assert result1 == [{"fecha": fecha_test, "hora": "10:00", "tratamiento": "Facial"}]
        # Verifica que la función original se ejecutó y se intentó guardar en cache
        mock_redis_client.setex.assert_called_once()
        mock_redis_client.get.assert_called_once()

        # Simula que el resultado ya está en cache para la segunda llamada
        mock_redis_client.get.return_value = json.dumps([{"fecha": fecha_test, "hora": "10:00", "tratamiento": "Facial"}])
        
        # Segunda llamada (hit de cache)
        result2 = await mock_get_citas_disponibles_db(fecha=fecha_test)
        assert result2 == [{"fecha": fecha_test, "hora": "10:00", "tratamiento": "Facial"}]
        # Verifica que la función original NO se ejecutó de nuevo (solo se llamó a get)
        assert mock_redis_client.get.call_count == 2 # Una vez por la primera, otra por esta
        assert mock_redis_client.setex.call_count == 1 # Solo se guardó una vez

    def test_cache_invalidation_tratamiento(self, mock_redis_client):
        """Verifica la invalidación de cache para un tratamiento actualizado."""
        from app.cache.invalidation import DomainCacheInvalidation

        tratamiento_id = "10"
        # Simular que hay datos en cache que deberían ser invalidados
        mock_redis_client.keys.side_effect = [
            [f"beauty_:data:tratamientos_:{tratamiento_id}:hash123"],
            [f"beauty_:data:catalogo_:general:hashABC"]
        ]

        # Llamar a la función de invalidación
        DomainCacheInvalidation.on_tratamiento_update(tratamiento_id)

        # Verificar que se intentó borrar la clave específica del tratamiento
        mock_redis_client.delete.assert_any_call(f"beauty_:data:tratamientos_:{tratamiento_id}:hash123")
        # Verificar que también se intentó borrar el caché del catálogo
        mock_redis_client.delete.assert_any_call(f"beauty_:data:catalogo_:general:hashABC")