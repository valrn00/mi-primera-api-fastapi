# app/database/optimized_queries.py
from typing import Dict, Any

class BeautyOptimizedQueries:
    """Consultas optimizadas para tu Clínica Estética"""

    @staticmethod
    def get_queries_for_domain():
        """Obtiene las consultas optimizadas para el dominio 'beauty_'"""
        return {
            'citas_disponibles': """
                SELECT c.*, t.nombre_tratamiento
                FROM beauty_citas c
                JOIN beauty_tratamientos t ON c.tratamiento_id = t.id
                WHERE c.fecha_cita = :fecha_cita
                AND c.esteticista_id = :esteticista_id
                AND c.estado = 'disponible'
                ORDER BY c.hora_inicio
            """,
            'historial_cliente': """
                SELECT p.fecha_procedimiento, t.nombre_tratamiento, p.observaciones, e.nombre as esteticista_nombre
                FROM beauty_procedimientos p
                JOIN beauty_citas c ON p.cita_id = c.id
                JOIN beauty_tratamientos t ON c.tratamiento_id = t.id
                JOIN beauty_esteticistas e ON c.esteticista_id = e.id
                WHERE p.cliente_id = :cliente_id
                ORDER BY p.fecha_procedimiento DESC
                LIMIT :limit
            """,
            'reporte_ocupacion_esteticista': """
                SELECT e.nombre, COUNT(c.id) as total_citas
                FROM beauty_esteticistas e
                JOIN beauty_citas c ON e.id = c.esteticista_id
                WHERE c.fecha_cita >= :fecha_inicio AND c.fecha_cita <= :fecha_fin
                AND c.estado = 'completada'
                GROUP BY e.nombre
                ORDER BY total_citas DESC
            """
        }