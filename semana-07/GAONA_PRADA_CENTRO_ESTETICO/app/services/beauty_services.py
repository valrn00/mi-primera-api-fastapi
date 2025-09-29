# app/services/beauty_service.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any, Optional
from ..database.optimized_queries import BeautyOptimizedQueries

class OptimizedBeautyService:
    def __init__(self, db: Session):
        self.db = db
        self.queries = BeautyOptimizedQueries.get_queries_for_domain()

    def get_citas_disponibles(self, fecha: str, esteticista_id: int) -> List[Dict]:
        """Obtiene citas disponibles de manera optimizada."""
        query = self.queries['citas_disponibles']
        params = {"fecha_cita": fecha, "esteticista_id": esteticista_id}
        result = self.db.execute(text(query), params)
        return [dict(row) for row in result]

    def get_historial_cliente(self, cliente_id: int, limit: int = 10) -> List[Dict]:
        """Obtiene el historial de tratamientos de un cliente de manera optimizada."""
        query = self.queries['historial_cliente']
        params = {"cliente_id": cliente_id, "limit": limit}
        result = self.db.execute(text(query), params)
        return [dict(row) for row in result]

    def get_reporte_ocupacion(self, fecha_inicio: str, fecha_fin: str) -> List[Dict]:
        """Genera un reporte de ocupación de esteticistas de manera optimizada."""
        query = self.queries['reporte_ocupacion_esteticista']
        params = {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin}
        result = self.db.execute(text(query), params)
        return [dict(row) for row in result]