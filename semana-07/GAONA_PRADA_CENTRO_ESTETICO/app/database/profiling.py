# app/database/profiling.py
import time
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Configurar logging para consultas lentas
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sql_performance")

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    if total > 0.1:  # Log consultas que toman más de 100ms
        logger.warning(f"Consulta lenta ({total:.3f}s): {statement[:100]}...")

# Función para analizar consultas específicas de tu dominio
def analyze_domain_queries(domain_prefix: str):
    """
    Analiza las consultas específicas de tu Clínica Estética
    """
    if domain_prefix == "beauty_":
        test_queries = [
            "Búsqueda de citas disponibles por fecha y esteticista",
            "Consulta del historial completo de un cliente",
            "Reporte de ocupación de esteticistas por mes"
        ]
        print(f"Analizando consultas críticas para el dominio '{domain_prefix}':")
        for q in test_queries:
            print(f"- {q}")
        print("\nEjecuta tus endpoints para ver el profiling de las consultas.")
    else:
        print("Dominio no reconocido. Por favor, usa 'beauty_'.")