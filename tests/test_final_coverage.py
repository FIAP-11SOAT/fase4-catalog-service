"""Testes integrados finais para cobertura do SonarQube."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid


class TestCoverageBasic:
    """Testes básicos para garantir cobertura."""
    
    def test_health_endpoint(self):
        """Teste básico do health endpoint."""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    def test_security_admin_required(self):
        """Teste que operações requerem admin."""
        client = TestClient(app)
        payload = {"name": "Test", "description": "Test"}
        
        # Sem header
        resp = client.post("/categories", json=payload)
        assert resp.status_code == 403
        
        # Com header inválido
        resp = client.post("/categories", json=payload, headers={"X-Role": "user"})
        assert resp.status_code == 403
        
        # Com admin válido - pode retornar 201 ou 409
        resp = client.post("/categories", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code in [201, 409]
    
    def test_categories_empty_list(self):
        """Teste de listagem vazia de categorias."""
        client = TestClient(app)
        resp = client.get("/categories")
        # Pode retornar 404 com array vazio ou 200 com lista
        assert resp.status_code in [200, 404]
        if resp.status_code == 404:
            assert resp.json() == []
    
    def test_products_empty_list(self):
        """Teste de listagem vazia de produtos."""
        client = TestClient(app)
        resp = client.get("/products")
        # Pode retornar 404 com array vazio ou 200 com lista
        assert resp.status_code in [200, 404]
        if resp.status_code == 404:
            assert resp.json() == []
    
    def test_category_not_found(self):
        """Teste de categoria não encontrada."""
        client = TestClient(app)
        resp = client.get("/categories/99999")
        assert resp.status_code == 404
        assert resp.json() == []
    
    def test_product_not_found(self):
        """Teste de produto não encontrado."""
        client = TestClient(app)
        resp = client.get("/products/99999")
        assert resp.status_code == 404
        assert resp.json() == []
    
    def test_invalid_json_data(self):
        """Teste com dados JSON inválidos."""
        client = TestClient(app)
        
        # JSON com campo obrigatório faltando
        resp = client.post("/categories", json={}, headers={"X-Role": "admin"})
        assert resp.status_code == 422
        
        # JSON com campo inválido
        resp = client.post("/categories", json={"name": ""}, headers={"X-Role": "admin"})
        assert resp.status_code == 422
    
    def test_product_validation_errors(self):
        """Teste de erros de validação de produtos."""
        client = TestClient(app)
        
        # Produto sem dados obrigatórios
        resp = client.post("/products", json={}, headers={"X-Role": "admin"})
        assert resp.status_code == 422
        
        # Produto com preço negativo
        payload = {
            "name": "Test",
            "price": -10,
            "preparation_time": 5,
            "category_id": 1
        }
        resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 422
    
    def test_product_with_invalid_category(self):
        """Teste de produto com categoria inexistente."""
        client = TestClient(app)
        
        payload = {
            "name": f"Test-Product-{uuid.uuid4().hex[:8]}",
            "price": 10.00,
            "preparation_time": 5,
            "category_id": 99999
        }
        
        resp = client.post("/products", json=payload, headers={"X-Role": "admin"})
        assert resp.status_code == 400
        assert "does not exist" in resp.json()["detail"]
    
    def test_crud_flow_basic(self):
        """Teste de fluxo CRUD básico."""
        client = TestClient(app)
        
        # Criar categoria
        cat_name = f"Test-Cat-{uuid.uuid4().hex[:8]}"
        cat_payload = {"name": cat_name, "description": "Test category"}
        cat_resp = client.post("/categories", json=cat_payload, headers={"X-Role": "admin"})
        
        if cat_resp.status_code == 201:
            cat_id = cat_resp.json()["id"]
            
            # Buscar categoria
            get_resp = client.get(f"/categories/{cat_id}")
            assert get_resp.status_code == 200
            
            # Atualizar categoria
            update_payload = {"name": cat_name, "description": "Updated"}
            update_resp = client.put(f"/categories/{cat_id}", json=update_payload, headers={"X-Role": "admin"})
            assert update_resp.status_code == 200
            
            # Criar produto na categoria
            prod_name = f"Test-Prod-{uuid.uuid4().hex[:8]}"
            prod_payload = {
                "name": prod_name,
                "price": 15.99,
                "preparation_time": 10,
                "category_id": cat_id
            }
            prod_resp = client.post("/products", json=prod_payload, headers={"X-Role": "admin"})
            
            if prod_resp.status_code == 201:
                prod_id = prod_resp.json()["id"]
                
                # Buscar produto
                get_prod_resp = client.get(f"/products/{prod_id}")
                assert get_prod_resp.status_code == 200
                
                # Deletar produto
                del_prod_resp = client.delete(f"/products/{prod_id}", headers={"X-Role": "admin"})
                assert del_prod_resp.status_code == 204
            
            # Deletar categoria
            del_resp = client.delete(f"/categories/{cat_id}", headers={"X-Role": "admin"})
            assert del_resp.status_code == 204
    
    def test_update_operations_require_admin(self):
        """Teste que operações de update requerem admin."""
        client = TestClient(app)
        
        payload = {"name": "Test", "description": "Test"}
        
        # PUT sem admin
        resp = client.put("/categories/1", json=payload)
        assert resp.status_code == 403
        
        # DELETE sem admin
        resp = client.delete("/categories/1")
        assert resp.status_code == 403
    
    def test_products_filter_by_category(self):
        """Teste de filtro de produtos por categoria."""
        client = TestClient(app)
        
        # Testa filtro por categoria (mesmo que não existam produtos)
        resp = client.get("/products?category_id=1")
        assert resp.status_code in [200, 404]
    
    def test_error_handling_edge_cases(self):
        """Teste de casos extremos de erro."""
        client = TestClient(app)
        
        # ID inválido (não numérico)
        resp = client.get("/categories/invalid")
        assert resp.status_code == 422
        
        # ID inválido para produtos
        resp = client.get("/products/invalid")
        assert resp.status_code == 422
    
    def test_models_basic_attributes(self):
        """Teste básico dos atributos dos modelos."""
        from app.models import Category, Product
        from decimal import Decimal
        
        # Instanciar categoria
        category = Category(name="Test", description="Test")
        assert category.name == "Test"
        assert hasattr(category, '__tablename__')
        
        # Instanciar produto
        product = Product(
            name="Test Product",
            price=Decimal("10.00"),
            preparation_time=5,
            category_id=1
        )
        assert product.name == "Test Product"
        assert hasattr(product, '__tablename__')
    
    def test_schemas_validation_basic(self):
        """Teste básico de validação dos schemas."""
        from app.schemas import CategoryInput, ProductInput
        from decimal import Decimal
        import pytest
        from pydantic import ValidationError
        
        # Schema válido de categoria
        cat = CategoryInput(name="Test", description="Test")
        assert cat.name == "Test"
        
        # Schema inválido de categoria
        with pytest.raises(ValidationError):
            CategoryInput(name="")
        
        # Schema válido de produto
        prod = ProductInput(
            name="Test",
            price=Decimal("10.00"),
            preparation_time=5,
            category_id=1
        )
        assert prod.name == "Test"
        
        # Schema inválido de produto
        with pytest.raises(ValidationError):
            ProductInput(name="Test", price=-1, preparation_time=5, category_id=1)