from src.product import Product
from src.category import Category
from src.smartphone import Smartphone
from src.lawn_grass import LawnGrass

if __name__ == '__main__':
    # Тестирование создания продуктов с логированием
    print("Создание продуктов (должно выводить сообщения о создании):")
    print("-" * 50)

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("\nСвойства продуктов:")
    print("-" * 50)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    print("\nСоздание категории:")
    print("-" * 50)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products_list))
    print(category1.category_count)
    print(category1.product_count)

    print("\nСоздание еще одного продукта:")
    print("-" * 50)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4]
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.products_list))
    print(category2.products)

    print("\nОбщая статистика:")
    print("-" * 50)

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего продуктов: {Category.product_count}")

    # Тестирование создания объектов классов-наследников
    print("\nСоздание смартфона (должно выводить сообщение о создании):")
    print("-" * 50)

    smartphone = Smartphone(
        "Samsung Galaxy S23",
        "256GB, Черный",
        150000.0, 3,
        95.5, "S23", 256, "Черный"
    )

    print(f"\nСвойства смартфона: {smartphone.name}, модель: {smartphone.model}")

    print("\nСоздание газонной травы (должно выводить сообщение о создании):")
    print("-" * 50)

    grass = LawnGrass(
        "Газонная трава премиум",
        "Высококачественная трава",
        1500.0, 50,
        "Россия", "14 дней", "Зеленый"
    )

    print(f"\nСвойства травы: {grass.name}, страна: {grass.country}")
