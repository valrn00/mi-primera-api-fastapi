import pytest
from fastapi.testclient import TestClient

# Asumimos que la fixture `client` y la base de datos están configuradas
# en conftest.py, como en las prácticas anteriores.

# --- UTILITY FIXTURES (Se podrían mover a conftest.py) ---
@pytest.fixture
def manager_auth_headers(client):
    """Headers de autenticación para un usuario con rol de 'gerente'."""
    client.post("/auth/register", json={
        "username": "gerente_catering",
        "password": "test123",
        "role": "gerente"
    })
    login_response = client.post("/auth/login", data={
        "username": "gerente_catering",
        "password": "test123"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def employee_auth_headers(client):
    """Headers de autenticación para un usuario con rol de 'empleado'."""
    client.post("/auth/register", json={
        "username": "empleado_catering",
        "password": "test123",
        "role": "empleado"
    })
    login_response = client.post("/auth/login", data={
        "username": "empleado_catering",
        "password": "test123"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- TESTS DE AUTENTICACIÓN Y AUTORIZACIÓN ---
def test_register_catering_user(client):
    """Test de registro de un nuevo usuario en el dominio de Catering."""
    data = {
        "username": "usuario_catering_test",
        "password": "password123",
        "role": "empleado"
    }

    response = client.post("/auth/register", json=data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_login_catering_user(client):
    """Test de login para un usuario de Catering."""
    # Registrar usuario primero
    register_data = {
        "username": "gerente_catering_login",
        "password": "admin123",
        "role": "gerente"
    }
    client.post("/auth/register", json=register_data)

    # Login
    login_data = {
        "username": "gerente_catering_login",
        "password": "admin123"
    }
    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()

# --- TESTS DE ROLES Y PERMISOS ESPECÍFICOS ---
def test_manager_can_delete_menu(client, manager_auth_headers, sample_menu_data):
    """Test que un gerente puede eliminar un menú."""
    # Crear un menú para luego eliminarlo
    create_response = client.post("/cateringmenus/", json=sample_menu_data, headers=manager_auth_headers)
    menu_id = create_response.json()["id"]

    # Intentar eliminar con el token de gerente
    response = client.delete(f"/cateringmenus/{menu_id}", headers=manager_auth_headers)
    assert response.status_code == 200

def test_employee_cannot_delete_menu(client, employee_auth_headers, sample_menu_data):
    """Test que un empleado no puede eliminar un menú."""
    # Crear un menú para verificar la restricción
    create_response = client.post("/cateringmenus/", json=sample_menu_data, headers=employee_auth_headers)
    menu_id = create_response.json()["id"]

    # Intentar eliminar con el token de empleado
    response = client.delete(f"/cateringmenus/{menu_id}", headers=employee_auth_headers)
    assert response.status_code == 403 # Código de error de prohibido
    assert "No tiene permiso" in response.json()["detail"]

def test_unauthenticated_cannot_create_menu(client, sample_menu_data):
    """Test que un usuario no autenticado no puede crear un menú."""
    response = client.post("/cateringmenus/", json=sample_menu_data)
    assert response.status_code == 401
    assert "No autenticado" in response.json()["detail"]

def test_unauthenticated_cannot_delete_menu(client, sample_menu_data):
    """Test que un usuario no autenticado no puede eliminar un menú."""
    # Se intenta eliminar un menú inexistente, pero se valida la falta de autenticación
    response = client.delete(f"/cateringmenus/999", headers={})
    assert response.status_code == 401
    assert "No autenticado" in response.json()["detail"]