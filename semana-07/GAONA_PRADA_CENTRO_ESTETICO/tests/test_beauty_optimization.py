# tests/test_beauty_optimization.py
import pytest
import time
from sqlalchemy.orm import Session
from app.services.beauty_service import OptimizedBeautyService
# Suponiendo que tienes un fixture para la sesión de DB
# from tests.conftest import db_session

class TestBeautyDatabaseOptimization:

    @pytest.mark.asyncio
    def test_citas_disponibles_performance(self, db_session: Session):
        """Verifica que la consulta de citas disponibles sea rápida."""
        service = OptimizedBeautyService(db_session)
        
        # Simular una fecha y esteticista (asegúrate de que existan en tus datos de test)
        fecha_test = "2025-01-10"
        esteticista_test_id = 1

        start_time = time.time()
        citas = service.get_citas_disponibles(fecha_test, esteticista_test_id)
        duration = time.time() - start_time

        assert duration < 0.1, f"Consulta de citas disponibles muy lenta: {duration:.3f}s"
        assert isinstance(citas, list)

    @pytest.mark.asyncio
    def test_historial_cliente_performance(self, db_session: Session):
        """Verifica el performance de la consulta del historial de un cliente."""
        service = OptimizedBeautyService(db_session)

        # Simular un cliente que existe y tiene historial
        cliente_test_id = 5
        
        start_time = time.time()
        historial = service.get_historial_cliente(cliente_test_id, limit=20)
        duration = time.time() - start_time

        assert duration < 0.2, f"Consulta de historial de cliente muy lenta: {duration:.3f}s"
        assert isinstance(historial, list)
        
    @pytest.mark.asyncio
    def test_reporte_ocupacion_performance(self, db_session: Session):
        """Verifica el performance de la consulta del reporte de ocupación."""
        service = OptimizedBeautyService(db_session)
        
        # Simular un rango de fechas con datos
        fecha_inicio = "2025-01-01"
        fecha_fin = "2025-01-31"

        start_time = time.time()
        reporte = service.get_reporte_ocupacion(fecha_inicio, fecha_fin)
        duration = time.time() - start_time
        
        assert duration < 0.5, f"Consulta de reporte de ocupación muy lenta: {duration:.3f}s"
        assert isinstance(reporte, list)