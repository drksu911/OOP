from src.product import Product
from src.category import Category

if __name__ == '__main__':
    # Тестирование создания продукта с нулевым количеством
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(f"Возникла ошибка ValueError: {e}")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    # Создание обычных продуктов
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создание категории с продуктами
    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    # Вычисление средней цены
    average_price = category1.middle_price()
    print(f"Средняя цена в категории '{category1.name}': {average_price:.2f} руб.")

    # Создание пустой категории
    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    empty_average_price = category_empty.middle_price()
    print(f"Средняя цена в пустой категории '{category_empty.name}': {empty_average_price:.2f} руб.")

    # Тестирование с одним продуктом
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category_single = Category("Телевизоры", "Категория телевизоров", [product4])
    single_average_price = category_single.middle_price()
    print(f"Средняя цена в категории с одним товаром: {single_average_price:.2f} руб.")

    # Дополнительный тест: добавление товара и пересчет средней цены
    product5 = Product("OLED 65\"", "4K OLED телевизор", 250000.0, 3)
    category_single.add_product(product5)
    new_average_price = category_single.middle_price()
    print(f"Средняя цена после добавления второго товара: {new_average_price:.2f} руб.")
