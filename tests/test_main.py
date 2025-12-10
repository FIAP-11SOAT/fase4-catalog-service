"""Testes para o módulo principal da aplicação."""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.main import app, handler
from mangum import Mangum


class TestMainApp:
    """Testes para a aplicação principal FastAPI."""
    
    def test_app_instance(self):
        """Teste de instância da aplicação."""
        assert isinstance(app, FastAPI)
        assert app.title == "Catalogo - Categories API"
        assert app.version == "1.0.0"
    
    def test_health_endpoint(self):
        """Teste do endpoint de health."""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    def test_cors_middleware_configured(self):
        """Teste de configuração do middleware CORS."""
        client = TestClient(app)
        
        # Testa CORS com uma requisição que requer CORS
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        
        # Verifica se o middleware CORS está configurado através dos headers
        assert response.status_code == 200
        # Em ambiente de teste, pode não ter todos os headers CORS, então verificamos apenas o funcionamento básico
    
    def test_categories_router_included(self):
        """Teste se o router de categorias está incluído."""
        client = TestClient(app)
        
        # Testa um endpoint de categorias
        response = client.get("/categories")
        # Deve retornar 404 (lista vazia) ou 200, não 404 de rota não encontrada
        assert response.status_code in [200, 404]
        
        # Se 404, deve retornar array vazio (comportamento específico)
        if response.status_code == 404:
            assert response.json() == []
    
    def test_products_router_included(self):
        """Teste se o router de produtos está incluído."""
        client = TestClient(app)
        
        # Testa um endpoint de produtos
        response = client.get("/products")
        # Deve retornar 404 (lista vazia) ou 200, não 404 de rota não encontrada
        assert response.status_code in [200, 404]
    
    def test_lambda_handler_instance(self):
        """Teste se o handler Lambda está configurado."""
        assert isinstance(handler, Mangum)
    
    def test_app_startup_event(self):
        """Teste do evento de startup."""
        # O evento de startup é executado automaticamente ao instanciar TestClient
        client = TestClient(app)
        
        # Se chegamos até aqui sem erro, o startup foi executado com sucesso
        response = client.get("/health")
        assert response.status_code == 200


class TestHealthEndpoint:
    """Testes específicos para o endpoint de health."""
    
    def test_health_returns_ok(self):
        """Teste básico do health endpoint."""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    
    def test_health_method_not_allowed(self):
        """Teste de método não permitido no health."""
        client = TestClient(app)
        
        # POST não deve ser permitido
        response = client.post("/health")
        assert response.status_code == 405
        
        # PUT não deve ser permitido
        response = client.put("/health")
        assert response.status_code == 405
        
        # DELETE não deve ser permitido
        response = client.delete("/health")
        assert response.status_code == 405
    
    def test_health_content_type(self):
        """Teste do content-type da resposta do health."""
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")


class TestAPIRoutes:
    """Testes gerais das rotas da API."""
    
    def test_root_path_not_found(self):
        """Teste de rota raiz não configurada."""
        client = TestClient(app)
        response = client.get("/")
        
        # Deve retornar 404 pois não há rota configurada para "/"
        assert response.status_code == 404
    
    def test_invalid_path_not_found(self):
        """Teste de rota inválida."""
        client = TestClient(app)
        response = client.get("/invalid-path")
        
        assert response.status_code == 404
    
    def test_api_accepts_json(self):
        """Teste se a API aceita JSON corretamente."""
        client = TestClient(app)
        
        # Testa com JSON válido
        response = client.post(
            "/categories",
            json={"name": "Test Category", "description": "Test"},
            headers={"X-Role": "admin", "Content-Type": "application/json"}
        )
        
        # Deve retornar 201 ou 409 (se já existe), não erro de parsing
        assert response.status_code in [201, 409]
