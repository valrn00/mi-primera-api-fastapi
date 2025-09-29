# app/database/indexes.py
from sqlalchemy import Index, text
# Asegúrate de importar tu motor de DB
# from app.database import engine

class BeautyDomainIndexes:
    """Índices específicos para optimizar consultas de tu Clínica Estética"""

    @staticmethod
    def create_beauty_indexes():
        """Índices específicos para Citas, Clientes y Procedimientos"""
        indexes = [
            # Búsquedas de citas por esteticista y fecha (crucial para la app)
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_beauty_citas_esteticista_fecha ON beauty_citas(esteticista_id, fecha_cita);",
            # Búsquedas de citas por estado (canceladas, completadas, etc.)
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_beauty_citas_estado_fecha ON beauty_citas(estado, fecha_cita DESC);",
            # Consultas de historial de cliente por ID
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_beauty_historial_cliente ON beauty_procedimientos(cliente_id, fecha_procedimiento DESC);",
            # Consultas para el catálogo de tratamientos por tipo o categoría
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_beauty_tratamientos_tipo ON beauty_tratamientos(tipo_tratamiento, duracion_minutos);",
        ]
        return indexes

    @staticmethod
    async def create_indexes_for_domain():
        """Crea índices específicos para tu dominio de Clínica Estética"""
        indexes = BeautyDomainIndexes.create_beauty_indexes()

        # Asume que 'engine' es tu motor de base de datos SQLAlchemy
        # with engine.connect() as connection:
        #     for index_sql in indexes:
        #         try:
        #             connection.execute(text(index_sql))
        #             print(f"✅ Índice creado: {index_sql[:50]}...")
        #         except Exception as e:
        #             print(f"❌ Error creando índice: {e}")
        print("Ejecuta manualmente los scripts SQL para crear los índices en tu base de datos.")