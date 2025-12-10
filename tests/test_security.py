"""Testes para o módulo de segurança."""
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.security import require_admin


class TestRequireAdminDependency:
    """Testes para a dependência require_admin."""
    
    def test_require_admin_with_valid_admin_header(self):
        """Teste com header admin válido."""
        result = require_admin("admin")
        assert result is True
    
    def test_require_admin_with_admin_uppercase(self):
        """Teste com header admin em maiúsculo."""
        result = require_admin("ADMIN")
        assert result is True
    
    def test_require_admin_with_admin_mixed_case(self):
        """Teste com header admin em caso misto."""
        result = require_admin("Admin")
        assert result is True
    
    def test_require_admin_without_header(self):
        """Teste sem header deve falhar."""
        with pytest.raises(HTTPException) as exc_info:
            require_admin(None)
        
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Admin role required"
    
    def test_require_admin_with_invalid_role(self):
        """Teste com role inválido deve falhar."""
        with pytest.raises(HTTPException) as exc_info:
            require_admin("user")
        
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Admin role required"
    
    def test_require_admin_with_empty_header(self):
        """Teste com header vazio deve falhar."""
        with pytest.raises(HTTPException) as exc_info:
            require_admin("")
        
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Admin role required"


class TestSecurityIntegration:
    """Testes de integração para segurança."""
    
    def test_require_admin_denied_no_header(self):
        """Teste de acesso negado sem header."""
        client = TestClient(app)
        r = client.post("/categories", json={"name": "test", "description": "test"})
        assert r.status_code == 403
    
    def test_require_admin_denied_invalid_role(self):
        """Teste de acesso negado com role inválido."""
        client = TestClient(app)
        r = client.post("/categories", json={"name": "test", "description": "test"}, headers={"X-Role": "user"})
        assert r.status_code == 403
    
    def test_require_admin_allowed_valid_admin(self):
        """Teste de acesso permitido com admin válido."""
        client = TestClient(app)
        r = client.post("/categories", json={"name": "test_admin", "description": "test"}, headers={"X-Role": "admin"})
        assert r.status_code in (201, 409)
    
    def test_require_admin_allowed_admin_uppercase(self):
        """Teste de acesso permitido com admin em maiúsculo."""
        client = TestClient(app)
        r = client.post("/categories", json={"name": "test_admin_upper", "description": "test"}, headers={"X-Role": "ADMIN"})
        assert r.status_code in (201, 409)
    
    def test_category_operations_require_admin(self):
        """Teste que todas as operações de categoria requerem admin."""
        client = TestClient(app)
        
        # POST sem admin
        r = client.post("/categories", json={"name": "test", "description": "test"})
        assert r.status_code == 403
        
        # Criar uma categoria primeiro para testar PUT e DELETE
        r = client.post("/categories", json={"name": "test_for_ops", "description": "test"}, headers={"X-Role": "admin"})
        if r.status_code == 201:
            cat_id = r.json()["id"]
        else:
            # Se já existe, pegar o ID
            r = client.get("/categories")
            if r.status_code == 200:
                categories = r.json()
                cat_id = next((c["id"] for c in categories if c["name"] == "test_for_ops"), 1)
            else:
                cat_id = 1  # fallback
        
        # PUT sem admin
        r = client.put(f"/categories/{cat_id}", json={"name": "updated", "description": "updated"})
        assert r.status_code == 403
        
        # DELETE sem admin
        r = client.delete(f"/categories/{cat_id}")
        assert r.status_code == 403
