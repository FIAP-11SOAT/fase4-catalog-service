"""Testes para os schemas do Pydantic."""
import pytest
from datetime import datetime
from decimal import Decimal
from pydantic import ValidationError
from app.schemas import CategoryInput, CategoryResponse, ProductInput, ProductResponse


class TestCategoryInput:
    """Testes para o schema CategoryInput."""
    
    def test_valid_category_input(self):
        """Teste de entrada válida para categoria."""
        data = {
            "name": "Test Category",
            "description": "Test description"
        }
        category = CategoryInput(**data)
        
        assert category.name == "Test Category"
        assert category.description == "Test description"
    
    def test_category_input_without_description(self):
        """Teste de categoria sem descrição."""
        data = {"name": "Test Category"}
        category = CategoryInput(**data)
        
        assert category.name == "Test Category"
        assert category.description is None
    
    def test_category_input_empty_name(self):
        """Teste de categoria com nome vazio deve falhar."""
        with pytest.raises(ValidationError):
            CategoryInput(name="")
    
    def test_category_input_name_too_long(self):
        """Teste de categoria com nome muito longo."""
        with pytest.raises(ValidationError):
            CategoryInput(name="A" * 101)  # Máximo é 100
    
    def test_category_input_missing_name(self):
        """Teste de categoria sem nome deve falhar."""
        with pytest.raises(ValidationError):
            CategoryInput(description="Test description")


class TestCategoryResponse:
    """Testes para o schema CategoryResponse."""
    
    def test_category_response_creation(self):
        """Teste de criação do response da categoria."""
        now = datetime.now()
        data = {
            "id": 1,
            "name": "Test Category",
            "description": "Test description",
            "created_at": now,
            "updated_at": now
        }
        category = CategoryResponse(**data)
        
        assert category.id == 1
        assert category.name == "Test Category"
        assert category.description == "Test description"
        assert category.created_at == now
        assert category.updated_at == now
    
    def test_category_response_without_description(self):
        """Teste de response da categoria sem descrição."""
        now = datetime.now()
        data = {
            "id": 1,
            "name": "Test Category",
            "created_at": now,
            "updated_at": now
        }
        category = CategoryResponse(**data)
        
        assert category.description is None


class TestProductInput:
    """Testes para o schema ProductInput."""
    
    def test_valid_product_input(self):
        """Teste de entrada válida para produto."""
        data = {
            "name": "Test Product",
            "description": "Test description",
            "price": Decimal("19.99"),
            "image_url": "http://example.com/image.jpg",
            "preparation_time": 15,
            "category_id": 1
        }
        product = ProductInput(**data)
        
        assert product.name == "Test Product"
        assert product.description == "Test description"
        assert product.price == Decimal("19.99")
        assert product.image_url == "http://example.com/image.jpg"
        assert product.preparation_time == 15
        assert product.category_id == 1
    
    def test_product_input_without_optionals(self):
        """Teste de produto sem campos opcionais."""
        data = {
            "name": "Test Product",
            "price": Decimal("19.99"),
            "preparation_time": 15,
            "category_id": 1
        }
        product = ProductInput(**data)
        
        assert product.description is None
        assert product.image_url is None
    
    def test_product_input_empty_name(self):
        """Teste de produto com nome vazio deve falhar."""
        with pytest.raises(ValidationError):
            ProductInput(name="", price=1.23, preparation_time=1, category_id=1)
    
    def test_product_input_name_too_long(self):
        """Teste de produto com nome muito longo."""
        with pytest.raises(ValidationError):
            ProductInput(name="A" * 151, price=1.23, preparation_time=1, category_id=1)
    
    def test_product_input_negative_price(self):
        """Teste de produto com preço negativo deve falhar."""
        with pytest.raises(ValidationError):
            ProductInput(name="P", price=-1, preparation_time=1, category_id=1)
    
    def test_product_input_negative_preparation_time(self):
        """Teste de produto com tempo de preparo negativo deve falhar."""
        with pytest.raises(ValidationError):
            ProductInput(name="P", price=1.23, preparation_time=-1, category_id=1)
    
    def test_product_input_invalid_category_id(self):
        """Teste de produto com category_id inválido deve falhar."""
        with pytest.raises(ValidationError):
            ProductInput(name="P", price=1.23, preparation_time=1, category_id=0)
    
    def test_product_input_image_url_too_long(self):
        """Teste de produto com URL de imagem muito longa."""
        with pytest.raises(ValidationError):
            ProductInput(
                name="Test Product",
                price=Decimal("19.99"),
                preparation_time=15,
                category_id=1,
                image_url="http://example.com/" + "A" * 500
            )
    
    def test_product_input_price_decimal_places(self):
        """Teste de produto com preço com muitas casas decimais deve falhar."""
        with pytest.raises(ValidationError):
            ProductInput(
                name="Test Product",
                price=Decimal("19.999"),  # Máximo 2 casas decimais
                preparation_time=15,
                category_id=1
            )
    
    def test_product_input_missing_required_fields(self):
        """Teste de produto sem campos obrigatórios deve falhar."""
        with pytest.raises(ValidationError):
            ProductInput(name="Test Product")


class TestProductResponse:
    """Testes para o schema ProductResponse."""
    
    def test_product_response_creation(self):
        """Teste de criação do response do produto."""
        now = datetime.now()
        data = {
            "id": 1,
            "name": "Test Product",
            "description": "Test description",
            "price": Decimal("19.99"),
            "image_url": "http://example.com/image.jpg",
            "preparation_time": 15,
            "category_id": 1,
            "created_at": now,
            "updated_at": now
        }
        product = ProductResponse(**data)
        
        assert product.id == 1
        assert product.name == "Test Product"
        assert product.description == "Test description"
        assert product.price == Decimal("19.99")
        assert product.image_url == "http://example.com/image.jpg"
        assert product.preparation_time == 15
        assert product.category_id == 1
        assert product.created_at == now
        assert product.updated_at == now
    
    def test_product_response_without_optionals(self):
        """Teste de response do produto sem campos opcionais."""
        now = datetime.now()
        data = {
            "id": 1,
            "name": "Test Product",
            "price": Decimal("19.99"),
            "preparation_time": 15,
            "category_id": 1,
            "created_at": now,
            "updated_at": now
        }
        product = ProductResponse(**data)
        
        assert product.description is None
        assert product.image_url is None
