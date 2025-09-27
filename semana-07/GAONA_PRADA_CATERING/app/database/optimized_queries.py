from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

class DomainOptimizedQueries:
    """Consultas optimizadas específicas para el dominio de Catering (Tipo D)"""

    @staticmethod
    def get_optimized_queries_type_d():
        """Consultas optimizadas para Catering (Menús e Inventario)"""
        return {
            'menus_disponibles': """
                -- Consulta optimizada para buscar menús disponibles por stock (ingredientes) y filtros
                SELECT m.nombre, m.descripcion, m.precio,
                       i.stock_actual, prov.nombre as proveedor
                FROM menus m
                -- Asume que 'inventario' es el stock de ingredientes asociados al menú
                JOIN inventario i ON m.id = i.producto_id 
                JOIN proveedores prov ON m.proveedor_id = prov.id
                WHERE i.stock_actual > :stock_minimo -- Por ejemplo, si el stock_actual es la cantidad de menús que se pueden preparar
                AND m.disponible = true
                AND (:buscar IS NULL OR
                     m.nombre ILIKE '%' || :buscar || '%' OR
                     m.descripcion ILIKE '%' || :buscar || '%')
                ORDER BY m.nombre
            """,
            'alertas_stock_bajo': """
                -- Alerta de ingredientes/menús con stock bajo
                SELECT m.nombre, i.stock_actual, i.stock_minimo,
                       (i.stock_actual::float / i.stock_minimo) as ratio_stock
                FROM menus m
                JOIN inventario i ON m.id = i.producto_id
                WHERE i.stock_actual <= i.stock_minimo * 1.2 -- Muestra todo lo que esté cerca del mínimo
                AND m.disponible = true
                ORDER BY ratio_stock ASC
            """
        }

    @staticmethod
    def get_queries_for_domain(domain_type: str):
        """
        Obtiene consultas optimizadas según el tipo de dominio (Catering -> Tipo D)
        """
        if domain_type == "catering_":
            return DomainOptimizedQueries.get_optimized_queries_type_d()
        else:
            # Fallback para otros tipos si existieran
            return {}
