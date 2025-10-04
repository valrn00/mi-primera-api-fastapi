import pytest
from fastapi import status

@pytest.mark.auth
@pytest.mark.integration
class TestAuthenticationSecureBank:
    """Tests completos de autenticación para SecureBank"""

    def test_login_valid_credentials(self, authenticated_client, sample_user_generic):
        """Test login con credenciales válidas"""
        response = authenticated_client.client.post(
            "/auth/login",
            json={
                "username": sample_user_generic["username"],
                "password": sample_user_generic["password"]
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_invalid_credentials(self, authenticated_client):
        """Test login con credenciales inválidas"""
        response = authenticated_client.client.post(
            "/auth/login",
            json={"username": "invalid_user", "password": "wrong_password"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "credenciales" in response.json()["detail"].lower()

    def test_logout(self, authenticated_client):
        """Test logout con token válido"""
        response = authenticated_client.post("/auth/logout")
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()

    def test_access_protected_endpoint_without_token(self, client_with_db_rollback):
        """Test acceso a endpoint protegido sin token"""
        response = client_with_db_rollback.get("/api/v1/accounts")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_expiration(self, authenticated_client, mocker):
        """Test manejo de token expirado"""
        mocker.patch(
            "app.auth.auth_handler.create_access_token",
            return_value=create_access_token({"sub": "test_user"}, expires_delta=-1)  # Token expirado
        )
        response = authenticated_client.get("/api/v1/accounts")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "expirado" in response.json()["detail"].lower()