import pytest
from fastapi import status
from datetime import datetime

@pytest.mark.tipo_d
@pytest.mark.integration
class TestAccountsEndpointsSecureBank:
    """Tests completos de endpoints para cuentas en SecureBank (tipo D)"""

    def test_crud_completo_account(self, authenticated_client, sample_account):
        """Test CRUD completo para cuenta bancaria"""
        # CREATE
        create_response = authenticated_client.post(
            "/api/v1/accounts",
            json=sample_account
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_data = create_response.json()
        account_id = created_data["account_id"]
        assert created_data["customer_name"] == sample_account["customer_name"]
        assert created_data["balance"] == sample_account["balance"]
        assert "created_at" in created_data

        # READ
        read_response = authenticated_client.get(f"/api/v1/accounts/{account_id}")
        assert read_response.status_code == status.HTTP_200_OK
        read_data = read_response.json()
        assert read_data["account_id"] == account_id
        assert read_data["account_type"] == sample_account["account_type"]

        # UPDATE
        update_data = {
            "customer_name": "Cliente Actualizado",
            "account_type": "checking",
            "balance": sample_account["balance"] + 100.0
        }
        update_response = authenticated_client.put(
            f"/api/v1/accounts/{account_id}",
            json=update_data
        )
        assert update_response.status_code == status.HTTP_200_OK
        updated_data = update_response.json()
        assert updated_data["customer_name"] == update_data["customer_name"]
        assert updated_data["account_type"] == update_data["account_type"]
        assert "updated_at" in updated_data
        assert datetime.fromisoformat(updated_data["updated_at"]) > datetime.fromisoformat(created_data["created_at"])

        # DELETE
        delete_response = authenticated_client.delete(f"/api/v1/accounts/{account_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        verify_response = authenticated_client.get(f"/api/v1/accounts/{account_id}")
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND

    def test_busqueda_avanzada_accounts(self, authenticated_client, sample_account):
        """Test búsqueda avanzada de cuentas con filtros"""
        # Crear múltiples cuentas
        for i in range(5):
            account_data = {
                **sample_account,
                "account_id": fake.uuid4()[:8].upper(),
                "account_type": "savings" if i % 2 == 0 else "checking",
                "balance": 1000.0 + (i * 100.0)
            }
            authenticated_client.post("/api/v1/accounts", json=account_data)

        # Búsqueda por tipo de cuenta y saldo mínimo
        search_response = authenticated_client.get(
            "/api/v1/accounts/search",
            params={
                "account_type": "savings",
                "min_balance": 1000.0,
                "limit": 10
            }
        )
        assert search_response.status_code == status.HTTP_200_OK
        search_data = search_response.json()
        assert "items" in search_data
        assert "total" in search_data
        assert len(search_data["items"]) > 0
        for item in search_data["items"]:
            assert item["account_type"] == "savings"
            assert item["balance"] >= 1000.0

    def test_paginacion_accounts(self, authenticated_client):
        """Test paginación de cuentas"""
        # Crear 25 cuentas
        for i in range(25):
            account_data = {
                "account_id": fake.uuid4()[:8].upper(),
                "customer_name": f"Cliente {i}",
                "balance": 1000.0 + (i * 50.0),
                "account_type": "savings"
            }
            authenticated_client.post("/api/v1/accounts", json=account_data)

        # Página 1
        page1_response = authenticated_client.get(
            "/api/v1/accounts",
            params={"skip": 0, "limit": 10}
        )
        assert page1_response.status_code == status.HTTP_200_OK
        page1_data = page1_response.json()
        assert len(page1_data["items"]) == 10
        assert page1_data["total"] >= 25
        assert page1_data["page"] == 1
        assert page1_data["has_next"] is True

        # Página 2
        page2_response = authenticated_client.get(
            "/api/v1/accounts",
            params={"skip": 10, "limit": 10}
        )
        assert page2_response.status_code == status.HTTP_200_OK
        page2_data = page2_response.json()
        assert len(page2_data["items"]) == 10
        assert page2_data["page"] == 2
        page1_ids = [item["account_id"] for item in page1_data["items"]]
        page2_ids = [item["account_id"] for item in page2_data["items"]]
        assert len(set(page1_ids) & set(page2_ids)) == 0

    def test_validaciones_negocio_accounts(self, authenticated_client):
        """Test validaciones de negocio para cuentas"""
        # Test cuenta duplicada
        account_data1 = {
            "account_id": "ACC12345",
            "customer_name": "Cliente Duplicado",
            "balance": 1000.0,
            "account_type": "savings"
        }
        account_data2 = {
            "account_id": "ACC12345",  # Mismo ID
            "customer_name": "Otro Cliente",
            "balance": 2000.0,
            "account_type": "checking"
        }
        response1 = authenticated_client.post("/api/v1/accounts", json=account_data1)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = authenticated_client.post("/api/v1/accounts", json=account_data2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "duplicado" in response2.json()["detail"].lower()

@pytest.mark.tipo_d
@pytest.mark.unit
class TestAccountValidations:
    """Tests de validaciones para cuentas en SecureBank"""
    def test_validacion_campos_requeridos(self, authenticated_client):
        """Test validación de campos requeridos"""
        invalid_data = {
            "customer_name": "Cliente Incompleto",
            # Falta account_id
            "balance": 1000.0
        }
        response = authenticated_client.post("/api/v1/accounts", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()["detail"]
        assert any("account_id" in str(error) for error in errors)

    def test_validacion_saldo_negativo(self, authenticated_client):
        """Test validación de saldo negativo"""
        invalid_data = {
            "account_id": fake.uuid4()[:8].upper(),
            "customer_name": "Cliente Inválido",
            "balance": -100.0,  # Saldo negativo
            "account_type": "savings"
        }
        response = authenticated_client.post("/api/v1/accounts", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY