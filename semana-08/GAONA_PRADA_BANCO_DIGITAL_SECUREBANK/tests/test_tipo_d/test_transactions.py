import pytest
from fastapi import status
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

@pytest.mark.tipo_d
@pytest.mark.integration
class TestTransactionsEndpointsSecureBank:
    """Tests completos de endpoints para transacciones en SecureBank (tipo D)"""

    def test_crud_completo_transaction(self, authenticated_client, sample_account, sample_transaction):
        """Test CRUD completo para transacción bancaria"""
        # Crear cuenta primero
        create_account_response = authenticated_client.post("/api/v1/accounts", json=sample_account)
        account_id = create_account_response.json()["account_id"]
        transaction_data = {**sample_transaction, "account_id": account_id}

        # CREATE
        create_response = authenticated_client.post(
            "/api/v1/transactions",
            json=transaction_data
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_data = create_response.json()
        transaction_id = created_data["transaction_id"]
        assert created_data["amount"] == transaction_data["amount"]
        assert created_data["transaction_type"] == transaction_data["transaction_type"]

        # READ
        read_response = authenticated_client.get(f"/api/v1/transactions/{transaction_id}")
        assert read_response.status_code == status.HTTP_200_OK
        read_data = read_response.json()
        assert read_data["transaction_id"] == transaction_id

        # UPDATE
        update_data = {
            "amount": transaction_data["amount"] + 50.0,
            "transaction_type": "deposit",
            "metodo_pago": "tarjeta"
        }
        update_response = authenticated_client.put(
            f"/api/v1/transactions/{transaction_id}",
            json=update_data
        )
        assert update_response.status_code == status.HTTP_200_OK
        updated_data = update_response.json()
        assert updated_data["amount"] == update_data["amount"]

        # DELETE
        delete_response = authenticated_client.delete(f"/api/v1/transactions/{transaction_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        verify_response = authenticated_client.get(f"/api/v1/transactions/{transaction_id}")
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND

    def test_transaccion_saldo_insuficiente(self, authenticated_client, sample_account):
        """Test transacción con saldo insuficiente"""
        # Crear cuenta con saldo bajo
        account_data = {**sample_account, "balance": 50.0}
        create_account_response = authenticated_client.post("/api/v1/accounts", json=account_data)
        account_id = create_account_response.json()["account_id"]

        # Intentar retiro mayor al saldo
        transaction_data = {
            "transaction_id": fake.uuid4()[:8].upper(),
            "account_id": account_id,
            "amount": 100.0,
            "transaction_type": "withdrawal",
            "fecha_transaccion": datetime.now().isoformat(),
            "metodo_pago": "tarjeta"
        }
        response = authenticated_client.post("/api/v1/transactions", json=transaction_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "saldo insuficiente" in response.json()["detail"].lower()

    def test_busqueda_transacciones_por_fecha(self, authenticated_client, sample_account, sample_transaction):
        """Test búsqueda de transacciones por rango de fechas"""
        # Crear cuenta
        create_account_response = authenticated_client.post("/api/v1/accounts", json=sample_account)
        account_id = create_account_response.json()["account_id"]

        # Crear múltiples transacciones
        for i in range(5):
            transaction_data = {
                **sample_transaction,
                "transaction_id": fake.uuid4()[:8].upper(),
                "account_id": account_id,
                "fecha_transaccion": (datetime.now() - timedelta(days=i)).isoformat()
            }
            authenticated_client.post("/api/v1/transactions", json=transaction_data)

        # Buscar transacciones en un rango de fechas
        start_date = (datetime.now() - timedelta(days=3)).date().isoformat()
        end_date = datetime.now().date().isoformat()
        search_response = authenticated_client.get(
            "/api/v1/transactions/search",
            params={"start_date": start_date, "end_date": end_date}
        )
        assert search_response.status_code == status.HTTP_200_OK
        search_data = search_response.json()
        assert len(search_data["items"]) > 0
        for item in search_data["items"]:
            assert start_date <= item["fecha_transaccion"].split("T")[0] <= end_date

    def test_external_payment_api(self, authenticated_client, sample_account, sample_transaction, mock_payment_api):
        """Test integración con API externa de pagos"""
        create_account_response = authenticated_client.post("/api/v1/accounts", json=sample_account)
        account_id = create_account_response.json()["account_id"]
        transaction_data = {
            **sample_transaction,
            "account_id": account_id,
            "transaction_type": "transfer"
        }
        response = authenticated_client.post("/api/v1/transactions", json=transaction_data)
        assert response.status_code == status.HTTP_201_CREATED
        mock_payment_api.process_payment.assert_called_once()

@pytest.mark.tipo_d
@pytest.mark.unit
class TestTransactionValidations:
    """Tests de validaciones para transacciones en SecureBank"""
    def test_validacion_monto_negativo(self, authenticated_client, sample_account):
        """Test validación de monto negativo"""
        create_account_response = authenticated_client.post("/api/v1/accounts", json=sample_account)
        account_id = create_account_response.json()["account_id"]
        invalid_transaction = {
            "transaction_id": fake.uuid4()[:8].upper(),
            "account_id": account_id,
            "amount": -50.0,  # Monto negativo
            "transaction_type": "transfer"
        }
        response = authenticated_client.post("/api/v1/transactions", json=invalid_transaction)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY