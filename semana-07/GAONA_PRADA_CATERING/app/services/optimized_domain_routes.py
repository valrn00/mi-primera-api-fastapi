from sqlalchemy.orm import Session
from sqlalchemy import text
# Importamos de la ruta relativa correcta (adaptamos la ruta de importación)
from ..database.optimized_queries import DomainOptimizedQueries 
from typing import List, Dict, Any, Optional

class OptimizedDomainService:
    def __init__(self, db: Session, domain_prefix: str):
        self.db = db
        self.domain_prefix = domain_prefix
        # Usamos el prefijo 'catering_' para obtener las queries
        self.queries = DomainOptimizedQueries.get_queries_for_domain(domain_prefix)

    async def execute_optimized_query(self, query_name: str, params: Dict[str, Any]) -> List[Dict]:
        """Ejecuta consulta optimizada específica del dominio"""
        if query_name not in self.queries:
            raise ValueError(f"Query {query_name} no encontrada para dominio {self.domain_prefix}")

        query = self.queries[query_name]
        # NOTA: En un entorno asíncrono real, usarías db.execute de forma asíncrona.
        result = self.db.execute(text(query), params) 
        return [dict(row) for row in result]

    async def get_available_menus(self, search_term: Optional[str] = None, stock_min: int = 1) -> List[Dict]:
        """Obtiene menús disponibles basado en stock y búsqueda rápida (Tipo D: 'menus_disponibles')"""
        if self.domain_prefix == "catering_":
            params = {
                "buscar": search_term, 
                "stock_minimo": stock_min
            }
            return await self.execute_optimized_query("menus_disponibles", params)
        return []

    async def get_inventory_alerts(self) -> List[Dict]:
        """Obtiene alertas de stock bajo para ingredientes/menús (Tipo D: 'alertas_stock_bajo')"""
        if self.domain_prefix == "catering_":
            return await self.execute_optimized_query("alertas_stock_bajo", {})
        return []

    # Se mantiene la función genérica, pero se ajusta el nombre para reflejar mejor el catering
    async def get_critical_data(self, entity_id: int, **filters) -> List[Dict]:
        """Obtiene datos críticos específicos (ej. historial de pedidos de un cliente o ingredientes de un menú)"""
        # Por simplicidad, esta función se deja como ejemplo
        return await self.get_available_menus(stock_min=0)