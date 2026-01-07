import sys
from io import StringIO

import pytest

from src.base_product import BaseProduct, LogCreationMixin
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


class TestBaseProduct:
    def test_base_product_is_abstract(self):
        """Тест, что BaseProduct является абстрактным классом"""
        # Нельзя создать экземпляр абстрактного класса
        with pytest.raises(TypeError):
            BaseProduct("Test", "Desc", 100.0, 5)

    def test_product_inherits_from_base_product(self):
        """Тест, что Product наследуется от BaseProduct"""
        product = Product("Test Product", "Description", 100.0, 5)
        assert isinstance(product, BaseProduct)
        assert isinstance(product, LogCreationMixin)

    def test_abstract_methods_implemented(self):
        """Тест, что Product реализует все абстрактные методы"""
        product = Product("Test Product", "Description", 100.0, 5)

        # Проверяем, что методы существуют и работают
        assert str(product) == "Test Product, 100.0 руб. Остаток: 5 шт."
        assert product.price == 100.0

        # Проверяем сложение
        product2 = Product("Test Product 2", "Description 2", 200.0, 3)
        result = product + product2
        assert result == (100.0 * 5) + (200.0 * 3)

        # Проверяем создание из словаря
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 150.0,
            "quantity": 10,
        }
        new_product = Product.new_product(product_data)
        assert new_product.name == "New Product"
        assert new_product.price == 150.0


class TestLogCreationMixin:
    def test_mixin_logs_creation(self):
        """Тест, что миксин логирует создание объектов"""
        # Перехватываем вывод в консоль
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            product = Product("Test Product", "Description", 100.0, 5)

            # Получаем вывод
            output = captured_output.getvalue().strip()

            # Проверяем, что вывод содержит информацию о создании
            assert "Создан объект Product" in output
            assert "'Test Product'" in output
            assert "'Description'" in output
            assert "100.0" in output
            assert "5" in output

            # Используем переменную product, чтобы избежать F841
            _ = product.name
        finally:
            sys.stdout = sys.__stdout__

    def test_mixin_inheritance_chain(self):
        """Тест, что миксин работает в цепочке наследования"""
        # Проверяем, что Product действительно наследует миксин
        assert (
            LogCreationMixin in Product.__bases__ or LogCreationMixin in Product.__mro__
        )

    def test_smartphone_inherits_mixin(self):
        """Тест, что Smartphone наследует миксин через Product"""
        smartphone = Smartphone(
            "Test Phone", "Description", 1000.0, 2, 95.0, "Model X", 256, "Black"
        )

        # Проверяем, что смартфон является экземпляром LogCreationMixin
        assert isinstance(smartphone, LogCreationMixin)

        # Проверяем, что он корректно наследует функциональность
        assert smartphone.name == "Test Phone"
        assert smartphone.model == "Model X"

    def test_lawn_grass_inherits_mixin(self):
        """Тест, что LawnGrass наследует миксин через Product"""
        grass = LawnGrass(
            "Test Grass", "Description", 500.0, 10, "Russia", "7 дней", "Green"
        )

        # Проверяем, что газонная трава является экземпляром LogCreationMixin
        assert isinstance(grass, LogCreationMixin)

        # Проверяем, что он корректно наследует функциональность
        assert grass.name == "Test Grass"
        assert grass.country == "Russia"


class TestMultipleInheritance:
    def test_product_mro(self):
        """Тест порядка разрешения методов (MRO) для Product"""
        mro = Product.__mro__

        # Проверяем порядок наследования
        assert mro[0] == Product
        assert BaseProduct in mro
        assert LogCreationMixin in mro

        # Проверяем, что Product стоит перед миксином в MRO
        product_index = mro.index(Product)
        mixin_index = mro.index(LogCreationMixin)
        assert product_index < mixin_index

    def test_inheritance_structure(self):
        """Тест общей структуры наследования"""
        # Product должен наследоваться от BaseProduct и LogCreationMixin
        assert BaseProduct in Product.__bases__
        assert LogCreationMixin in Product.__bases__

        # Smartphone и LawnGrass должны наследоваться только от Product
        assert Smartphone.__bases__ == (Product,)
        assert LawnGrass.__bases__ == (Product,)


def test_concrete_methods_implementation():
    """Тест реализации конкретных методов в наследниках"""
    # Создаем продукт
    product = Product("Test", "Desc", 100.0, 5)

    # Проверяем, что методы возвращают правильные значения
    assert product.price == 100.0

    # Меняем цену
    product.price = 150.0
    assert product.price == 150.0

    # Проверяем строковое представление
    assert str(product) == "Test, 150.0 руб. Остаток: 5 шт."

    # Проверяем сложение
    product2 = Product("Test2", "Desc2", 200.0, 3)
    result = product + product2
    expected = (150.0 * 5) + (200.0 * 3)
    assert result == expected
