import pytest

from src.category import Category, CategoryIterator
from src.product import Product


class TestProductMagicMethods:
    def test_product_str_method(self):
        """Тест строкового представления продукта"""
        product = Product("Test Product", "Description", 100.0, 5)
        expected = "Test Product, 100.0 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_product_addition(self):
        """Тест сложения продуктов"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)

        result = product1 + product2
        expected = (100.0 * 2) + (200.0 * 3)  # 200 + 600 = 800
        assert result == expected

    def test_product_addition_with_different_products(self):
        """Тест сложения продуктов с разными ценами и количествами"""
        product1 = Product("Product1", "Desc1", 50.0, 10)
        product2 = Product("Product2", "Desc2", 75.0, 4)

        result = product1 + product2
        expected = (50.0 * 10) + (75.0 * 4)  # 500 + 300 = 800
        assert result == expected

    def test_product_addition_type_error(self):
        """Тест ошибки типа при сложении"""
        product = Product("Product", "Desc", 100.0, 5)

        with pytest.raises(TypeError, match="Можно складывать только объекты Product"):
            product + "invalid"


class TestCategoryMagicMethods:
    def test_category_str_method(self):
        """Тест строкового представления категории"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Description", [product1, product2])

        expected = "Test Category, количество продуктов: 5 шт."
        assert str(category) == expected

    def test_category_str_empty(self):
        """Тест строкового представления пустой категории"""
        category = Category("Empty Category", "Description", [])

        expected = "Empty Category, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_category_str_single_product(self):
        """Тест строкового представления категории с одним продуктом"""
        product = Product("Product", "Desc", 100.0, 7)
        category = Category("Single Category", "Description", [product])

        expected = "Single Category, количество продуктов: 7 шт."
        assert str(category) == expected

    def test_category_str_calculation(self):
        """Тест правильности расчета общего количества продуктов"""
        product1 = Product("Product1", "Desc1", 100.0, 10)
        product2 = Product("Product2", "Desc2", 200.0, 5)
        product3 = Product("Product3", "Desc3", 300.0, 3)
        category = Category(
            "Test Category", "Description", [product1, product2, product3]
        )

        expected_quantity = 10 + 5 + 3  # 18
        expected = f"Test Category, количество продуктов: {expected_quantity} шт."
        assert str(category) == expected


class TestCategoryIterator:
    def test_category_iterator(self):
        """Тест итератора категории"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Description", [product1, product2])

        products = list(category)
        assert len(products) == 2
        assert products[0] == product1
        assert products[1] == product2

    def test_category_iterator_empty(self):
        """Тест итератора пустой категории"""
        category = Category("Empty Category", "Description", [])

        products = list(category)
        assert len(products) == 0

    def test_category_iterator_direct(self):
        """Тест прямого использования итератора"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        iterator = CategoryIterator([product1, product2])

        products = list(iterator)
        assert len(products) == 2
        assert products[0] == product1
        assert products[1] == product2

    def test_category_for_loop(self):
        """Тест использования категории в цикле for"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        category = Category("Test Category", "Description", [product1, product2])

        names = []
        for product in category:
            names.append(product.name)

        assert names == ["Product1", "Product2"]

    def test_category_iterator_stop_iteration(self):
        """Тест остановки итератора"""
        product = Product("Product", "Desc", 100.0, 2)
        iterator = CategoryIterator([product])

        # Первый вызов должен вернуть продукт
        assert next(iterator) == product

        # Второй вызов должен вызвать StopIteration
        with pytest.raises(StopIteration):
            next(iterator)
