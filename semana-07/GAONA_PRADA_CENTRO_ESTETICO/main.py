from fastapi import FastAPI, Request, Response
from prometheus_fastapi_instrumentator import Instrumentator
from monitoring.metrics import APIMetrics, monitor_performance
from monitoring.profiler import APIProfiler
from monitoring.alerts import AlertManager, AlertRule, email_alert
import asyncio
import time

# Configuración según tu dominio asignado
DOMAIN_CONFIG = {
    "app_name": "beauty_clinic_api",
    "domain": "beauty_",
    "entity": "cita"
}

app = FastAPI(title=f"API {DOMAIN_CONFIG['entity']}")

# Inicializar sistemas de monitoring
metrics = APIMetrics(
    app_name=DOMAIN_CONFIG["app_name"],
    domain=DOMAIN_CONFIG["domain"]
)

profiler = APIProfiler(domain=DOMAIN_CONFIG["domain"])

alert_manager = AlertManager(domain=DOMAIN_CONFIG["domain"])

# Configurar Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Configurar alertas específicas del dominio
alert_manager.add_rule(AlertRule(
    name=f"{DOMAIN_CONFIG['domain']}_high_response_time",
    metric_name="response_time",
    threshold=2.0,  # 2 segundos
    comparison="gt",
    duration=60,    # 1 minuto
    action=email_alert
))

alert_manager.add_rule(AlertRule(
    name=f"{DOMAIN_CONFIG['domain']}_high_cpu",
    metric_name="cpu_usage",
    threshold=80.0,  # 80%
    comparison="gt",
    duration=120,    # 2 minutos
    action=email_alert
))

# Middleware para métricas automáticas
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    metrics.record_request(
        method=request.method,
        endpoint=str(request.url.path),
        status=response.status_code,
        duration=duration
    )

    return response

# Tarea en background para métricas del sistema
@asyncio.create_task
async def update_system_metrics():
    while True:
        metrics.update_system_metrics()
        await asyncio.sleep(30)  # Cada 30 segundos

# Endpoint para métricas personalizadas
@app.get("/metrics-dashboard")
async def get_metrics_dashboard():
    """Endpoint para obtener métricas del dashboard"""
    return {
        "domain": DOMAIN_CONFIG["domain"],
        "entity": DOMAIN_CONFIG["entity"],
        "profiles": profiler.get_profile_report(),
        "system_status": "healthy"
    }

# Ejemplo de uso en endpoints existentes
@app.post(f"/{DOMAIN_CONFIG['domain']}{DOMAIN_CONFIG['entity']}/")
@profiler.profile_function(f"create_{DOMAIN_CONFIG['entity']}")
@monitor_performance(metrics)
async def create_entity(entity_data: dict):
    """Crear nueva entidad con monitoring"""

    # Tu lógica existente aquí
    # ...

    # Registrar evento de negocio
    metrics.record_business_event('citas_creadas')

    return {"message": f"{DOMAIN_CONFIG['entity']} creado exitosamente"}