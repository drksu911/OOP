import pytest

from src.category import Category
from src.product import Product


class TestProductZeroQuantityValidation:
    def test_product_creation_with_zero_quantity(self):
        """Тест создания продукта с нулевым количеством"""
        with pytest.raises(
            ValueError, match="Товар с нулевым количеством не может быть добавлен"
        ):
            Product("Test Product", "Description", 100.0, 0)

    def test_product_creation_with_positive_quantity(self):
        """Тест создания продукта с положительным количеством"""
        product = Product("Test Product", "Description", 100.0, 5)
        assert product.quantity == 5
        assert product.name == "Test Product"
        assert product.price == 100.0

    def test_product_creation_with_negative_quantity(self):
        """Тест создания продукта с отрицательным количеством"""
        # Отрицательное количество должно пройти, т.к. проверяется только ноль
        # В реальной системе можно добавить проверку и на отрицательные значения
        product = Product("Test Product", "Description", 100.0, -5)
        assert product.quantity == -5

    def test_new_product_with_zero_quantity(self):
        """Тест создания продукта через new_product с нулевым количеством"""
        product_data = {
            "name": "Test Product",
            "description": "Description",
            "price": 100.0,
            "quantity": 0,
        }

        with pytest.raises(
            ValueError, match="Товар с нулевым количеством не может быть добавлен"
        ):
            Product.new_product(product_data)


class TestCategoryMiddlePrice:
    def test_middle_price_with_products(self):
        """Тест средней цены в категории с товарами"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        product3 = Product("Product3", "Desc3", 300.0, 4)

        category = Category(
            "Test Category", "Description", [product1, product2, product3]
        )

        expected_average = (100.0 + 200.0 + 300.0) / 3
        assert category.middle_price() == pytest.approx(expected_average, 0.01)

    def test_middle_price_empty_category(self):
        """Тест средней цены в пустой категории"""
        category = Category("Empty Category", "Description", [])

        assert category.middle_price() == 0.0

    def test_middle_price_single_product(self):
        """Тест средней цены в категории с одним товаром"""
        product = Product("Product", "Desc", 150.0, 5)
        category = Category("Single Category", "Description", [product])

        assert category.middle_price() == 150.0

    def test_middle_price_after_adding_product(self):
        """Тест средней цены после добавления товара"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        category = Category("Test Category", "Description", [product1])

        assert category.middle_price() == 100.0

        product2 = Product("Product2", "Desc2", 200.0, 3)
        category.add_product(product2)

        expected_average = (100.0 + 200.0) / 2
        assert category.middle_price() == pytest.approx(expected_average, 0.01)

    def test_middle_price_with_zero_price_product(self):
        """Тест средней цены с товаром по нулевой цене"""
        product1 = Product("Product1", "Desc1", 0.0, 2)
        product2 = Product("Product2", "Desc2", 100.0, 3)

        category = Category("Test Category", "Description", [product1, product2])

        expected_average = (0.0 + 100.0) / 2
        assert category.middle_price() == pytest.approx(expected_average, 0.01)

    def test_middle_price_calculation_precision(self):
        """Тест точности вычисления средней цены"""
        product1 = Product("Product1", "Desc1", 33.33, 2)
        product2 = Product("Product2", "Desc2", 66.66, 3)
        product3 = Product("Product3", "Desc3", 99.99, 4)

        category = Category(
            "Test Category", "Description", [product1, product2, product3]
        )

        expected_average = (33.33 + 66.66 + 99.99) / 3
        actual_average = category.middle_price()

        assert actual_average == pytest.approx(expected_average, 0.01)


class TestMixedFunctionality:
    def test_valid_product_with_category_middle_price(self):
        """Интеграционный тест: валидный продукт + средняя цена категории"""
        product1 = Product("Product1", "Desc1", 150.0, 10)
        product2 = Product("Product2", "Desc2", 250.0, 5)

        category = Category("Test Category", "Description", [product1, product2])

        assert category.middle_price() == 200.0  # (150 + 250) / 2

    def test_category_initialization_with_zero_quantity_product(self):
        """Тест инициализации категории с продуктом нулевого количества"""
        with pytest.raises(
            ValueError, match="Товар с нулевым количеством не может быть добавлен"
        ):
            product = Product("Invalid Product", "Desc", 100.0, 0)
            # Это никогда не выполнится, так как выше будет исключение
            Category("Test Category", "Description", [product])
