import pytest

from src.category import Category
from src.product import Product


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)


@pytest.fixture
def sample_category(sample_product):
    return Category("Test Category", "Test Description", [sample_product])


# Тесты инициализации и базовой функциональности
def test_category_initialization(sample_category, sample_product):
    """Тест инициализации категории"""
    assert sample_category.name == "Test Category"
    assert sample_category.description == "Test Description"
    assert sample_category.products_list == [sample_product]


def test_category_count():
    """Тест подсчета количества категорий"""
    initial_count = Category.category_count
    category = Category("New Category", "Description", [])
    assert Category.category_count == initial_count + 1
    assert category.name == "New Category"


def test_product_count(sample_product):
    """Тест подсчета количества продуктов"""
    initial_count = Category.product_count
    category = Category("New Category", "Description", [sample_product])
    assert Category.product_count == initial_count + 1
    assert len(category.products_list) == 1


def test_empty_category():
    """Тест пустой категории"""
    category = Category("Empty Category", "No products", [])
    assert len(category.products_list) == 0
    assert category.name == "Empty Category"


# Тесты приватного атрибута и методов доступа
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


def test_products_property_format(sample_category, sample_product):
    """Тест геттера продуктов с правильным форматом"""
    products_str = sample_category.products
    expected_format = (
        f"{sample_product.name}, {sample_product.price} руб. "
        f"Остаток: {sample_product.quantity} шт.\n"
    )
    assert products_str == expected_format


def test_products_property_multiple_products():
    """Тест геттера продуктов с несколькими товарами"""
    product1 = Product("Product1", "Desc1", 100.0, 10)
    product2 = Product("Product2", "Desc2", 50.0, 5)
    category = Category("Test Category", "Desc", [product1])
    category.add_product(product2)

    products_str = category.products
    expected = (
        f"{product1.name}, {product1.price} руб. Остаток: {product1.quantity} шт.\n"
        f"{product2.name}, {product2.price} руб. Остаток: {product2.quantity} шт.\n"
    )
    assert products_str == expected


def test_products_property_empty_category():
    """Тест геттера продуктов для пустой категории"""
    category = Category("Empty Category", "No products", [])
    products_str = category.products
    assert products_str == ""


def test_products_format_strict():
    """Строгая проверка формата вывода"""
    product = Product("iPhone", "Smartphone", 999.99, 5)
    category = Category("Phones", "Mobile phones", [product])

    output = category.products
    expected = "iPhone, 999.99 руб. Остаток: 5 шт.\n"

    # Проверяем точное соответствие формату
    assert output == expected
    # Проверяем наличие ключевых элементов в выводе
    assert product.name in output
    assert f"{product.price} руб." in output
    assert f"Остаток: {product.quantity} шт." in output
    assert output.endswith("\n")  # Обязательный перенос строки


def test_products_list_property(sample_category, sample_product):
    """Тест геттера products_list для получения объектов"""
    products_list = sample_category.products_list
    assert products_list == [sample_product]
    assert isinstance(products_list[0], Product)


def test_add_product_increases_count():
    """Тест, что добавление продукта увеличивает счетчик"""
    initial_count = Category.product_count
    product = Product("New Product", "Description", 100.0, 5)
    category = Category("Test Category", "Description", [])

    category.add_product(product)
    assert Category.product_count == initial_count + 1


def test_category_count_multiple_instances():
    """Тест счетчика категорий для нескольких экземпляров"""
    initial_count = Category.category_count
    category1 = Category("Category1", "Desc1", [])
    category2 = Category("Category2", "Desc2", [])

    assert Category.category_count == initial_count + 2
    assert category1.name == "Category1"
    assert category2.name == "Category2"


def test_product_count_with_multiple_products():
    """Тест счетчика продуктов для нескольких товаров"""
    initial_count = Category.product_count
    product1 = Product("Product1", "Desc1", 100.0, 1)
    product2 = Product("Product2", "Desc2", 200.0, 2)
    product3 = Product("Product3", "Desc3", 300.0, 3)

    category = Category("Test Category", "Description", [product1, product2])
    category.add_product(product3)

    assert Category.product_count == initial_count + 3


def test_products_property_after_removal():
    """Тест геттера продуктов после изменения списка"""
    product1 = Product("Product1", "Desc1", 100.0, 10)
    product2 = Product("Product2", "Desc2", 200.0, 20)
    category = Category("Test Category", "Description", [product1, product2])

    # Симулируем удаление продукта (в реальности нужно будет добавить метод remove)
    category._Category__products = [product1]  # Прямой доступ к приватному атрибуту для теста

    products_str = category.products
    expected = f"{product1.name}, {product1.price} руб. Остаток: {product1.quantity} шт.\n"
    assert products_str == expected


def test_products_property_special_characters():
    """Тест геттера продуктов с особыми символами в названии"""
    product = Product("Product & Co.", "Description with % symbols", 123.45, 7)
    category = Category("Special Category", "Desc", [product])

    output = category.products
    expected = "Product & Co., 123.45 руб. Остаток: 7 шт.\n"
    assert output == expected


def test_products_property_zero_quantity():
    """Тест геттера продуктов с нулевым количеством"""
    product = Product("Out of Stock", "No items", 100.0, 0)
    category = Category("Test Category", "Desc", [product])

    output = category.products
    expected = "Out of Stock, 100.0 руб. Остаток: 0 шт.\n"
    assert output == expected


def test_products_property_high_price():
    """Тест геттера продуктов с высокой ценой"""
    product = Product("Expensive Item", "Luxury", 999999.99, 1)
    category = Category("Luxury Category", "Desc", [product])

    output = category.products
    expected = "Expensive Item, 999999.99 руб. Остаток: 1 шт.\n"
    assert output == expected
