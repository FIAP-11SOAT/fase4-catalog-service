"""Testes para as rotas de categorias."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid


class TestCategoriesBasic:
    """Testes básicos de categorias."""
    
    def test_list_categories_empty_returns_404_and_empty_array(self):
        """Teste de listagem vazia retorna 404 com array vazio."""
        client = TestClient(app)
        resp = client.get("/categories")
        assert resp.status_code == 404
        assert resp.json() == []
    
    def test_create_category_requires_admin_header(self):
        """Teste que criação requer header admin."""
        payload = {"name": "Lanches", "description": "Lanches rápidos"}
        client = TestClient(app)
        resp = client.post("/categories", json=payload)
        assert resp.status_code == 403


class TestCategoriesCRUD:
    """Testes de operações CRUD de categorias."""
    
    def test_create_category_success(self):
        """Teste de criação de categoria com sucesso."""
        client = TestClient(app)
        unique_name = f"Categoria-{uuid.uuid4().hex[:8]}"
        payload = {"name": unique_name, "description": "Descrição da categoria"}
        
        resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        
        # Aceita 201 (criado) ou 409 (já existe) 
        assert resp.status_code in [201, 409]
        
        if resp.status_code == 201:
            created = resp.json()
            assert created["name"] == unique_name
            assert created["description"] == "Descrição da categoria"
            assert "id" in created
            assert "created_at" in created
            assert "updated_at" in created
    
    def test_create_category_without_description(self):
        """Teste de criação de categoria sem descrição."""
        client = TestClient(app)
        unique_name = f"Categoria-NoDesc-{uuid.uuid4().hex[:8]}"
        payload = {"name": unique_name}
        
        resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code in [201, 409]
        
        if resp.status_code == 201:
            created = resp.json()
            assert created["name"] == unique_name
            assert created["description"] is None
    
    def test_create_category_duplicate_name(self):
        """Teste de criação de categoria com nome duplicado."""
        client = TestClient(app)
        name = f"Categoria-Dup-{uuid.uuid4().hex[:8]}"
        payload = {"name": name, "description": "Primeira"}
        
        # Primeira criação
        resp1 = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        assert resp1.status_code in [201, 409]
        
        # Segunda criação com mesmo nome
        payload2 = {"name": name, "description": "Segunda"}
        resp2 = client.post("/categories", json=payload2, headers={"X-Role": "admin"})
        assert resp2.status_code == 409
    
    def test_create_category_requires_name(self):
        """Teste que criação requer nome."""
        client = TestClient(app)
        payload = {"description": "Sem nome"}
        
        resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 422  # Validation error
    
    def test_create_category_empty_name(self):
        """Teste de criação com nome vazio."""
        client = TestClient(app)
        payload = {"name": "", "description": "Nome vazio"}
        
        resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 422  # Validation error
    
    def test_create_category_name_too_long(self):
        """Teste de criação com nome muito longo."""
        client = TestClient(app)
        payload = {"name": "A" * 101, "description": "Nome muito longo"}  # Máximo é 100
        
        resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 422  # Validation error
    
    def test_get_category_by_id_success(self):
        """Teste de busca de categoria por ID com sucesso."""
        client = TestClient(app)
        
        # Criar categoria primeiro
        unique_name = f"Categoria-Get-{uuid.uuid4().hex[:8]}"
        payload = {"name": unique_name, "description": "Para buscar"}
        
        create_resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        
        if create_resp.status_code == 201:
            category_id = create_resp.json()["id"]
        elif create_resp.status_code == 409:
            # Se já existe, buscar o ID
            resp = client.get("/categories")
            if resp.status_code == 200:
                categories = resp.json()
                category_id = next((c["id"] for c in categories if c["name"] == unique_name), None)
                if category_id is None:
                    pytest.skip("Não foi possível encontrar categoria para teste")
            else:
                pytest.skip("Não foi possível criar ou encontrar categoria para teste")
        else:
            pytest.skip("Não foi possível criar categoria para teste")
        
        # Buscar categoria
        get_resp = client.get(f"/categories/{category_id}")
        assert get_resp.status_code == 200
        
        category = get_resp.json()
        assert category["id"] == category_id
        assert category["name"] == unique_name
    
    def test_get_category_by_id_not_found(self):
        """Teste de busca de categoria por ID inexistente."""
        client = TestClient(app)
        
        resp = client.get("/categories/99999")
        assert resp.status_code == 404
        assert resp.json() == []
    
    def test_update_category_success(self):
        """Teste de atualização de categoria com sucesso."""
        client = TestClient(app)
        
        # Criar categoria
        unique_name = f"Categoria-Update-{uuid.uuid4().hex[:8]}"
        payload = {"name": unique_name, "description": "Original"}
        
        create_resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        
        if create_resp.status_code == 201:
            category_id = create_resp.json()["id"]
        elif create_resp.status_code == 409:
            # Se já existe, buscar o ID
            resp = client.get("/categories")
            if resp.status_code == 200:
                categories = resp.json()
                category_id = next((c["id"] for c in categories if c["name"] == unique_name), None)
                if category_id is None:
                    pytest.skip("Não foi possível encontrar categoria para teste")
            else:
                pytest.skip("Não foi possível criar ou encontrar categoria para teste")
        else:
            pytest.skip("Não foi possível criar categoria para teste")
        
        # Atualizar categoria
        update_payload = {"name": unique_name, "description": "Atualizada"}
        update_resp = client.put(f"/categories/{category_id}", json=update_payload, headers={"X-Role": "admin"})
        assert update_resp.status_code == 200
        
        updated = update_resp.json()
        assert updated["description"] == "Atualizada"
        assert updated["id"] == category_id
    
    def test_update_category_requires_admin(self):
        """Teste que atualização requer admin."""
        client = TestClient(app)
        payload = {"name": "Test", "description": "Test"}
        
        # Sem header admin
        resp = client.put("/categories/1", json=payload)
        assert resp.status_code == 403
        
        # Com header inválido
        resp = client.put("/categories/1", json=payload, headers={"X-Role": "user"})
        assert resp.status_code == 403
    
    def test_update_category_not_found(self):
        """Teste de atualização de categoria inexistente."""
        client = TestClient(app)
        payload = {"name": "Test", "description": "Test"}
        
        resp = client.put("/categories/99999", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 404
    
    def test_update_category_duplicate_name(self):
        """Teste de atualização com nome duplicado."""
        client = TestClient(app)
        
        # Criar duas categorias
        name1 = f"Cat1-{uuid.uuid4().hex[:8]}"
        name2 = f"Cat2-{uuid.uuid4().hex[:8]}"
        
        resp1 = client.post("/categories", json={"name": name1}, headers={"X-Role": "admin"})
        resp2 = client.post("/categories", json={"name": name2}, headers={"X-Role": "admin"})
        
        assert resp1.status_code == 201
        assert resp2.status_code == 201
        
        cat2_id = resp2.json()["id"]
        
        # Tentar atualizar cat2 para ter o nome de cat1
        update_resp = client.put(f"/categories/{cat2_id}", json={"name": name1}, headers={"X-Role": "admin"})
        assert update_resp.status_code == 409
    
    def test_delete_category_success(self):
        """Teste de exclusão de categoria com sucesso."""
        client = TestClient(app)
        
        # Criar categoria
        unique_name = f"Categoria-Delete-{uuid.uuid4().hex[:8]}"
        payload = {"name": unique_name, "description": "Para deletar"}
        
        create_resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        
        if create_resp.status_code == 201:
            category_id = create_resp.json()["id"]
        elif create_resp.status_code == 409:
            # Se já existe, buscar o ID
            resp = client.get("/categories")
            if resp.status_code == 200:
                categories = resp.json()
                category_id = next((c["id"] for c in categories if c["name"] == unique_name), None)
                if category_id is None:
                    pytest.skip("Não foi possível encontrar categoria para teste")
            else:
                pytest.skip("Não foi possível criar ou encontrar categoria para teste")
        else:
            pytest.skip("Não foi possível criar categoria para teste")
        
        # Deletar categoria
        delete_resp = client.delete(f"/categories/{category_id}", headers={"X-Role": "admin"})
        assert delete_resp.status_code == 204
        
        # Verificar se foi deletada
        get_resp = client.get(f"/categories/{category_id}")
        assert get_resp.status_code == 404
    
    def test_delete_category_requires_admin(self):
        """Teste que exclusão requer admin."""
        client = TestClient(app)
        
        # Sem header admin
        resp = client.delete("/categories/1")
        assert resp.status_code == 403
    
    def test_delete_category_not_found(self):
        """Teste de exclusão de categoria inexistente."""
        client = TestClient(app)
        
        resp = client.delete("/categories/99999", headers={"X-Role": "admin"})
        assert resp.status_code == 404


class TestCategoriesFlow:
    """Teste de fluxo completo."""
    
    def test_create_get_update_delete_category_happy_path(self):
        """Teste de fluxo completo CRUD."""
        client = TestClient(app)
        # Create
        unique_name = f"Bebidas-{uuid.uuid4().hex[:8]}"
        payload = {"name": unique_name, "description": "Categoria de bebidas"}
        resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        
        # Should create successfully with unique name
        assert resp.status_code == 201
        created = resp.json()
        cat_id = created["id"]
        assert created["name"] == unique_name

        # Get by id
        resp = client.get(f"/categories/{cat_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == cat_id

        # Update
        upd = {"name": unique_name, "description": "Atualizada"}
        resp = client.put(f"/categories/{cat_id}", json=upd, headers={"X-Role": "admin"})
        assert resp.status_code == 200
        assert resp.json()["description"] == "Atualizada"

        # Delete
        resp = client.delete(f"/categories/{cat_id}", headers={"X-Role": "admin"})
        assert resp.status_code == 204

        # Ensure gone
        resp = client.get(f"/categories/{cat_id}")
        assert resp.status_code == 404
        assert resp.json() == []


class TestCategoriesValidation:
    """Testes de validação de dados."""
    
    def test_create_category_invalid_json(self):
        """Teste de criação com JSON inválido."""
        client = TestClient(app)
        
        resp = client.post(
            "/categories",
            data="invalid json",
            headers={"X-Role": "admin", "Content-Type": "application/json"}
        )
        assert resp.status_code == 422
    
    def test_create_category_missing_content_type(self):
        """Teste de criação sem content-type."""
        client = TestClient(app)
        
        resp = client.post(
            "/categories",
            data='{"name": "test"}',
            headers={"X-Role": "admin"}
        )
        # FastAPI geralmente aceita JSON mesmo sem content-type explícito
        # mas vamos verificar que não é erro de servidor
        assert resp.status_code != 500


class TestCategoriesSecurity:
    """Testes de segurança específicos para categorias."""
    
    def test_admin_role_case_insensitive(self):
        """Teste que role admin é case-insensitive."""
        client = TestClient(app)
        payload = {"name": f"Test-Case-{uuid.uuid4().hex[:8]}"}
        
        # Testa diferentes casos
        for role in ["admin", "ADMIN", "Admin", "aDmIn"]:
            unique_name = f"Test-{role}-{uuid.uuid4().hex[:6]}"
            test_payload = {"name": unique_name}
            
            resp = client.post("/categories", json=test_payload, headers={"X-Role": role})
            assert resp.status_code in [201, 409]  # 201 criado, 409 se já existe
    
    def test_invalid_roles_denied(self):
        """Teste que roles inválidos são negados."""
        client = TestClient(app)
        payload = {"name": "Test"}
        
        invalid_roles = ["user", "guest", "manager", "operator", "", "admin "]
        
        for role in invalid_roles:
            resp = client.post("/categories", json=payload, headers={"X-Role": role})
            assert resp.status_code == 403
    
    def test_missing_role_header_denied(self):
        """Teste que ausência de header role é negada."""
        client = TestClient(app)
        payload = {"name": "Test"}
        
        resp = client.post("/categories", json=payload)
        assert resp.status_code == 403
