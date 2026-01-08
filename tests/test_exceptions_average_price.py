import sys
import time
from io import StringIO

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

    def test_zero_quantity_error_message(self):
        """Тест сообщения об ошибке при нулевом количестве"""
        try:
            Product("Test", "Desc", 100.0, 0)
        except ValueError as e:
            assert str(e) == "Товар с нулевым количеством не может быть добавлен"
        else:
            pytest.fail("Expected ValueError not raised")

    def test_zero_quantity_in_new_product_with_duplicate_check(self):
        """Тест нулевого количества в методе new_product_with_duplicate_check"""
        existing_product = Product("Existing", "Desc", 100.0, 5)
        existing_products = [existing_product]

        product_data = {
            "name": "New Product",
            "description": "Description",
            "price": 150.0,
            "quantity": 0,  # Нулевое количество!
        }

        with pytest.raises(
            ValueError, match="Товар с нулевым количеством не может быть добавлен"
        ):
            Product.new_product_with_duplicate_check(product_data, existing_products)

    def test_valid_quantity_in_new_product(self):
        """Тест корректного количества в методе new_product"""
        product_data = {
            "name": "Valid Product",
            "description": "Description",
            "price": 100.0,
            "quantity": 1,  # Корректное количество
        }

        product = Product.new_product(product_data)
        assert product.quantity == 1
        assert product.name == "Valid Product"

    def test_zero_quantity_boundary_condition(self):
        """Тест граничного условия: количество 1 должно работать"""
        product = Product("Boundary Test", "Desc", 100.0, 1)
        assert product.quantity == 1

    def test_negative_quantity_allowed_but_not_zero(self):
        """Тест, что отрицательное количество разрешено, но ноль - нет"""
        # Проверяем, что отрицательное количество проходит
        product = Product("Negative", "Desc", 100.0, -1)
        assert product.quantity == -1

        # Проверяем, что ноль не проходит
        with pytest.raises(ValueError):
            Product("Zero", "Desc", 100.0, 0)


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

    def test_middle_price_large_number_of_products(self):
        """Тест средней цены с большим количеством товаров"""
        products = []
        total_price = 0
        n = 100  # 100 товаров

        for i in range(n):
            price = (i + 1) * 10.0  # Цены от 10 до 1000
            product = Product(f"Product{i + 1}", f"Desc{i + 1}", price, i + 1)
            products.append(product)
            total_price += price

        category = Category("Large Category", "Description", products)

        expected_average = total_price / n
        actual_average = category.middle_price()

        # Проверяем с небольшой погрешностью для float
        assert actual_average == pytest.approx(expected_average, 0.001)
        assert actual_average > 0

    def test_middle_price_identical_prices(self):
        """Тест средней цены при одинаковых ценах"""
        product1 = Product("Product1", "Desc1", 100.0, 5)
        product2 = Product("Product2", "Desc2", 100.0, 3)
        product3 = Product("Product3", "Desc3", 100.0, 7)

        category = Category(
            "Identical Prices", "Description", [product1, product2, product3]
        )

        # Все цены одинаковые, средняя должна быть 100
        assert category.middle_price() == 100.0

    def test_middle_price_extreme_values(self):
        """Тест средней цены с экстремальными значениями"""
        product1 = Product("Cheap", "Very cheap", 0.01, 1000)
        product2 = Product("Expensive", "Very expensive", 1000000.0, 1)

        category = Category("Extreme Values", "Description", [product1, product2])

        expected_average = (0.01 + 1000000.0) / 2
        actual_average = category.middle_price()

        assert actual_average == pytest.approx(expected_average, 0.01)

    def test_middle_price_decimal_precision(self):
        """Тест точности вычислений с десятичными дробями"""
        product1 = Product("Product1", "Desc1", 33.333333, 2)
        product2 = Product("Product2", "Desc2", 66.666666, 3)

        category = Category("Decimal Precision", "Description", [product1, product2])

        expected_average = (33.333333 + 66.666666) / 2
        actual_average = category.middle_price()

        # Проверяем с высокой точностью
        assert actual_average == pytest.approx(expected_average, 0.000001)

    def test_middle_price_after_removing_products(self):
        """Тест средней цены после условного 'удаления' товаров"""
        # Симулируем удаление путем создания новой категории
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)
        product3 = Product("Product3", "Desc3", 300.0, 4)

        category = Category(
            "Test Category", "Description", [product1, product2, product3]
        )
        initial_average = category.middle_price()

        # "Удаляем" product3 (создаем новую категорию без него)
        category_without_last = Category(
            "Reduced Category", "Description", [product1, product2]
        )
        new_average = category_without_last.middle_price()

        expected_new_average = (100.0 + 200.0) / 2
        assert new_average == pytest.approx(expected_new_average, 0.01)
        assert new_average != initial_average

    def test_middle_price_type_return(self):
        """Тест типа возвращаемого значения"""
        product = Product("Product", "Desc", 150.0, 5)
        category = Category("Test Category", "Description", [product])

        result = category.middle_price()
        assert isinstance(result, float)

        # Для пустой категории тоже должен возвращаться float
        empty_category = Category("Empty Category", "Description", [])
        empty_result = empty_category.middle_price()
        assert isinstance(empty_result, float)
        assert empty_result == 0.0

    def test_middle_price_negative_prices_not_allowed(self):
        """Тест, что отрицательные цены не влияют на среднюю"""
        # Создаем продукты
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)

        category = Category("Test Category", "Description", [product1, product2])

        # Запоминаем начальную среднюю цену
        initial_average = category.middle_price()

        # Пытаемся установить отрицательную цену и перехватываем вывод
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            product1.price = -50.0  # Это вызовет сообщение, но не изменит цену
        finally:
            sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()

        # Проверяем, что было выведено сообщение об ошибке
        assert "Цена не должна быть нулевая или отрицательная" in output

        # Проверяем, что цена не изменилась
        assert product1.price == 100.0

        # Средняя цена должна остаться прежней
        current_average = category.middle_price()
        assert current_average == pytest.approx(initial_average, 0.01)
        assert current_average == 150.0  # (100 + 200) / 2

    def test_middle_price_with_smartphone_and_grass(self):
        """Тест средней цены с разными типами продуктов"""
        from src.lawn_grass import LawnGrass
        from src.smartphone import Smartphone

        smartphone = Smartphone(
            "Smartphone", "High-end", 50000.0, 2, 95.0, "Model X", 256, "Black"
        )

        grass = LawnGrass("Grass", "Premium", 1000.0, 10, "Russia", "7 days", "Green")

        category = Category("Mixed Products", "Description", [smartphone, grass])

        expected_average = (50000.0 + 1000.0) / 2
        actual_average = category.middle_price()

        assert actual_average == pytest.approx(expected_average, 0.01)

    def test_middle_price_cache_invalidation(self):
        """Тест, что средняя цена пересчитывается при изменении цен"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)

        category = Category("Test Category", "Description", [product1, product2])

        initial_average = category.middle_price()

        # Меняем цену одного товара
        product1.price = 150.0

        # Средняя цена должна пересчитаться
        new_average = category.middle_price()
        expected_new_average = (150.0 + 200.0) / 2

        assert new_average == pytest.approx(expected_new_average, 0.01)
        assert new_average != initial_average

    def test_middle_price_edge_case_one_product_zero_price(self):
        """Тест граничного случая: один товар с нулевой ценой"""
        product = Product("Free Product", "Free", 0.0, 1)
        category = Category("Free Category", "Description", [product])

        assert category.middle_price() == 0.0

    def test_middle_price_all_products_zero_price(self):
        """Тест, когда все товары имеют нулевую цену"""
        product1 = Product("Free1", "Desc1", 0.0, 2)
        product2 = Product("Free2", "Desc2", 0.0, 3)
        product3 = Product("Free3", "Desc3", 0.0, 4)

        category = Category("All Free", "Description", [product1, product2, product3])

        assert category.middle_price() == 0.0


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
            Product("Invalid Product", "Desc", 100.0, 0)
            # Это никогда не выполнится, так как выше будет исключение
            Category("Test Category", "Description", [])


class TestIntegrationExceptionsAndAveragePrice:
    """Интеграционные тесты исключений и средней цены"""

    def test_middle_price_after_exception_handling(self):
        """Тест средней цены после обработки исключений"""
        # Создаем категорию с валидными продуктами
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)

        category = Category("Test Category", "Description", [product1, product2])

        # Средняя цена должна считаться корректно
        average1 = category.middle_price()
        assert average1 == 150.0

        # Добавляем еще один продукт
        product3 = Product("Product3", "Desc3", 300.0, 1)
        category.add_product(product3)

        # Средняя цена должна пересчитаться
        average2 = category.middle_price()
        expected_average2 = (100.0 + 200.0 + 300.0) / 3
        assert average2 == pytest.approx(expected_average2, 0.01)

        # Проверяем, что попытка добавить продукт с нулевым количеством вызывает исключение
        with pytest.raises(ValueError):
            Product("Invalid", "Desc", 400.0, 0)

        # Средняя цена не должна измениться
        average3 = category.middle_price()
        assert average3 == pytest.approx(expected_average2, 0.01)

    def test_middle_price_performance(self):
        """Тест производительности вычисления средней цены"""
        # Создаем много продуктов
        n = 1000
        products = []
        for i in range(n):
            product = Product(f"Product{i}", f"Desc{i}", float(i * 10), i % 10 + 1)
            products.append(product)

        category = Category("Performance Test", "Description", products)

        # Измеряем время вычисления
        start_time = time.time()
        average = category.middle_price()
        end_time = time.time()

        # Вычисление должно быть быстрым
        computation_time = end_time - start_time
        assert computation_time < 0.1  # Должно выполняться менее чем за 100 мс

        # Проверяем правильность вычисления
        total_price = sum(product.price for product in products)
        expected_average = total_price / n
        assert average == pytest.approx(expected_average, 0.01)
