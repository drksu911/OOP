from src.category import Category
from src.product import Product
import pytest

@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)

@pytest.fixture
def sample_category(sample_product):
    return Category("Test Category", "Test Description", [sample_product])

def test_category_initialization(sample_category, sample_product):
    assert sample_category.name == "Test Category"
    assert sample_category.description == "Test Description"
    assert sample_category.products == [sample_product]

def test_category_count():
    initial_count = Category.category_count
    category = Category("New Category", "Description", [])
    assert Category.category_count == initial_count + 1

def test_product_count(sample_product):
    initial_count = Category.product_count
    category = Category("New Category", "Description", [sample_product])
    assert Category.product_count == initial_count + 1

def test_empty_category():
    category = Category("Empty Category", "No products", [])
    assert len(category.products) == 0
