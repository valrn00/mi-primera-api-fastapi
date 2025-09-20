import pytest
from fastapi.testclient import TestClient

class TestCateringAPI:
    """
    Tests específicos para el dominio de Catering.
    """

    def test_create_menu_success(self, client, sample_menu_data, auth_headers):
        """Test de creación exitosa de un menú en Catering."""
        response = client.post(
            "/cateringmenus/",
            json=sample_menu_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()

        # Validaciones específicas de tu dominio
        assert data["name"] == sample_menu_data["name"]
        assert data["price"] == sample_menu_data["price"]
        assert data["is_available"] is True

    def test_get_menu_not_found(self, client, auth_headers):
        """Test de menú no encontrado en Catering."""
        response = client.get(f"/cateringmenus/999", headers=auth_headers)

        assert response.status_code == 404
        assert "Menu no encontrado" in response.json()["detail"]

    def test_menu_validation_error(self, client, auth_headers):
        """Test de validación específica para un menú en Catering."""
        # Datos inválidos: nombre vacío y precio negativo
        invalid_data = {
            "name": "",
            "description": "Menú sin nombre",
            "price": -10.00,
            "is_vegetarian": False,
            "is_available": True
        }

        response = client.post(
            "/cateringmenus/",
            json=invalid_data,
            headers=auth_headers
        )

        assert response.status_code == 422
        errors = response.json()["detail"]

        # Validar errores específicos de tu dominio
        assert any("name" in str(error) and "field required" in str(error) for error in errors)
        assert any("price" in str(error) and "greater than 0" in str(error) for error in errors)

class TestCateringAPI:
    """
    Tests específicos para el dominio de Catering - FICHA 3147246
    """

    # ... (Mantener los tests de la Práctica 19 aquí) ...

    # --- TESTS DE CREACIÓN (POST) ---
    def test_create_menu_complete(self, client, auth_headers):
        """Test completo de creación para Catering."""
        data = {
            "name": "Menú Ejecutivo",
            "description": "Una opción rápida y deliciosa para eventos de negocios.",
            "price": 35.00,
            "is_vegetarian": False,
            "is_available": True
        }
        
        response = client.post("/cateringmenus/", json=data, headers=auth_headers)

        assert response.status_code == 201
        created = response.json()
        
        # Validaciones específicas de tu dominio
        assert created["name"] == data["name"]
        assert "id" in created

    def test_create_menu_duplicate(self, client, auth_headers):
        """Test de creación duplicada de un menú en Catering."""
        # Datos que causarían conflicto (p. ej., nombre único)
        data = {
            "name": "Menú de Temporada",
            "description": "Menú especial con ingredientes de temporada.",
            "price": 50.00,
            "is_vegetarian": True,
            "is_available": True
        }

        # Crear primera vez
        client.post("/cateringmenus/", json=data, headers=auth_headers)

        # Intentar crear duplicado
        response = client.post("/cateringmenus/", json=data, headers=auth_headers)

        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"].lower()

    # --- TESTS DE CONSULTA (GET) ---
    def test_get_menu_by_id(self, client, auth_headers):
        """Test de consulta de menú por ID en Catering."""
        create_data = {
            "name": "Menú Clásico",
            "description": "Una opción segura y popular para cualquier evento.",
            "price": 40.00,
            "is_vegetarian": False,
            "is_available": True
        }
        create_response = client.post("/cateringmenus/", json=create_data, headers=auth_headers)
        created_id = create_response.json()["id"]
        
        # Consultar por ID
        response = client.get(f"/cateringmenus/{created_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
        assert data["name"] == create_data["name"]

    def test_get_all_menus(self, client, auth_headers):
        """Test de consulta de todos los menús en Catering."""
        # Se asume que ya hay al menos un menú creado por otros tests
        response = client.get("/cateringmenus/", headers=auth_headers)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_menu_not_found(self, client, auth_headers):
        """Test de menú no encontrado en Catering."""
        response = client.get("/cateringmenus/99999", headers=auth_headers)

        assert response.status_code == 404
        assert "menu no encontrado" in response.json()["detail"].lower()
    
    # --- TESTS DE ACTUALIZACIÓN (PUT) ---
    def test_update_menu_complete(self, client, auth_headers):
        """Test de actualización completa de menú en Catering."""
        create_data = {
            "name": "Menú de Cumpleaños",
            "description": "Platos festivos para celebraciones.",
            "price": 25.00,
            "is_vegetarian": True,
            "is_available": True
        }
        create_response = client.post("/cateringmenus/", json=create_data, headers=auth_headers)
        menu_id = create_response.json()["id"]

        update_data = {
            "name": "Menú de Aniversario",
            "description": "Una opción más elegante para conmemorar.",
            "price": 55.00,
            "is_vegetarian": False,
            "is_available": False
        }
        
        response = client.put(f"/cateringmenus/{menu_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        updated = response.json()
        
        assert updated["name"] == update_data["name"]
        assert updated["price"] == update_data["price"]
        assert updated["is_available"] == update_data["is_available"]
    
    # --- TESTS DE ELIMINACIÓN (DELETE) ---
    def test_delete_menu_success(self, client, auth_headers):
        """Test de eliminación exitosa de un menú en Catering."""
        create_data = {
            "name": "Menú Light",
            "description": "Opciones saludables y ligeras.",
            "price": 20.00,
            "is_vegetarian": True,
            "is_available": True
        }
        create_response = client.post("/cateringmenus/", json=create_data, headers=auth_headers)
        menu_id = create_response.json()["id"]

        response = client.delete(f"/cateringmenus/{menu_id}", headers=auth_headers)

        assert response.status_code == 200

        # Verificar que ya no existe
        get_response = client.get(f"/cateringmenus/{menu_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_menu_not_found(self, client, auth_headers):
        """Test de eliminación de menú inexistente en Catering."""
        response = client.delete("/cateringmenus/99999", headers=auth_headers)

        assert response.status_code == 404

    # --- TESTS DE VALIDACIONES ESPECÍFICAS ---
    def test_menu_business_rules(self, client, auth_headers):
        """Test de reglas de negocio específicas para Catering (precio > 0)."""
        invalid_data = {
            "name": "Menú de Prueba",
            "description": "Menú con precio no válido.",
            "price": -10.00,  # Regla de negocio: El precio debe ser mayor que 0
            "is_vegetarian": False,
            "is_available": True
        }

        response = client.post("/cateringmenus/", json=invalid_data, headers=auth_headers)

        assert response.status_code == 422
        errors = response.json()["detail"]
        
        # Validar el mensaje de error específico
        assert any("price" in str(error) and "greater than 0" in str(error) for error in errors)