from src.product import Product
from src.category import Category

if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra",
                       "256GB, Серый цвет, 200MP камера",
                       180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения "
        "дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.products)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print("\nПосле добавления нового продукта:")
    print(category1.products)

    print(f"\nОбщее количество продуктов: {Category.product_count}")

    # Тестирование класс-метода
    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5
        }
    )
    print(f"\nНовый продукт через класс-метод:")
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    # Тестирование сеттера цены
    print("\nТестирование изменения цены:")
    new_product.price = 800
    print(f"Новая цена: {new_product.price}")

    # Тестирование защиты от отрицательной цены
    new_product.price = -100
    print(f"Цена после попытки установить -100: {new_product.price}")

    new_product.price = 0
    print(f"Цена после попытки установить 0: {new_product.price}")

    # Тестирование проверки дубликатов
    print("\nТестирование проверки дубликатов:")
    existing_products = [product1, product2, product3]
    duplicate_product = Product.new_product_with_duplicate_check(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 190000.0,  # Более высокая цена
            "quantity": 3
        },
        existing_products
    )
    print(f"Количество после объединения: {product1.quantity}")
    print(f"Цена после объединения: {product1.price}")
