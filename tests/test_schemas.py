import pytest
from pydantic import ValidationError
from app.schemas import CategoryInput, ProductInput


def test_category_input_validation():
    CategoryInput(name="A")
    with pytest.raises(ValidationError):
        CategoryInput(name="")


def test_product_input_validation():
    ProductInput(name="P", description=None, price=1.23, image_url=None, preparation_time=1, category_id=1)
    with pytest.raises(ValidationError):
        ProductInput(name="", description=None, price=1.23, image_url=None, preparation_time=1, category_id=1)
    with pytest.raises(ValidationError):
        ProductInput(name="P", description=None, price=-1, image_url=None, preparation_time=1, category_id=1)
    with pytest.raises(ValidationError):
        ProductInput(name="P", description=None, price=1.23, image_url=None, preparation_time=-1, category_id=1)
    with pytest.raises(ValidationError):
        ProductInput(name="P", description=None, price=1.23, image_url=None, preparation_time=1, category_id=0)
