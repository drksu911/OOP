import pytest

from src.category import Category
from src.product import Product


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)


@pytest.fixture
def sample_category(sample_product):
    return Category("Test Category", "Test Description", [sample_product])


# Старые тесты
def test_category_initialization(sample_category, sample_product):
    assert sample_category.name == "Test Category"
    assert sample_category.description == "Test Description"
    assert sample_category.products_list == [sample_product]


def test_category_count():
    initial_count = Category.category_count
    category = Category("New Category", "Description", [])
    assert Category.category_count == initial_count + 1
    assert category.name == "New Category"


def test_product_count(sample_product):
    initial_count = Category.product_count
    category = Category("New Category", "Description", [sample_product])
    assert Category.product_count == initial_count + 1
    assert len(category.products_list) == 1


def test_empty_category():
    category = Category("Empty Category", "No products", [])
    assert len(category.products_list) == 0
    assert category.name == "Empty Category"


# Новые тесты для приватного атрибута и методов
def test_private_products_attribute(sample_category):
    """Тест приватного атрибута продуктов"""
    # Проверяем, что атрибут действительно приватный
    with pytest.raises(AttributeError):
        _ = sample_category.__products


def test_add_product_method():
    """Тест метода добавления продукта"""
    product1 = Product("Product1", "Desc1", 100, 5)
    product2 = Product("Product2", "Desc2", 200, 10)
    category = Category("Test Category", "Desc", [product1])

    initial_count = Category.product_count
    category.add_product(product2)

    # Проверяем, что продукт добавлен и счетчик увеличился
    assert Category.product_count == initial_count + 1
    products_str = category.products
    assert "Product2" in products_str


def test_products_property_format():
    """Тест геттера продуктов с правильным форматом"""
    product = Product("Test Product", "Test Description", 100.0, 10)
    category = Category("Test Category", "Test Description", [product])

    products_str = category.products
    expected_format = (
        f"{product.name}, {product.price} руб. "
        f"Остаток: {product.quantity} шт."
    )
    assert products_str == expected_format


def test_products_property_multiple_products():
    """Тест геттера продуктов с несколькими товарами"""
    product1 = Product("Product1", "Desc1", 100.0, 10)
    product2 = Product("Product2", "Desc2", 50.0, 5)
    category = Category("Test Category", "Desc", [product1])
    category.add_product(product2)

    products_str = category.products
    # Должны быть оба продукта
    assert product1.name in products_str
    assert product2.name in products_str
    # Проверяем, что строки разделены переводом строки
    lines = products_str.split('\n')
    assert len(lines) == 2
    assert lines[0] == f"{product1.name}, {product1.price} руб. Остаток: {product1.quantity} шт."
    assert lines[1] == f"{product2.name}, {product2.price} руб. Остаток: {product2.quantity} шт."


def test_products_list_property(sample_category, sample_product):
    """Тест геттера products_list для получения объектов"""
    products_list = sample_category.products_list
    assert products_list == [sample_product]
    assert isinstance(products_list[0], Product)
