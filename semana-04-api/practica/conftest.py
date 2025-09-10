import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from main import app
from database import get_db, Base

# Base de datos de prueba (en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    # Crear tablas de prueba
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Limpiar después de cada test
    Base.metadata.drop_all(bind=engine)
    # Eliminar archivo de base de datos de prueba
    if os.path.exists("test.db"):
        os.remove("test.db")