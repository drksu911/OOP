class Product:
    def __init__(
            self, name: str, description: str, price: float, quantity: int
    ):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут с двойным подчеркиванием
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Дополнительное задание: подтверждение понижения цены
        if hasattr(self, '_Product__price') and value < self.__price:
            confirmation = input(
                "Цена понижается. Подтвердите действие (y/n): "
            )
            if confirmation.lower() != 'y':
                print("Изменение цены отменено")
                return

        self.__price = value

    @classmethod
    def new_product(cls, product_data: dict):
        """Создает новый продукт из словаря данных"""
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    @classmethod
    def new_product_with_duplicate_check(cls, product_data: dict,
                                         existing_products: list):
        """Создает новый продукт с проверкой дубликатов"""
        # Поиск дубликатов по имени
        for existing_product in existing_products:
            if existing_product.name == product_data['name']:
                # Объединение количеств
                existing_product.quantity += product_data['quantity']
                # Выбор максимальной цены
                existing_product.price = max(
                    existing_product.price,
                    product_data['price']
                )
                return existing_product

        # Если дубликат не найден, создаем новый продукт
        return cls.new_product(product_data)
