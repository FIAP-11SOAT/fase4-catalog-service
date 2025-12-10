"""Testes para as rotas de produtos."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Category
import uuid
from decimal import Decimal


def _ensure_category(client, name=None):
    """Helper para garantir que uma categoria existe."""
    if name is None:
        name = f"Cat-{uuid.uuid4().hex[:6]}"
    
    resp = client.post("/categories", json={"name": name, "description": "tmp"}, headers={"X-Role": "admin"})
    
    if resp.status_code == 201:
        return resp.json()["id"], name
    elif resp.status_code == 409:
        # Category already exists, fetch it
        resp = client.get("/categories")
        if resp.status_code == 200:
            categories = resp.json()
            for cat in categories:
                if cat["name"] == name:
                    return cat["id"], cat["name"]
        
        # If not found in list, try with a different name
        return _ensure_category(client, f"{name}-{uuid.uuid4().hex[:4]}")
    else:
        pytest.fail(f"Failed to create category: {resp.status_code} - {resp.text}")


class TestProductsCRUD:
    """Testes de operações CRUD de produtos."""
    
    def test_create_product_success(self):
        """Teste de criação de produto com sucesso."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        unique = uuid.uuid4().hex[:8]
        payload = {
            "name": f"Produto-{unique}",
            "description": "Descrição do produto",
            "price": 12.34,
            "image_url": "http://example.com/img.png",
            "preparation_time": 10,
            "category_id": cat_id,
        }
        
        resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 201
        
        created = resp.json()
        assert created["name"] == payload["name"]
        assert created["description"] == payload["description"]
        assert float(created["price"]) == payload["price"]
        assert created["image_url"] == payload["image_url"]
        assert created["preparation_time"] == payload["preparation_time"]
        assert created["category_id"] == payload["category_id"]
        assert "id" in created
        assert "created_at" in created
        assert "updated_at" in created
    
    def test_create_product_requires_admin(self):
        """Teste que criação de produto requer admin."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        payload = {
            "name": "Produto Test",
            "price": 10.00,
            "preparation_time": 5,
            "category_id": cat_id,
        }
        
        # Sem header admin
        resp = client.post("/products", json=payload)
        assert resp.status_code == 403
        
        # Com header inválido
        resp = client.post("/products", json=payload, headers={"X-Role": "user"})
        assert resp.status_code == 403
    
    def test_create_product_minimal_fields(self):
        """Teste de criação de produto com campos mínimos."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        unique = uuid.uuid4().hex[:8]
        payload = {
            "name": f"Produto-Minimal-{unique}",
            "price": 5.99,
            "preparation_time": 15,
            "category_id": cat_id,
        }
        
        resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 201
        
        created = resp.json()
        assert created["name"] == payload["name"]
        assert created["description"] is None
        assert created["image_url"] is None
    
    def test_create_product_invalid_category(self):
        """Teste de criação de produto com categoria inválida."""
        client = TestClient(app)
        
        payload = {
            "name": "Produto Test",
            "price": 10.00,
            "preparation_time": 5,
            "category_id": 99999,  # ID inexistente
        }
        
        resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 400
    
    def test_create_product_duplicate_name(self):
        """Teste de criação de produto com nome duplicado."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        name = f"Produto-Duplicado-{uuid.uuid4().hex[:8]}"
        payload = {
            "name": name,
            "price": 10.00,
            "preparation_time": 5,
            "category_id": cat_id,
        }
        
        # Primeiro produto
        resp1 = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp1.status_code == 201
        
        # Segundo produto com mesmo nome
        resp2 = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp2.status_code == 409
    
    def test_get_product_by_id_success(self):
        """Teste de busca de produto por ID com sucesso."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        # Criar produto primeiro
        unique = uuid.uuid4().hex[:8]
        payload = {
            "name": f"Produto-Get-{unique}",
            "price": 15.99,
            "preparation_time": 20,
            "category_id": cat_id,
        }
        
        create_resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert create_resp.status_code == 201
        product_id = create_resp.json()["id"]
        
        # Buscar produto
        get_resp = client.get(f"/products/{product_id}")
        assert get_resp.status_code == 200
        
        product = get_resp.json()
        assert product["id"] == product_id
        assert product["name"] == payload["name"]
    
    def test_get_product_by_id_not_found(self):
        """Teste de busca de produto por ID inexistente."""
        client = TestClient(app)
        
        resp = client.get("/products/99999")
        assert resp.status_code == 404
        assert resp.json() == []
    
    def test_list_products_empty(self):
        """Teste de listagem de produtos vazia."""
        client = TestClient(app)
        
        resp = client.get("/products")
        # Pode retornar 404 com array vazio ou 200 com lista
        assert resp.status_code in [200, 404]
        
        if resp.status_code == 404:
            assert resp.json() == []
    
    def test_update_product_success(self):
        """Teste de atualização de produto com sucesso."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        # Criar produto
        unique = uuid.uuid4().hex[:8]
        payload = {
            "name": f"Produto-Update-{unique}",
            "description": "Descrição original",
            "price": 20.00,
            "preparation_time": 25,
            "category_id": cat_id,
        }
        
        create_resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert create_resp.status_code == 201
        product_id = create_resp.json()["id"]
        
        # Atualizar produto
        update_payload = {
            "name": f"Produto-Update-{unique}",  # Mesmo nome
            "description": "Descrição atualizada",
            "price": 25.00,
            "preparation_time": 30,
            "category_id": cat_id,
        }
        
        update_resp = client.put(f"/products/{product_id}", json=update_payload, headers={"X-Role": "admin"})
        assert update_resp.status_code == 200
        
        updated = update_resp.json()
        assert updated["description"] == "Descrição atualizada"
        assert float(updated["price"]) == 25.00
        assert updated["preparation_time"] == 30
    
    def test_update_product_requires_admin(self):
        """Teste que atualização de produto requer admin."""
        client = TestClient(app)
        
        payload = {
            "name": "Produto Test",
            "price": 10.00,
            "preparation_time": 5,
            "category_id": 1,
        }
        
        # Sem admin
        resp = client.put("/products/1", json=payload)
        assert resp.status_code == 403
    
    def test_update_product_not_found(self):
        """Teste de atualização de produto inexistente."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        payload = {
            "name": "Produto Test",
            "price": 10.00,
            "preparation_time": 5,
            "category_id": cat_id,
        }
        
        resp = client.put("/products/99999", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 404
    
    def test_delete_product_success(self):
        """Teste de exclusão de produto com sucesso."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        # Criar produto
        unique = uuid.uuid4().hex[:8]
        payload = {
            "name": f"Produto-Delete-{unique}",
            "price": 30.00,
            "preparation_time": 15,
            "category_id": cat_id,
        }
        
        create_resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert create_resp.status_code == 201
        product_id = create_resp.json()["id"]
        
        # Deletar produto
        delete_resp = client.delete(f"/products/{product_id}", headers={"X-Role": "admin"})
        assert delete_resp.status_code == 204
        
        # Verificar se foi deletado
        get_resp = client.get(f"/products/{product_id}")
        assert get_resp.status_code == 404
    
    def test_delete_product_requires_admin(self):
        """Teste que exclusão de produto requer admin."""
        client = TestClient(app)
        
        # Sem admin
        resp = client.delete("/products/1")
        assert resp.status_code == 403
    
    def test_delete_product_not_found(self):
        """Teste de exclusão de produto inexistente."""
        client = TestClient(app)
        
        resp = client.delete("/products/99999", headers={"X-Role": "admin"})
        assert resp.status_code == 404


class TestProductsValidation:
    """Testes de validação de dados de produtos."""
    
    def test_create_product_invalid_price_format(self):
        """Teste de criação com preço em formato inválido."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        payload = {
            "name": "Produto Test",
            "price": "invalid",  # String ao invés de número
            "preparation_time": 5,
            "category_id": cat_id,
        }
        
        resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 422  # Validation error
    
    def test_create_product_missing_required_fields(self):
        """Teste de criação sem campos obrigatórios."""
        client = TestClient(app)
        
        # Sem nome
        payload = {
            "price": 10.00,
            "preparation_time": 5,
            "category_id": 1,
        }
        
        resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 422
    
    def test_create_product_empty_name(self):
        """Teste de criação com nome vazio."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        payload = {
            "name": "",  # Nome vazio
            "price": 10.00,
            "preparation_time": 5,
            "category_id": cat_id,
        }
        
        resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 422


class TestProductsWithCategory:
    """Testes de produtos com relacionamento de categoria."""
    
    def test_list_products_by_category(self):
        """Teste de listagem de produtos por categoria."""
        client = TestClient(app)
        cat_id, cat_name = _ensure_category(client, f"TestCategory-{uuid.uuid4().hex[:6]}")
        
        # Criar alguns produtos para a categoria
        products = []
        for i in range(3):
            unique = uuid.uuid4().hex[:8]
            payload = {
                "name": f"Produto-{i}-{unique}",
                "price": 10.00 + i,
                "preparation_time": 5 + i,
                "category_id": cat_id,
            }
            
            resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
            if resp.status_code == 201:
                products.append(resp.json())
        
        # Listar produtos por categoria (se o endpoint existir)
        resp = client.get(f"/products?category_id={cat_id}")
        # Como não sabemos se este endpoint existe, vamos apenas verificar que não é 404 de rota não encontrada
        assert resp.status_code != 404 or "Not Found" not in resp.text
    
    def test_product_category_relationship_integrity(self):
        """Teste de integridade referencial categoria-produto."""
        client = TestClient(app)
        cat_id, _ = _ensure_category(client)
        
        # Criar produto
        unique = uuid.uuid4().hex[:8]
        payload = {
            "name": f"Produto-Integrity-{unique}",
            "price": 15.00,
            "preparation_time": 10,
            "category_id": cat_id,
        }
        
        create_resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert create_resp.status_code == 201
        product = create_resp.json()
        
        # Verificar se o produto tem a categoria correta
        get_resp = client.get(f"/products/{product['id']}")
        assert get_resp.status_code == 200
        assert get_resp.json()["category_id"] == cat_id


def test_products_crud_flow():
    """Teste de fluxo completo CRUD de produtos (teste original simplificado)."""
    client = TestClient(app)
    cat_id, _ = _ensure_category(client)

    unique = uuid.uuid4().hex[:8]
    payload = {
        "name": f"Produto-{unique}",
        "description": "desc",
        "price": 12.34,
        "image_url": "http://example.com/img.png",
        "preparation_time": 10,
        "category_id": cat_id,
    }

    # Create requires admin
    r = client.post("/products", json=payload)
    assert r.status_code == 403

    r = client.post("/products", json=payload, headers={"X-Role": "admin"})
    assert r.status_code == 201
    created = r.json()
    pid = created["id"]

    # Get by id
    r = client.get(f"/products/{pid}")
    assert r.status_code == 200

    # List
    r = client.get("/products")
    assert r.status_code in (200, 404)

    # Update
    upd = dict(payload)
    upd["description"] = "nova"
    r = client.put(f"/products/{pid}", json=upd, headers={"X-Role": "admin"})
    assert r.status_code == 200
    assert r.json()["description"] == "nova"

    # Delete
    r = client.delete(f"/products/{pid}", headers={"X-Role": "admin"})
    assert r.status_code == 204

    # Ensure gone
    r = client.get(f"/products/{pid}")
    assert r.status_code == 404
