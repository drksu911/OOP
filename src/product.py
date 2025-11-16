from typing import Any, Dict, List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price  # Приватный атрибут
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое представление продукта"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение продуктов - возвращает общую стоимость"""
        if type(self) is not type(other):
            raise TypeError("Можно складывать только объекты одинаковых классов")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Дополнительное задание: подтверждение понижения цены
        if hasattr(self, "_price") and value < self._price:
            confirmation = input("Цена понижается. Подтвердите действие (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено")
                return

        self._price = value

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "Product":
        """Создает новый продукт из словаря данных"""
        return cls(
            name=str(product_data["name"]),
            description=str(product_data["description"]),
            price=float(product_data["price"]),
            quantity=int(product_data["quantity"]),
        )

    @classmethod
    def new_product_with_duplicate_check(
        cls, product_data: Dict[str, Any], existing_products: List["Product"]
    ) -> "Product":
        """Создает новый продукт с проверкой дубликатов"""
        # Поиск дубликатов по имени
        for existing_product in existing_products:
            if existing_product.name == product_data["name"]:
                # Объединение количеств
                existing_product.quantity += int(product_data["quantity"])
                # Выбор максимальной цены
                existing_product.price = max(
                    existing_product.price, float(product_data["price"])
                )
                return existing_product

        # Если дубликат не найден, создаем новый продукт
        return cls.new_product(product_data)
