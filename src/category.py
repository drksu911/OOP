from src.product import Product


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self):
        """Строковое представление категории"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product):
        """Добавляет продукт в категорию"""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для получения списка товаров в формате строк"""
        return "".join(str(product) + "\n" for product in self.__products)

    @property
    def products_list(self):
        """Геттер для получения исходного списка объектов продуктов"""
        return self.__products

    def __iter__(self):
        """Возвращает итератор для продуктов категории"""
        return CategoryIterator(self.__products)


class CategoryIterator:
    """Итератор для перебора продуктов в категории"""

    def __init__(self, products: list):
        self.products = products
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration
