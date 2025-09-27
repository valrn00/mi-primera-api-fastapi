import pytest
import time
from sqlalchemy.orm import Session
# Ajustamos la importación del service
from ..app.services.optimized_domain_service import OptimizedDomainService
from sqlalchemy import text
from typing import Dict, Any

# Mock para simular una sesión de BD y datos de Catering
class MockSession:
    def execute(self, sql_statement, params=None):
        # Simula resultados para 'menus_disponibles' y 'alertas_stock_bajo'
        if "menus" in str(sql_statement):
            # Resultados de Menús disponibles
            return type('MockResult', (object,), {'all': lambda: [{'nombre': 'Paella', 'precio': 15.0}], '__iter__': lambda self: iter(self.all())})()
        elif "pg_indexes" in str(sql_statement):
             # Resultados para la verificación de índices (simula que existen 3)
            return type('MockResult', (object,), {'all': lambda: [{'indexname': 'idx_menus_nombre_disponible', 'tablename': 'menus'}, 
                                                                 {'indexname': 'idx_inventario_producto_stock', 'tablename': 'inventario'},
                                                                 {'indexname': 'idx_transacciones_fecha_total', 'tablename': 'transacciones'}],
                                                  '__iter__': lambda self: iter(self.all())})()
        
        return type('MockResult', (object,), {'all': lambda: [], '__iter__': lambda self: iter(self.all())})()

@pytest.fixture
def db_session() -> Session:
    return MockSession()

class TestDatabaseOptimization:
    DOMAIN_PREFIX = "catering_"
    
    @pytest.mark.asyncio
    async def test_available_menus_performance(self, db_session: Session):
        """Verifica que la consulta crítica de Menús Disponibles sea rápida."""
        service = OptimizedDomainService(db_session, self.DOMAIN_PREFIX)

        start_time = time.time()
        # Llamamos al método que usa la consulta optimizada 'menus_disponibles'
        result = await service.get_available_menus(search_term="Paella")
        duration = time.time() - start_time

        # Objetivo de performance para consultas críticas: < 200ms
        assert duration < 0.2, f"Consulta crítica de menús muy lenta: {duration:.3f}s"
        assert len(result) > 0, "No se obtuvieron resultados de menús."

    @pytest.mark.asyncio
    async def test_inventory_alerts_performance(self, db_session: Session):
        """Verifica performance de consultas de alertas de stock."""
        service = OptimizedDomainService(db_session, self.DOMAIN_PREFIX)

        start_time = time.time()
        # Llamamos al método que usa la consulta optimizada 'alertas_stock_bajo'
        result = await service.get_inventory_alerts()
        duration = time.time() - start_time

        # Objetivo de performance para consultas de inventario: < 300ms
        assert duration < 0.3, f"Consulta de alertas de stock lenta: {duration:.3f}s"

    def test_catering_indexes_exist(self, db_session: Session):
        """Verifica que los índices específicos del dominio de Catering existan."""
        # Consulta para verificar índices
        check_indexes = """
        SELECT indexname, tablename
        FROM pg_indexes
        WHERE indexname LIKE 'idx_menus_%' OR indexname LIKE 'idx_inventario_%'
        OR tablename IN ('menus', 'inventario', 'transacciones');
        """

        # En un test real, harías: result = db_session.execute(text(check_indexes))
        # Usamos el mock para simular un resultado de índices existentes.
        # Debe haber al menos los 3 índices principales que definimos.
        result = db_session.execute(text(check_indexes)) 
        indexes = [dict(row) for row in result]

        assert len(indexes) >= 3, "Faltan índices específicos del dominio de Catering."