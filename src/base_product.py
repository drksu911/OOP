from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление продукта"""
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        """Сложение продуктов"""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Геттер цены"""
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        """Сеттер цены с валидацией"""
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "BaseProduct":
        """Создание нового продукта из словаря"""
        pass


class LogCreationMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        # Сначала вызываем __init__ родительского класса
        super().__init__(*args, **kwargs)
        # Затем выводим информацию о создании объекта
        class_name = self.__class__.__name__
        # Форматируем аргументы для вывода
        args_repr = [repr(arg) for arg in args]
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        all_args = ", ".join(args_repr + kwargs_repr)
        print(f"Создан объект {class_name}({all_args})")
