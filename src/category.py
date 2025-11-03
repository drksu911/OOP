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

    def add_product(self, product: Product):
        """Добавляет продукт в категорию"""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для получения списка товаров в формате строк"""
        products_info = []
        for product in self.__products:
            product_info = (
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт."
            )
            products_info.append(product_info)
        return "\n".join(products_info)

    @property
    def products_list(self):
        """Геттер для получения исходного списка объектов продуктов"""
        return self.__products
