import time
from sqlalchemy import text
from sqlalchemy.orm import Session
from contextlib import contextmanager
from typing import List, Dict, Any

class DatabasePerformanceMonitor:

    @staticmethod
    @contextmanager
    def measure_query_time(query_name: str):
        """Context manager para medir tiempo de consultas"""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            print(f"Query '{query_name}' ejecutada en {duration:.3f}s")

            # Log si es lenta (threshold para consultas críticas de Catering)
            if duration > 0.2:  # 200ms
                print(f"⚠️  Consulta lenta de Catering detectada: {query_name}")

    @staticmethod
    def get_database_stats(db: Session) -> List[Dict[str, Any]]:
        """Obtiene estadísticas generales de la base de datos (PostgreSQL ejemplo)"""
        stats_query = """
        SELECT
            schemaname, tablename, attname, n_distinct, correlation
        FROM pg_stats
        WHERE schemaname = 'public'
        ORDER BY tablename, attname;
        """
        try:
            result = db.execute(text(stats_query))
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return []

    @staticmethod
    def analyze_slow_queries(db: Session, domain_prefix: str) -> List[Dict[str, Any]]:
        """Analiza consultas lentas específicas del dominio (requiere pg_stat_statements)"""
        # Personalizamos la búsqueda para tablas principales de Catering (menus, inventario)
        slow_queries = """
        SELECT query, calls, total_time, mean_time
        FROM pg_stat_statements
        WHERE query LIKE '%menus%' OR query LIKE '%inventario%' 
        ORDER BY mean_time DESC
        LIMIT 10;
        """
        try:
            result = db.execute(text(slow_queries))
            return [dict(row) for row in result]
        except Exception as e:
            print(f"Error analizando consultas lentas (instala pg_stat_statements): {e}")
            return []
