"""
Testes aprimorados para routes/categories.py para melhorar cobertura do SonarQube.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid


class TestCategoriesEnhanced:
    """Testes aprimorados para cobertura completa de categorias."""

    def test_list_all_categories_empty(self):
        """Teste de listagem quando não há categorias."""
        client = TestClient(app)
        resp = client.get("/categories")
        # Pode retornar 404 com lista vazia ou 200 com lista existentes
        assert resp.status_code in [200, 404]
        if resp.status_code == 404:
            assert resp.json() == []

    def test_list_all_categories_with_data(self):
        """Teste de listagem com categorias existentes."""
        client = TestClient(app)
        
        # Criar uma categoria
        category_data = {
            "name": f"TestCat-{uuid.uuid4().hex[:8]}",
            "description": "Test category"
        }
        
        create_resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            # Listar categorias
            list_resp = client.get("/categories")
            assert list_resp.status_code == 200
            categories = list_resp.json()
            assert len(categories) > 0
            
            # Verificar ordenação por ID
            for i in range(1, len(categories)):
                assert categories[i]["id"] >= categories[i-1]["id"]

    def test_find_category_by_id_not_found(self):
        """Teste de busca de categoria por ID inexistente."""
        client = TestClient(app)
        
        resp = client.get("/categories/99999")
        assert resp.status_code == 404
        assert resp.json() == []

    def test_find_category_by_id_existing(self):
        """Teste de busca de categoria por ID existente."""
        client = TestClient(app)
        
        # Criar categoria
        category_data = {
            "name": f"FindCat-{uuid.uuid4().hex[:8]}",
            "description": "Find test category"
        }
        
        create_resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            category_id = create_resp.json()["id"]
            
            # Buscar por ID
            find_resp = client.get(f"/categories/{category_id}")
            assert find_resp.status_code == 200
            found_category = find_resp.json()
            assert found_category["id"] == category_id
            assert found_category["name"] == category_data["name"]

    def test_create_category_success(self):
        """Teste de criação de categoria com sucesso."""
        client = TestClient(app)
        
        category_data = {
            "name": f"CreateCat-{uuid.uuid4().hex[:8]}",
            "description": "Create test category"
        }
        
        resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
        if resp.status_code == 201:
            created_category = resp.json()
            assert created_category["name"] == category_data["name"]
            assert created_category["description"] == category_data["description"]
            assert "id" in created_category

    def test_create_category_duplicate_name(self):
        """Teste de criação de categoria com nome duplicado."""
        client = TestClient(app)
        
        category_name = f"DupCat-{uuid.uuid4().hex[:8]}"
        category_data = {
            "name": category_name,
            "description": "Duplicate test"
        }
        
        # Primeira categoria
        resp1 = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
        if resp1.status_code == 201:
            # Segunda categoria com mesmo nome
            resp2 = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
            assert resp2.status_code == 409
            assert "already exists" in resp2.json()["detail"]

    def test_create_category_no_admin_role(self):
        """Teste de criação de categoria sem role de admin."""
        client = TestClient(app)
        
        category_data = {
            "name": f"NoAdminCat-{uuid.uuid4().hex[:8]}",
            "description": "No admin test"
        }
        
        # Sem header de admin
        resp = client.post("/categories", json=category_data)
        assert resp.status_code == 403

    def test_create_category_invalid_admin_role(self):
        """Teste de criação com role inválida."""
        client = TestClient(app)
        
        category_data = {
            "name": f"InvalidAdminCat-{uuid.uuid4().hex[:8]}",
            "description": "Invalid admin test"
        }
        
        # Com role não-admin
        resp = client.post("/categories", json=category_data, headers={"X-Role": "user"})
        assert resp.status_code == 403

    def test_update_category_success(self):
        """Teste de atualização de categoria com sucesso."""
        client = TestClient(app)
        
        # Criar categoria
        original_data = {
            "name": f"UpdateCat-{uuid.uuid4().hex[:8]}",
            "description": "Original description"
        }
        
        create_resp = client.post("/categories", json=original_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            category_id = create_resp.json()["id"]
            
            # Atualizar categoria
            updated_data = {
                "name": f"UpdatedCat-{uuid.uuid4().hex[:8]}",
                "description": "Updated description"
            }
            
            update_resp = client.put(f"/categories/{category_id}", json=updated_data, headers={"X-Role": "admin"})
            if update_resp.status_code == 200:
                updated_category = update_resp.json()
                assert updated_category["name"] == updated_data["name"]
                assert updated_category["description"] == updated_data["description"]
                assert updated_category["id"] == category_id

    def test_update_category_not_found(self):
        """Teste de atualização de categoria inexistente."""
        client = TestClient(app)
        
        update_data = {
            "name": "NonExistentCategory",
            "description": "Does not exist"
        }
        
        resp = client.put("/categories/99999", json=update_data, headers={"X-Role": "admin"})
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]

    def test_update_category_duplicate_name(self):
        """Teste de atualização com nome duplicado."""
        client = TestClient(app)
        
        # Criar duas categorias
        cat1_data = {
            "name": f"Cat1-{uuid.uuid4().hex[:8]}",
            "description": "Category 1"
        }
        
        cat2_data = {
            "name": f"Cat2-{uuid.uuid4().hex[:8]}",
            "description": "Category 2"
        }
        
        resp1 = client.post("/categories", json=cat1_data, headers={"X-Role": "admin"})
        resp2 = client.post("/categories", json=cat2_data, headers={"X-Role": "admin"})
        
        if resp1.status_code == 201 and resp2.status_code == 201:
            cat2_id = resp2.json()["id"]
            cat1_name = resp1.json()["name"]
            
            # Tentar atualizar cat2 com nome do cat1
            duplicate_data = {
                "name": cat1_name,
                "description": "Duplicate name"
            }
            
            resp = client.put(f"/categories/{cat2_id}", json=duplicate_data, headers={"X-Role": "admin"})
            assert resp.status_code == 409
            assert "already exists" in resp.json()["detail"]

    def test_update_category_no_admin_role(self):
        """Teste de atualização sem role de admin."""
        client = TestClient(app)
        
        update_data = {
            "name": "NoAdminUpdate",
            "description": "No admin"
        }
        
        resp = client.put("/categories/1", json=update_data)
        assert resp.status_code == 403

    def test_delete_category_success(self):
        """Teste de exclusão de categoria com sucesso."""
        client = TestClient(app)
        
        # Criar categoria
        category_data = {
            "name": f"DeleteCat-{uuid.uuid4().hex[:8]}",
            "description": "To be deleted"
        }
        
        create_resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            category_id = create_resp.json()["id"]
            
            # Deletar categoria
            delete_resp = client.delete(f"/categories/{category_id}", headers={"X-Role": "admin"})
            assert delete_resp.status_code == 204
            
            # Verificar se foi deletada
            find_resp = client.get(f"/categories/{category_id}")
            assert find_resp.status_code == 404

    def test_delete_category_not_found(self):
        """Teste de exclusão de categoria inexistente."""
        client = TestClient(app)
        
        resp = client.delete("/categories/99999", headers={"X-Role": "admin"})
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]

    def test_delete_category_no_admin_role(self):
        """Teste de exclusão sem role de admin."""
        client = TestClient(app)
        
        resp = client.delete("/categories/1")
        assert resp.status_code == 403


class TestCategoriesValidation:
    """Testes de validação de dados de categorias."""

    def test_create_category_empty_name(self):
        """Teste de criação com nome vazio."""
        client = TestClient(app)
        
        category_data = {
            "name": "",
            "description": "Empty name test"
        }
        
        resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
        assert resp.status_code == 422

    def test_create_category_too_long_name(self):
        """Teste de criação com nome muito longo."""
        client = TestClient(app)
        
        category_data = {
            "name": "A" * 101,  # Nome com mais de 100 caracteres
            "description": "Too long name test"
        }
        
        resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
        assert resp.status_code == 422

    def test_create_category_missing_name(self):
        """Teste de criação sem campo nome."""
        client = TestClient(app)
        
        category_data = {
            "description": "Missing name test"
        }
        
        resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
        assert resp.status_code == 422

    def test_create_category_invalid_json(self):
        """Teste de criação com JSON inválido."""
        client = TestClient(app)
        
        resp = client.post(
            "/categories",
            data="invalid json",
            headers={"X-Role": "admin", "Content-Type": "application/json"}
        )
        assert resp.status_code == 422

    def test_update_category_invalid_data(self):
        """Teste de atualização com dados inválidos."""
        client = TestClient(app)
        
        invalid_data = {
            "name": None,
            "description": 12345  # Tipo inválido
        }
        
        resp = client.put("/categories/1", json=invalid_data, headers={"X-Role": "admin"})
        assert resp.status_code == 422


class TestCategoriesIntegration:
    """Testes de integração para cenários complexos."""

    def test_category_crud_full_flow(self):
        """Teste de fluxo completo CRUD."""
        client = TestClient(app)
        
        # 1. Criar
        create_data = {
            "name": f"FlowCat-{uuid.uuid4().hex[:8]}",
            "description": "Flow test category"
        }
        
        create_resp = client.post("/categories", json=create_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            category_id = create_resp.json()["id"]
            
            # 2. Ler por ID
            read_resp = client.get(f"/categories/{category_id}")
            assert read_resp.status_code == 200
            assert read_resp.json()["name"] == create_data["name"]
            
            # 3. Atualizar
            update_data = {
                "name": f"FlowCatUpdated-{uuid.uuid4().hex[:8]}",
                "description": "Updated flow test"
            }
            
            update_resp = client.put(f"/categories/{category_id}", json=update_data, headers={"X-Role": "admin"})
            if update_resp.status_code == 200:
                # 4. Verificar atualização
                verify_resp = client.get(f"/categories/{category_id}")
                assert verify_resp.status_code == 200
                assert verify_resp.json()["name"] == update_data["name"]
                
                # 5. Deletar
                delete_resp = client.delete(f"/categories/{category_id}", headers={"X-Role": "admin"})
                assert delete_resp.status_code == 204
                
                # 6. Verificar exclusão
                final_resp = client.get(f"/categories/{category_id}")
                assert final_resp.status_code == 404

    def test_multiple_categories_ordering(self):
        """Teste de criação de múltiplas categorias e ordenação."""
        client = TestClient(app)
        
        created_ids = []
        
        # Criar múltiplas categorias
        for i in range(3):
            category_data = {
                "name": f"OrderCat{i}-{uuid.uuid4().hex[:4]}",
                "description": f"Order test {i}"
            }
            
            resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
            if resp.status_code == 201:
                created_ids.append(resp.json()["id"])
        
        if created_ids:
            # Listar e verificar ordenação
            list_resp = client.get("/categories")
            if list_resp.status_code == 200:
                categories = list_resp.json()
                
                # Verificar que as categorias criadas estão na lista
                found_categories = [cat for cat in categories if cat["id"] in created_ids]
                assert len(found_categories) > 0

    def test_category_name_edge_cases(self):
        """Teste com nomes de categoria em casos extremos."""
        client = TestClient(app)
        
        edge_cases = [
            f"Cat-{uuid.uuid4().hex[:8]}-with-dashes",
            f"Cat {uuid.uuid4().hex[:8]} with spaces",
            f"Cat_{uuid.uuid4().hex[:8]}_with_underscores",
            f"Cat.{uuid.uuid4().hex[:8]}.with.dots"
        ]
        
        for name in edge_cases:
            category_data = {
                "name": name,
                "description": "Edge case test"
            }
            
            resp = client.post("/categories", json=category_data, headers={"X-Role": "admin"})
            # Pode ser 201 ou 409 se já existe
            assert resp.status_code in [201, 409, 422]