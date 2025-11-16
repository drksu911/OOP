from typing import List

from src.product import Product


class Category:
    category_count: int = 0
    product_count: int = 0
    __products: List[Product]  # Аннотация на уровне класса

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = []  # Инициализация приватного атрибута
        Category.category_count += 1

        # Добавляем продукты через метод для проверки типов
        for product in products:
            self.add_product(product)

    def __str__(self) -> str:
        """Строковое представление категории"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию с проверкой типа"""
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты Product или его наследников"
            )

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для получения списка товаров в формате строк"""
        return "".join(str(product) + "\n" for product in self.__products)

    @property
    def products_list(self) -> List[Product]:
        """Геттер для получения исходного списка объектов продуктов"""
        return self.__products

    def __iter__(self) -> "CategoryIterator":
        """Возвращает итератор для продуктов категории"""
        return CategoryIterator(self.__products)


class CategoryIterator:
    """Итератор для перебора продуктов в категории"""

    def __init__(self, products: List[Product]):
        self.products = products
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration
