# app/middleware/domain_logger.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import json
import time
from typing import Dict, Any

class DomainLogger(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str):
        super().__init__(app)
        self.domain_prefix = domain_prefix

        # Configurar logger específico para el dominio
        self.logger = logging.getLogger(f"{domain_prefix}domain_logger")
        self.logger.setLevel(logging.INFO)

        # Handler específico para archivos del dominio
        handler = logging.FileHandler(f"logs/{domain_prefix}domain.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Configurar qué endpoints loggear por dominio
        self.logged_endpoints = self._get_logged_endpoints(domain_prefix)

    def _get_logged_endpoints(self, domain_prefix: str) -> Dict[str, str]:
        """Define qué endpoints requieren logging específico para 'beauty_'"""

        logging_configs = {
            "beauty_": {
                "/procedimientos/create": "WARNING", # Creación de nuevos procedimientos
                "/procedimientos/update": "WARNING", # Modificación de procedimientos
                "/historial": "INFO",                # Acceso a historial de cliente
                "/citas/book": "INFO",               # Creación de citas
                "/precios": "CRITICAL"               # Acceso a datos sensibles
            }
        }
        return logging_configs.get(domain_prefix, {})

    def _should_log_endpoint(self, path: str) -> tuple[bool, str]:
        """Determina si el endpoint debe ser loggeado y su nivel"""
        for endpoint_pattern, level in self.logged_endpoints.items():
            if endpoint_pattern in path:
                return True, level
        return False, "INFO"

    def _extract_domain_specific_data(self, request: Request, path: str) -> Dict[str, Any]:
        """Extrae datos específicos del dominio para logging"""
        data = {
            "domain": self.domain_prefix,
            "path": path,
            "method": request.method,
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent", "unknown")
        }

        # Para Clínica Estética, loggear IDs de cliente, esteticista y tratamiento
        if "cliente_id" in str(request.url):
            data["entity_type"] = "cliente"
        elif "esteticista_id" in str(request.url):
            data["entity_type"] = "esteticista"
        elif "tratamiento_id" in str(request.url):
            data["entity_type"] = "tratamiento"

        return data

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url.path

        # Solo procesar endpoints del dominio
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        # Verificar si debe ser loggeado
        should_log, log_level = self._should_log_endpoint(path)

        if should_log:
            request_data = self._extract_domain_specific_data(request, path)
            self.logger.log(
                getattr(logging, log_level),
                f"REQUEST_START: {json.dumps(request_data)}"
            )

        response = await call_next(request)

        if should_log:
            process_time = time.time() - start_time
            response_data = {
                **request_data,
                "status_code": response.status_code,
                "process_time": round(process_time, 3)
            }

            if response.status_code >= 500:
                response_level = "CRITICAL"
            elif response.status_code >= 400:
                response_level = "WARNING"
            else:
                response_level = log_level

            self.logger.log(
                getattr(logging, response_level),
                f"REQUEST_END: {json.dumps(response_data)}"
            )

        return response