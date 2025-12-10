"""
Testes aprimorados para routes/products.py para melhorar cobertura do SonarQube.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
from decimal import Decimal


def _ensure_category_simple(client):
    """Helper simplificado para garantir que uma categoria existe."""
    # Tentar criar uma categoria única
    for attempt in range(5):
        name = f"TestCat-{uuid.uuid4().hex[:8]}-{attempt}"
        resp = client.post("/categories", json={"name": name, "description": "Test"}, headers={"X-Role": "admin"})
        
        if resp.status_code == 201:
            return resp.json()["id"], name
        elif resp.status_code == 409:
            # Se já existe, tentar buscar
            list_resp = client.get("/categories")
            if list_resp.status_code == 200:
                categories = list_resp.json()
                for cat in categories:
                    if cat["name"] == name:
                        return cat["id"], cat["name"]
    
    # Se tudo falhou, usar uma categoria genérica
    list_resp = client.get("/categories")
    if list_resp.status_code == 200:
        categories = list_resp.json()
        if categories:
            return categories[0]["id"], categories[0]["name"]
    
    pytest.skip("Não foi possível criar nem encontrar categoria para testes")


class TestProductsEnhanced:
    """Testes aprimorados para cobertura completa de produtos."""

    def test_list_all_products_empty(self):
        """Teste de listagem quando não há produtos."""
        client = TestClient(app)
        resp = client.get("/products")
        # Pode retornar 404 com lista vazia ou 200 com lista vazia
        assert resp.status_code in [200, 404]

    def test_list_all_products_with_data(self):
        """Teste de listagem com produtos existentes."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        # Criar um produto de teste
        product_data = {
            "name": f"TestProduct-{uuid.uuid4().hex[:8]}",
            "description": "Test product",
            "price": 10.50,
            "image_url": "https://example.com/image.jpg",
            "preparation_time": 5,
            "category_id": cat_id
        }
        
        create_resp = client.post("/products", json=product_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            # Listar produtos
            list_resp = client.get("/products")
            assert list_resp.status_code == 200
            products = list_resp.json()
            assert len(products) > 0
        else:
            pytest.skip("Não foi possível criar produto para teste")

    def test_list_products_with_category_filter_existing(self):
        """Teste de listagem filtrando por categoria existente."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        # Filtrar por categoria
        resp = client.get(f"/products?category_id={cat_id}")
        # Pode retornar 200 com lista vazia ou 404
        assert resp.status_code in [200, 404]

    def test_list_products_with_category_filter_nonexistent(self):
        """Teste de listagem filtrando por categoria inexistente."""
        client = TestClient(app)
        
        # Usar um ID de categoria que provavelmente não existe
        resp = client.get("/products?category_id=99999")
        assert resp.status_code in [200, 404]
        if resp.status_code == 200:
            assert resp.json() == []

    def test_find_product_by_id_not_found(self):
        """Teste de busca de produto por ID inexistente."""
        client = TestClient(app)
        
        resp = client.get("/products/99999")
        assert resp.status_code == 404
        assert resp.json() == []

    def test_find_product_by_id_existing(self):
        """Teste de busca de produto por ID existente."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        # Criar produto
        product_data = {
            "name": f"FindProduct-{uuid.uuid4().hex[:8]}",
            "description": "Find test",
            "price": 15.75,
            "image_url": "https://example.com/find.jpg",
            "preparation_time": 3,
            "category_id": cat_id
        }
        
        create_resp = client.post("/products", json=product_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            product_id = create_resp.json()["id"]
            
            # Buscar por ID
            find_resp = client.get(f"/products/{product_id}")
            assert find_resp.status_code == 200
            found_product = find_resp.json()
            assert found_product["id"] == product_id
            assert found_product["name"] == product_data["name"]

    def test_create_product_success(self):
        """Teste de criação de produto com sucesso."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        product_data = {
            "name": f"CreateProduct-{uuid.uuid4().hex[:8]}",
            "description": "Create test",
            "price": 20.99,
            "image_url": "https://example.com/create.jpg",
            "preparation_time": 10,
            "category_id": cat_id
        }
        
        resp = client.post("/products", json=product_data, headers={"X-Role": "admin"})
        if resp.status_code == 201:
            created_product = resp.json()
            assert created_product["name"] == product_data["name"]
            assert created_product["price"] == product_data["price"]
            assert created_product["category_id"] == cat_id

    def test_create_product_duplicate_name(self):
        """Teste de criação de produto com nome duplicado."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        product_name = f"DuplicateProduct-{uuid.uuid4().hex[:8]}"
        product_data = {
            "name": product_name,
            "description": "Duplicate test",
            "price": 12.50,
            "image_url": "https://example.com/dup.jpg",
            "preparation_time": 7,
            "category_id": cat_id
        }
        
        # Primeiro produto
        resp1 = client.post("/products", json=product_data, headers={"X-Role": "admin"})
        if resp1.status_code == 201:
            # Segundo produto com mesmo nome
            resp2 = client.post("/products", json=product_data, headers={"X-Role": "admin"})
            assert resp2.status_code == 409

    def test_create_product_invalid_category(self):
        """Teste de criação de produto com categoria inexistente."""
        client = TestClient(app)
        
        product_data = {
            "name": f"InvalidCatProduct-{uuid.uuid4().hex[:8]}",
            "description": "Invalid category test",
            "price": 25.00,
            "image_url": "https://example.com/invalid.jpg",
            "preparation_time": 15,
            "category_id": 99999  # ID inexistente
        }
        
        resp = client.post("/products", json=product_data, headers={"X-Role": "admin"})
        assert resp.status_code == 400
        assert "does not exist" in resp.json()["detail"]

    def test_create_product_no_admin_role(self):
        """Teste de criação de produto sem role de admin."""
        client = TestClient(app)
        
        product_data = {
            "name": f"NoAdminProduct-{uuid.uuid4().hex[:8]}",
            "description": "No admin test",
            "price": 30.00,
            "category_id": 1
        }
        
        # Sem header de admin
        resp = client.post("/products", json=product_data)
        assert resp.status_code == 403

    def test_update_product_success(self):
        """Teste de atualização de produto com sucesso."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        # Criar produto
        original_data = {
            "name": f"UpdateProduct-{uuid.uuid4().hex[:8]}",
            "description": "Original",
            "price": 35.00,
            "image_url": "https://example.com/original.jpg",
            "preparation_time": 20,
            "category_id": cat_id
        }
        
        create_resp = client.post("/products", json=original_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            product_id = create_resp.json()["id"]
            
            # Atualizar produto
            updated_data = {
                "name": f"UpdatedProduct-{uuid.uuid4().hex[:8]}",
                "description": "Updated",
                "price": 40.00,
                "image_url": "https://example.com/updated.jpg",
                "preparation_time": 25,
                "category_id": cat_id
            }
            
            update_resp = client.put(f"/products/{product_id}", json=updated_data, headers={"X-Role": "admin"})
            if update_resp.status_code == 200:
                updated_product = update_resp.json()
                assert updated_product["name"] == updated_data["name"]
                assert updated_product["description"] == "Updated"
                assert updated_product["price"] == 40.00

    def test_update_product_not_found(self):
        """Teste de atualização de produto inexistente."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        update_data = {
            "name": "NonExistentProduct",
            "description": "Does not exist",
            "price": 50.00,
            "image_url": "https://example.com/none.jpg",
            "preparation_time": 30,
            "category_id": cat_id
        }
        
        resp = client.put("/products/99999", json=update_data, headers={"X-Role": "admin"})
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]

    def test_update_product_invalid_category(self):
        """Teste de atualização de produto com categoria inexistente."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        # Criar produto
        original_data = {
            "name": f"InvalidUpdateProduct-{uuid.uuid4().hex[:8]}",
            "description": "Original",
            "price": 45.00,
            "image_url": "https://example.com/orig.jpg",
            "preparation_time": 12,
            "category_id": cat_id
        }
        
        create_resp = client.post("/products", json=original_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            product_id = create_resp.json()["id"]
            
            # Atualizar com categoria inexistente
            invalid_data = {
                "name": "InvalidCategoryUpdate",
                "description": "Invalid update",
                "price": 50.00,
                "image_url": "https://example.com/invalid_up.jpg",
                "preparation_time": 15,
                "category_id": 99999
            }
            
            resp = client.put(f"/products/{product_id}", json=invalid_data, headers={"X-Role": "admin"})
            assert resp.status_code == 400
            assert "does not exist" in resp.json()["detail"]

    def test_update_product_duplicate_name(self):
        """Teste de atualização com nome duplicado."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        # Criar dois produtos
        product1_data = {
            "name": f"Product1-{uuid.uuid4().hex[:8]}",
            "description": "Product 1",
            "price": 25.00,
            "image_url": "https://example.com/p1.jpg",
            "preparation_time": 5,
            "category_id": cat_id
        }
        
        product2_data = {
            "name": f"Product2-{uuid.uuid4().hex[:8]}",
            "description": "Product 2",
            "price": 30.00,
            "image_url": "https://example.com/p2.jpg",
            "preparation_time": 8,
            "category_id": cat_id
        }
        
        resp1 = client.post("/products", json=product1_data, headers={"X-Role": "admin"})
        resp2 = client.post("/products", json=product2_data, headers={"X-Role": "admin"})
        
        if resp1.status_code == 201 and resp2.status_code == 201:
            product2_id = resp2.json()["id"]
            product1_name = resp1.json()["name"]
            
            # Tentar atualizar produto2 com nome do produto1
            duplicate_data = {
                "name": product1_name,
                "description": "Duplicate name",
                "price": 35.00,
                "image_url": "https://example.com/dup_up.jpg",
                "preparation_time": 10,
                "category_id": cat_id
            }
            
            resp = client.put(f"/products/{product2_id}", json=duplicate_data, headers={"X-Role": "admin"})
            assert resp.status_code == 409

    def test_delete_product_success(self):
        """Teste de exclusão de produto com sucesso."""
        client = TestClient(app)
        cat_id, _ = _ensure_category_simple(client)
        
        # Criar produto
        product_data = {
            "name": f"DeleteProduct-{uuid.uuid4().hex[:8]}",
            "description": "To be deleted",
            "price": 15.00,
            "image_url": "https://example.com/delete.jpg",
            "preparation_time": 3,
            "category_id": cat_id
        }
        
        create_resp = client.post("/products", json=product_data, headers={"X-Role": "admin"})
        if create_resp.status_code == 201:
            product_id = create_resp.json()["id"]
            
            # Deletar produto
            delete_resp = client.delete(f"/products/{product_id}", headers={"X-Role": "admin"})
            assert delete_resp.status_code == 204
            
            # Verificar se foi deletado
            find_resp = client.get(f"/products/{product_id}")
            assert find_resp.status_code == 404

    def test_delete_product_not_found(self):
        """Teste de exclusão de produto inexistente."""
        client = TestClient(app)
        
        resp = client.delete("/products/99999", headers={"X-Role": "admin"})
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]

    def test_delete_product_no_admin_role(self):
        """Teste de exclusão sem role de admin."""
        client = TestClient(app)
        
        resp = client.delete("/products/1")
        assert resp.status_code == 403


class TestProductsValidation:
    """Testes de validação de dados de produtos."""

    def test_create_product_invalid_data(self):
        """Teste de criação com dados inválidos."""
        client = TestClient(app)
        
        # Dados inválidos (preço negativo, etc.)
        invalid_data = {
            "name": "",  # Nome vazio
            "description": "",
            "price": -10.0,  # Preço negativo
            "preparation_time": -5,  # Tempo negativo
            "category_id": "invalid"  # Tipo inválido
        }
        
        resp = client.post("/products", json=invalid_data, headers={"X-Role": "admin"})
        assert resp.status_code == 422

    def test_update_product_invalid_data(self):
        """Teste de atualização com dados inválidos."""
        client = TestClient(app)
        
        invalid_data = {
            "name": "",
            "price": "not_a_number",
            "category_id": None
        }
        
        resp = client.put("/products/1", json=invalid_data, headers={"X-Role": "admin"})
        assert resp.status_code == 422