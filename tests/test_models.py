"""Testes básicos para os modelos de dados."""
import pytest
from app.models import Category, Product


def test_category_model_attributes():
    """Teste de atributos do modelo Category."""
    # Teste apenas instanciação sem salvar no banco
    category = Category(
        name="Test Category",
        description="Test description"
    )
    
    assert category.name == "Test Category"
    assert category.description == "Test description"
    assert hasattr(category, 'id')
    assert hasattr(category, 'created_at')
    assert hasattr(category, 'updated_at')
    assert hasattr(category, 'products')


def test_category_model_without_description():
    """Teste de categoria sem descrição."""
    category = Category(name="No Description Category")
    
    assert category.name == "No Description Category"
    assert category.description is None


def test_product_model_attributes():
    """Teste de atributos do modelo Product."""
    from decimal import Decimal
    
    # Teste apenas instanciação sem salvar no banco
    product = Product(
        name="Test Product",
        description="Test description",
        price=Decimal("19.99"),
        image_url="http://example.com/image.jpg",
        preparation_time=15,
        category_id=1
    )
    
    assert product.name == "Test Product"
    assert product.description == "Test description"
    assert product.price == Decimal("19.99")
    assert product.image_url == "http://example.com/image.jpg"
    assert product.preparation_time == 15
    assert product.category_id == 1
    assert hasattr(product, 'id')
    assert hasattr(product, 'created_at')
    assert hasattr(product, 'updated_at')
    assert hasattr(product, 'category')


def test_product_model_without_optional_fields():
    """Teste de produto sem campos opcionais."""
    from decimal import Decimal
    
    product = Product(
        name="Minimal Product",
        price=Decimal("9.99"),
        preparation_time=5,
        category_id=1
    )
    
    assert product.description is None
    assert product.image_url is None
    assert product.name == "Minimal Product"


def test_category_table_name():
    """Teste do nome da tabela de categorias."""
    assert Category.__tablename__ == "product_categories"


def test_product_table_name():
    """Teste do nome da tabela de produtos."""
    assert Product.__tablename__ == "products"


def test_model_relationships():
    """Teste dos relacionamentos entre modelos."""
    # Verifica se os relacionamentos estão definidos
    assert hasattr(Category, 'products')
    assert hasattr(Product, 'category')
    
    # Verifica metadata das relações
    category_products_rel = Category.products
    product_category_rel = Product.category
    
    assert category_products_rel is not None
    assert product_category_rel is not None