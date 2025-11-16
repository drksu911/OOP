import pytest

from src.product import Product


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)


# Старые тесты
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


# Новые тесты для приватной цены и класс-методов
def test_private_price_attribute(sample_product):
    """Тест приватного атрибута цены"""
    with pytest.raises(AttributeError):
        _ = sample_product.__price


def test_price_property(sample_product):
    """Тест геттера и сеттера цены"""
    assert sample_product.price == 100.0
    sample_product.price = 150.0
    assert sample_product.price == 150.0


def test_price_validation_negative(sample_product, capsys):
    """Тест валидации отрицательной цены"""
    sample_product.price = -50
    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"
    assert sample_product.price == 100.0  # Цена не изменилась


def test_price_validation_zero(sample_product, capsys):
    """Тест валидации нулевой цены"""
    sample_product.price = 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "Цена не должна быть нулевая или отрицательная"
    assert sample_product.price == 100.0  # Цена не изменилась


def test_new_product_class_method():
    """Тест класс-метода создания продукта"""
    product_data = {
        "name": "New Product",
        "description": "New Description",
        "price": 200.0,
        "quantity": 10,
    }

    product = Product.new_product(product_data)

    assert product.name == "New Product"
    assert product.description == "New Description"
    assert product.price == 200.0
    assert product.quantity == 10


def test_new_product_with_duplicate_check():
    """Тест проверки дубликатов"""
    existing_product = Product("Existing Product", "Description", 100.0, 5)
    existing_products = [existing_product]

    duplicate_data = {
        "name": "Existing Product",
        "description": "New Description",
        "price": 150.0,  # Более высокая цена
        "quantity": 3,
    }

    result = Product.new_product_with_duplicate_check(duplicate_data, existing_products)

    # Должен вернуться существующий продукт с обновленными значениями
    assert result is existing_product
    assert result.quantity == 8  # 5 + 3
    assert result.price == 150.0  # Максимальная цена


def test_new_product_with_duplicate_check_new_product():
    """Тест проверки дубликатов для нового продукта"""
    existing_product = Product("Existing Product", "Description", 100.0, 5)
    existing_products = [existing_product]

    new_product_data = {
        "name": "New Product",
        "description": "New Description",
        "price": 200.0,
        "quantity": 10,
    }

    result = Product.new_product_with_duplicate_check(
        new_product_data, existing_products
    )

    # Должен вернуться новый продукт
    assert result is not existing_product
    assert result.name == "New Product"
    assert result.quantity == 10
    assert result.price == 200.0


def test_product_str_method():
    """Тест строкового представления продукта"""
    product = Product("Test Product", "Description", 100.0, 5)
    expected = "Test Product, 100.0 руб. Остаток: 5 шт."
    assert str(product) == expected


def test_product_addition():
    """Тест сложения продуктов"""
    product1 = Product("Product1", "Desc1", 100.0, 2)
    product2 = Product("Product2", "Desc2", 200.0, 3)

    result = product1 + product2
    expected = (100.0 * 2) + (200.0 * 3)
    assert result == expected


def test_product_addition_with_zero_quantity():
    """Тест сложения продуктов с нулевым количеством"""
    product1 = Product("Product1", "Desc1", 100.0, 0)
    product2 = Product("Product2", "Desc2", 200.0, 5)

    result = product1 + product2
    expected = (100.0 * 0) + (200.0 * 5)
    assert result == expected


def test_product_addition_different_classes_error():
    """Тест ошибки при сложении продуктов разных классов"""
    product = Product("Product", "Desc", 100.0, 2)

    # Создаем мок-объект другого класса
    class OtherClass:
        pass

    other = OtherClass()

    with pytest.raises(
        TypeError, match="Можно складывать только объекты одинаковых классов"
    ):
        product + other
