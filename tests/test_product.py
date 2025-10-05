import pytest

from src.product import Product


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)


def test_product_initialization(sample_product):
    assert sample_product.name == "Test Product"
    assert sample_product.description == "Test Description"
    assert sample_product.price == 100.0
    assert sample_product.quantity == 10


def test_product_attributes():
    product = Product("Phone", "Smartphone", 500.0, 5)
    assert product.name == "Phone"
    assert product.description == "Smartphone"
    assert product.price == 500.0
    assert product.quantity == 5
