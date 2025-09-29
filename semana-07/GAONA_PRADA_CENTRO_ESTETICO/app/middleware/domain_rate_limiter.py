# app/middleware/domain_rate_limiter.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import time
import json
from typing import Dict, Optional

class DomainRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str, redis_client: redis.Redis):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.redis = redis_client

        # Configuración específica por dominio
        self.rate_limits = self._get_domain_rate_limits(domain_prefix)

    def _get_domain_rate_limits(self, domain_prefix: str) -> Dict[str, Dict]:
        """Configuración de límites específicos para tu dominio 'beauty_'"""

        rate_configs = {
            "beauty_": {
                # Límites altos para disponibilidad
                "availability": {"requests": 400, "window": 60},  # 400 req/min disponibilidad
                # Límites medios para reservas y historial
                "booking": {"requests": 100, "window": 60},      # 100 req/min reservas de citas
                "history": {"requests": 150, "window": 60},      # 150 req/min historial
                # Límites bajos para admin
                "admin": {"requests": 50, "window": 60}          # 50 req/min admin
            }
        }

        # Configuración por defecto para otros dominios
        default_config = {
            "high_priority": {"requests": 200, "window": 60},
            "medium_priority": {"requests": 100, "window": 60},
            "low_priority": {"requests": 50, "window": 60},
            "general": {"requests": 120, "window": 60},
            "admin": {"requests": 30, "window": 60}
        }

        return rate_configs.get(domain_prefix, default_config)

    def _get_rate_limit_category(self, path: str, method: str) -> str:
        """Determina la categoría de rate limit según el endpoint del dominio 'beauty_'"""

        if self.domain_prefix == "beauty_":
            if "/citas/disponibles" in path:
                return "availability"
            elif "/citas/book" in path or "/citas/cancel" in path:
                return "booking"
            elif "/historial" in path:
                return "history"
            elif "/admin" in path:
                return "admin"

        return "general"

    async def dispatch(self, request: Request, call_next):
        # Obtener información del request
        client_ip = request.client.host
        path = request.url.path
        method = request.method

        # Solo aplicar rate limiting a endpoints de tu dominio
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        # Determinar categoría de rate limit
        category = self._get_rate_limit_category(path, method)
        rate_config = self.rate_limits.get(category, self.rate_limits["general"])

        # Verificar rate limit
        if not self._check_rate_limit(client_ip, category, rate_config):
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "category": category,
                    "limit": rate_config["requests"],
                    "window": rate_config["window"],
                    "domain": self.domain_prefix
                }
            )

        # Continuar con el request
        response = await call_next(request)
        return response

    def _check_rate_limit(self, client_ip: str, category: str, config: Dict) -> bool:
        """Verifica si el cliente excede el rate limit"""
        current_time = int(time.time())
        window_start = current_time - config["window"]

        # Clave específica para el dominio y categoría
        key = f"{self.domain_prefix}:rate_limit:{category}:{client_ip}"

        # Obtener requests en la ventana actual
        requests = self.redis.zrangebyscore(key, window_start, current_time)

        if len(requests) >= config["requests"]:
            return False

        # Añadir request actual
        self.redis.zadd(key, {str(current_time): current_time})
        self.redis.expire(key, config["window"])

        # Limpiar requests antiguos
        self.redis.zremrangebyscore(key, 0, window_start)

        return True