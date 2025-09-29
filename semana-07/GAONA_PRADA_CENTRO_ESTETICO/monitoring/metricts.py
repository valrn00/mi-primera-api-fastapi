from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge, Info
import psutil
import time
from functools import wraps

class APIMetrics:
    def __init__(self, app_name: str, domain: str):
        self.app_name = app_name
        self.domain = domain

        # Métricas personalizadas por dominio 'beauty_'
        self.request_counter = Counter(
            f'{domain}_requests_total',
            'Total de requests por endpoint',
            ['method', 'endpoint', 'status']
        )

        self.response_time = Histogram(
            f'{domain}_response_duration_seconds',
            'Tiempo de respuesta por endpoint',
            ['method', 'endpoint'],
            buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        )

        self.active_connections = Gauge(
            f'{domain}_active_connections',
            'Conexiones activas'
        )

        self.system_metrics = {
            'cpu_usage': Gauge(f'{domain}_cpu_usage_percent', 'Uso de CPU'),
            'memory_usage': Gauge(f'{domain}_memory_usage_bytes', 'Uso de memoria'),
            'disk_usage': Gauge(f'{domain}_disk_usage_percent', 'Uso de disco')
        }

        # Métricas específicas del dominio 'beauty_'
        self.business_metrics = self._create_business_metrics()

    def _create_business_metrics(self):
        """Crea métricas específicas para el dominio de Clínica Estética"""
        return {
            'citas_creadas': Counter(
                f'{self.domain}_citas_creadas_total',
                'Total de citas creadas'
            ),
            'procedimientos_registrados': Counter(
                f'{self.domain}_procedimientos_registrados_total',
                'Total de procedimientos registrados',
                ['tipo_procedimiento']
            ),
            'api_errors': Counter(
                f'{self.domain}_api_errors_total',
                'Total de errores de API',
                ['error_type', 'endpoint']
            )
        }

    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """Registra métricas de request"""
        self.request_counter.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()

        self.response_time.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    def update_system_metrics(self):
        """Actualiza métricas del sistema"""
        self.system_metrics['cpu_usage'].set(psutil.cpu_percent())
        self.system_metrics['memory_usage'].set(psutil.virtual_memory().used)
        self.system_metrics['disk_usage'].set(psutil.disk_usage('/').percent)

    def record_business_event(self, event_type: str, **kwargs):
        """Registra eventos de negocio específicos del dominio"""
        if event_type in self.business_metrics:
            if hasattr(self.business_metrics[event_type], 'labels'):
                self.business_metrics[event_type].labels(**kwargs).inc()
            else:
                self.business_metrics[event_type].inc()

# Decorador para métricas automáticas
def monitor_performance(metrics: APIMetrics):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time

                # Registrar métricas de éxito
                metrics.record_request(
                    method="POST",
                    endpoint=func.__name__,
                    status=200,
                    duration=duration
                )
                return result
            except Exception as e:
                duration = time.time() - start_time

                # Registrar métricas de error
                metrics.record_request(
                    method="POST",
                    endpoint=func.__name__,
                    status=500,
                    duration=duration
                )

                metrics.record_business_event(
                    'api_errors',
                    error_type=type(e).__name__,
                    endpoint=func.__name__
                )
                raise
        return wrapper
    return decorator