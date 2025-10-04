import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from app.main import app
from app.database import get_db, Base
from app.auth.auth_handler import create_access_token

# Configuración de base de datos de prueba
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./semana_8/test_securebank.db"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)

fake = Faker()

@pytest.fixture(scope="session")
def event_loop():
    """Configuración del loop de eventos para tests async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Fixture de sesión de base de datos para SecureBank"""
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture de cliente de prueba para SecureBank"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    """Fixture para headers de autenticación"""
    token_data = {"sub": "cliente_test_securebank"}
    token = create_access_token(token_data)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_account():
    """Fixture para cuenta bancaria (tipo D)"""
    return {
        "account_id": fake.uuid4()[:8].upper(),
        "customer_name": fake.name(),
        "balance": round(fake.random.uniform(100.0, 10000.0), 2),
        "account_type": fake.random_element(["savings", "checking"])
    }

@pytest.fixture
def sample_transaction():
    """Fixture para transacción bancaria (tipo D)"""
    return {
        "transaction_id": fake.uuid4()[:8].upper(),
        "account_id": fake.uuid4()[:8].upper(),
        "amount": round(fake.random.uniform(10.0, 5000.0), 2),
        "transaction_type": fake.random_element(["transfer", "deposit", "withdrawal"]),
        "fecha_transaccion": fake.date_time_this_year().isoformat(),
        "metodo_pago": fake.random_element(["tarjeta", "transferencia"])
    }

@pytest.fixture
def pagination_params():
    """Fixture para parámetros de paginación"""
    return {
        "skip": 0,
        "limit": 10,
        "sort_by": "account_id",
        "sort_order": "asc"
    }

@pytest.fixture
def search_params():
    """Fixture para parámetros de búsqueda de cuentas"""
    return {
        "query": fake.word(),
        "filters": {
            "account_type": "savings",
            "min_balance": 100.0
        }
    }

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)

fake = Faker()

@pytest.fixture(scope="session")
def event_loop():
    """Configuración del loop de eventos para tests async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Fixture de sesión de base de datos para SecureBank"""
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture de cliente de prueba para SecureBank"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def client_with_db_rollback(db_session):
    """Cliente que hace rollback automático después de cada test"""
    def override_get_db():
        try:
            transaction = db_session.begin()
            yield db_session
        finally:
            transaction.rollback()
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    """Fixture para headers de autenticación"""
    token_data = {"sub": "cliente_test_securebank"}
    token = create_access_token(token_data)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def authenticated_client(client_with_db_rollback, sample_user_generic, auth_headers):
    """Cliente pre-autenticado para tests rápidos"""
    client_with_db_rollback.post("/auth/register", json=sample_user_generic)
    class AuthenticatedClient:
        def __init__(self, base_client, headers):
            self.client = base_client
            self.headers = headers
        def get(self, url, **kwargs):
            kwargs.setdefault('headers', {}).update(self.headers)
            return self.client.get(url, **kwargs)
        def post(self, url, **kwargs):
            kwargs.setdefault('headers', {}).update(self.headers)
            return self.client.post(url, **kwargs)
        def put(self, url, **kwargs):
            kwargs.setdefault('headers', {}).update(self.headers)
            return self.client.put(url, **kwargs)
        def delete(self, url, **kwargs):
            kwargs.setdefault('headers', {}).update(self.headers)
            return self.client.delete(url, **kwargs)
    return AuthenticatedClient(client_with_db_rollback, auth_headers)

@pytest.fixture
def sample_user_generic():
    """Fixture para usuario genérico"""
    return {
        "username": "cliente_test_securebank",
        "email": fake.email(),
        "password": "Secure123!",
        "is_active": True
    }

@pytest.fixture
def sample_account():
    """Fixture para cuenta bancaria (tipo D)"""
    return {
        "account_id": fake.uuid4()[:8].upper(),
        "customer_name": fake.name(),
        "balance": round(fake.random.uniform(100.0, 10000.0), 2),
        "account_type": fake.random_element(["savings", "checking"])
    }

@pytest.fixture
def sample_transaction():
    """Fixture para transacción bancaria (tipo D)"""
    return {
        "transaction_id": fake.uuid4()[:8].upper(),
        "account_id": fake.uuid4()[:8].upper(),
        "amount": round(fake.random.uniform(10.0, 5000.0), 2),
        "transaction_type": fake.random_element(["transfer", "deposit", "withdrawal"]),
        "fecha_transaccion": fake.date_time_this_year().isoformat(),
        "metodo_pago": fake.random_element(["tarjeta", "transferencia"])
    }

@pytest.fixture
def mock_payment_api():
    """Mock para API externa de pagos"""
    with patch('app.external.payment_api_client') as mock:
        mock.process_payment.return_value = {"status": "success", "transaction_id": fake.uuid4()[:8].upper()}
        yield mock