# app/middleware/domain_validator.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import json
from typing import Dict, Any, Optional
from datetime import datetime

class DomainValidator(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.validators = self._get_domain_validators(domain_prefix)

    def _get_domain_validators(self, domain_prefix: str) -> Dict[str, Any]:
        """Validadores específicos para el dominio 'beauty_'"""

        validators = {
            "beauty_": {
                "required_headers": ["X-Beauty-Cliente-ID"], # ID de cliente para ciertas operaciones
                "business_hours": (9, 21),                   # 9 AM a 9 PM
                "consent_required": ["/procedimientos/invasivos"], # Procedimientos que requieren consentimiento
                "restricted_days": ["/procedimientos/especializados"] # Restricción de días para ciertos procedimientos
            }
        }

        return validators.get(domain_prefix, {
            "required_headers": [],
            "business_hours": (0, 24),
            "special_validations": []
        })

    def _validate_business_hours(self, path: str) -> bool:
        """Valida horarios de atención de la clínica"""
        current_hour = datetime.now().hour
        start_hour, end_hour = self.validators.get("business_hours", (0, 24))

        # No hay excepciones 24/7 en este negocio, así que solo validamos horario
        return start_hour <= current_hour < end_hour

    def _validate_required_headers(self, request: Request) -> bool:
        """Valida headers requeridos por dominio"""
        required = self.validators.get("required_headers", [])

        for header in required:
            if header not in request.headers:
                return False

        return True

    def _validate_domain_specific_rules(self, request: Request, path: str) -> tuple[bool, Optional[str]]:
        """Validaciones específicas del dominio 'beauty_'"""

        # Validación 1: Consentimiento requerido para procedimientos invasivos
        consent_required_endpoints = self.validators.get("consent_required", [])
        if any(endpoint in path for endpoint in consent_required_endpoints):
            if "X-Consentimiento-ID" not in request.headers:
                return False, "Procedimiento invasivo requiere consentimiento"

        # Validación 2: Restricción de días para procedimientos especializados (ej. solo entre semana)
        restricted_endpoints = self.validators.get("restricted_days", [])
        if any(endpoint in path for endpoint in restricted_endpoints):
            if datetime.now().weekday() >= 5:  # Sábado o Domingo
                return False, "Procedimiento no disponible los fines de semana"

        return True, None

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Solo validar endpoints del dominio
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        # Validar horarios de atención
        if not self._validate_business_hours(path):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Fuera de horario de atención",
                    "domain": self.domain_prefix,
                    "business_hours": self.validators["business_hours"]
                }
            )

        # Validar headers requeridos
        if not self._validate_required_headers(request):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Headers requeridos faltantes",
                    "required_headers": self.validators["required_headers"]
                }
            )

        # Validaciones específicas del dominio
        is_valid, error_message = self._validate_domain_specific_rules(request, path)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail={"error": error_message, "domain": self.domain_prefix}
            )

        return await call_next(request)