"""Descripciones centralizadas para la documentación API de SecureBank"""

# Descripciones de tags
TAGS_METADATA = [
    {
        "name": "accounts",
        "description": "Operaciones CRUD para cuentas bancarias en SecureBank. "
                       "Permite crear, consultar, actualizar y eliminar cuentas.",
        "externalDocs": {
            "description": "Documentación externa de SecureBank",
            "url": "https://docs.securebank.com/api",
        },
    },
    {
        "name": "transactions",
        "description": "Gestión de transacciones bancarias, incluyendo depósitos, retiros y transferencias.",
    },
    {
        "name": "auth",
        "description": "Endpoints de autenticación para usuarios de SecureBank.",
    },
]

# Descripciones de endpoints
ENDPOINT_DESCRIPTIONS = {
    "create_account": """
    ### Crear Nueva Cuenta Bancaria

    Crea una nueva cuenta bancaria en SecureBank con las siguientes características:

    - **account_id**: Identificador único (formato ACCXXXXX).
    - **customer_name**: Nombre del titular.
    - **balance**: Saldo inicial (no negativo).
    - **account_type**: Tipo de cuenta (savings o checking).

    #### Ejemplo de uso:
    ```json
    {
        "account_id": "ACC12345",
        "customer_name": "Juan Perez",
        "balance": 1000.0,
        "account_type": "savings"
    }
    ```
    """
}