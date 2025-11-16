import pytest

from src.category import Category
from src.lawn_grass import LawnGrass
from src.product import Product
from src.smartphone import Smartphone


class TestSmartphone:
    def test_smartphone_initialization(self):
        """Тест инициализации смартфона"""
        smartphone = Smartphone(
            "Test Phone", "Description", 1000.0, 5, 95.5, "Model X", 256, "Black"
        )

        assert smartphone.name == "Test Phone"
        assert smartphone.description == "Description"
        assert smartphone.price == 1000.0
        assert smartphone.quantity == 5
        assert smartphone.efficiency == 95.5
        assert smartphone.model == "Model X"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_smartphone_addition(self):
        """Тест сложения смартфонов"""
        smartphone1 = Smartphone("Phone1", "Desc1", 1000.0, 2, 95.0, "M1", 128, "Black")
        smartphone2 = Smartphone("Phone2", "Desc2", 1500.0, 3, 98.0, "M2", 256, "White")

        result = smartphone1 + smartphone2
        expected = (1000.0 * 2) + (1500.0 * 3)  # 2000 + 4500 = 6500
        assert result == expected

    def test_smartphone_addition_type_error(self):
        """Тест ошибки при сложении смартфона с другим классом"""
        smartphone = Smartphone("Phone", "Desc", 1000.0, 2, 95.0, "M1", 128, "Black")
        grass = LawnGrass("Grass", "Desc", 500.0, 5, "Russia", "7 days", "Green")

        # Обновляем на универсальное сообщение об ошибке
        with pytest.raises(
            TypeError, match="Можно складывать только объекты одинаковых классов"
        ):
            smartphone + grass


class TestLawnGrass:
    def test_lawn_grass_initialization(self):
        """Тест инициализации газонной травы"""
        grass = LawnGrass(
            "Test Grass", "Description", 500.0, 10, "Russia", "7 дней", "Green"
        )

        assert grass.name == "Test Grass"
        assert grass.description == "Description"
        assert grass.price == 500.0
        assert grass.quantity == 10
        assert grass.country == "Russia"
        assert grass.germination_period == "7 дней"
        assert grass.color == "Green"

    def test_lawn_grass_addition(self):
        """Тест сложения газонной травы"""
        grass1 = LawnGrass("Grass1", "Desc1", 500.0, 5, "Russia", "7 days", "Green")
        grass2 = LawnGrass("Grass2", "Desc2", 600.0, 3, "USA", "5 days", "Dark Green")

        result = grass1 + grass2
        expected = (500.0 * 5) + (600.0 * 3)  # 2500 + 1800 = 4300
        assert result == expected

    def test_lawn_grass_addition_type_error(self):
        """Тест ошибки при сложении газонной травы с другим классом"""
        grass = LawnGrass("Grass", "Desc", 500.0, 5, "Russia", "7 days", "Green")
        smartphone = Smartphone("Phone", "Desc", 1000.0, 2, 95.0, "M1", 128, "Black")

        # Обновляем на универсальное сообщение об ошибке
        with pytest.raises(
            TypeError, match="Можно складывать только объекты одинаковых классов"
        ):
            grass + smartphone


class TestCategoryWithInheritance:
    def test_category_add_product_validation(self):
        """Тест валидации при добавлении продукта в категорию"""
        category = Category("Test Category", "Description", [])

        # Должен работать с Product
        product = Product("Product", "Desc", 100.0, 5)
        category.add_product(product)
        assert len(category.products_list) == 1

        # Должен работать с Smartphone
        smartphone = Smartphone("Phone", "Desc", 1000.0, 2, 95.0, "M1", 128, "Black")
        category.add_product(smartphone)
        assert len(category.products_list) == 2

        # Должен работать с LawnGrass
        grass = LawnGrass("Grass", "Desc", 500.0, 5, "Russia", "7 days", "Green")
        category.add_product(grass)
        assert len(category.products_list) == 3

    def test_category_add_invalid_product(self):
        """Тест ошибки при добавлении не-продукта в категорию"""
        category = Category("Test Category", "Description", [])

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты Product или его наследников",
        ):
            category.add_product("Not a product")

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты Product или его наследников",
        ):
            category.add_product(123)

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты Product или его наследников",
        ):
            category.add_product({"name": "dict"})

    def test_category_initialization_with_invalid_products(self):
        """Тест инициализации категории с невалидными продуктами"""
        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты Product или его наследников",
        ):
            Category("Test Category", "Description", ["invalid1", "invalid2"])


class TestProductAdditionRestrictions:
    def test_product_addition_same_class(self):
        """Тест сложения продуктов одного класса"""
        product1 = Product("Product1", "Desc1", 100.0, 2)
        product2 = Product("Product2", "Desc2", 200.0, 3)

        result = product1 + product2
        expected = (100.0 * 2) + (200.0 * 3)  # 200 + 600 = 800
        assert result == expected

    def test_product_addition_different_classes(self):
        """Тест ошибки при сложении продуктов разных классов"""
        product = Product("Product", "Desc", 100.0, 2)
        smartphone = Smartphone("Phone", "Desc", 1000.0, 2, 95.0, "M1", 128, "Black")

        with pytest.raises(
            TypeError, match="Можно складывать только объекты одинаковых классов"
        ):
            product + smartphone

    def test_inherited_classes_cannot_add_base(self):
        """Тест что наследники не могут складываться с базовым классом"""
        smartphone = Smartphone("Phone", "Desc", 1000.0, 2, 95.0, "M1", 128, "Black")
        product = Product("Product", "Desc", 100.0, 2)

        with pytest.raises(
            TypeError, match="Можно складывать только объекты одинаковых классов"
        ):
            smartphone + product

        with pytest.raises(
            TypeError, match="Можно складывать только объекты одинаковых классов"
        ):
            product + smartphone
