from src.product import Product
from src.category import Category


if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra",
                       "256GB, Серый цвет, 200MP камера",
                       180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Тестирование __str__ для продуктов
    print("Строковое представление продуктов:")
    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения "
        "дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    # Тестирование __str__ для категории
    print("\nСтроковое представление категории:")
    print(str(category1))

    # Тестирование геттера products
    print("\nСписок товаров через геттер:")
    print(category1.products)

    # Тестирование __add__ для продуктов
    print("\nСложение продуктов:")
    print(f"product1 + product2 = {product1 + product2}")
    print(f"product1 + product3 = {product1 + product3}")
    print(f"product2 + product3 = {product2 + product3}")

    # Тестирование итератора (дополнительное задание)
    print("\nИтерация по продуктам категории:")
    for product in category1:
        print(f"  - {product.name}")