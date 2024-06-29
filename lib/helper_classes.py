from datetime import datetime


class Guest:
    """
    Класс Guest представляет объект посетителя с идентификатором, полным именем и контактным номером.

    Атрибуты:\n
    - ID (int): Идентификатор посетителя.
    - FullName (str): Полное имя посетителя.
    - ContactNumber (str): Контактный номер посетителя.

    Методы:\n
    1) __init__(a, b, c):
        Конструктор класса Guest, инициализирует объект посетителя с переданными параметрами.

    2) to_turple():
        Возвращает кортеж с идентификатором, полным именем и контактным номером текущего объекта.

    Примечания:\n
    - Класс предоставляет только базовую структуру для хранения данных о посетителе.
    - Метод to_turple() полезен для представления данных объекта в виде кортежа.

    Пример использования:
        guest1 = Guest(1, 'Егоров Егор Егорыч', '+7(910)123-45-67')\n
        # Создание объекта посетителя с идентификатором 1, именем "Егоров Егор Егорыч" и контактным номером "+7(910)123-45-67".\n
        print(guest1.to_turple())\n
        # Выведет: (1, 'Егоров Егор Егорыч', '+7(910)123-45-67')
    """
    def __init__(self, a, b, c):
        if not isinstance(a, int):
            raise TypeError("ID должен быть целым числом")
        if not isinstance(b, str):
            raise TypeError("Имя должен быть строкой")
        if not isinstance(c, str):
            raise TypeError("Номер телефона должен быть строкой")
        self.ID = a
        self.FullName = b
        self.ContactNumber = c

    def to_turple(self) -> tuple[int, str, str]:
        """
        Возвращает кортеж с данными текущего объекта Guest.

        Возвращает:
             - tuple[int, str, str]: Кортеж с идентификатором, полным именем и контактным номером.
        """
        return (self.ID, self.FullName, self.ContactNumber)


class Barista:
    """
        Класс Barista представляет объект бариста с идентификатором, полным именем и рабочим временем.

        Атрибуты:\n
        - ID (int): Идентификатор посетителя.
        - FullName (str): Полное имя посетителя.
        - WorkTime (int): Рабочее время бариста.

        Методы:\n
        1) __init__(a, b, c):
            Конструктор класса Barista, инициализирует объект посетителя с переданными параметрами.

        2) to_turple():
            Возвращает кортеж с идентификатором, полным именем и рабочим временем текущего объекта.

        Примечания:\n
        - Класс предоставляет только базовую структуру для хранения данных о посетителе.
        - Метод to_turple() полезен для представления данных объекта в виде кортежа.

        Пример использования:
            barista1 = Barista(1, 'Егоров Егор Егорыч', 160)\n
            # Создание объекта бариста с идентификатором 1, именем "Егоров Егор Егорыч" и рабочим временем 160.\n
            print(barista1.to_turple())\n
            # Выведет: (1, 'Егоров Егор Егорыч', 160)
        """
    def __init__(self, a, b, c):
        if not isinstance(a, int):
            raise TypeError("ID должен быть целым числом")
        if not isinstance(b, str):
            raise TypeError("Имя должен быть строкой")
        if not isinstance(c, int):
            raise TypeError("Время работы должно быть целым числом")
        self.ID = a
        self.FullName = b
        self.WorkTime = c

    def to_turple(self) -> tuple[int, str, int]:
        """
        Возвращает кортеж с данными текущего объекта Barista.

        Возвращает:
            - tuple[int, str, int]: Кортеж с идентификатором, полным именем и рабочим временем.
        """
        return (self.ID, self.FullName, self.WorkTime)


class Orders:
    """
    Класс Orders представляет объект заказ с идентификатором, временем заказа, кодом-бариста и кодом-гостя.

    Атрибуты:\n
    - ID (int): Идентификатор заказа.
    - OrderData (str): Дата заказа.
    - BaristaID (int): Идентификатор бариста, который принял заказ.
    - GuestID (int): Идентификатор гостя, который сделал заказ.
    Методы:\n
    1) __init__(a, b, c, d):
        Конструктор класса Orders, инициализирует объект с переданными параметрами.

    2) to_turple():
        Возвращает кортеж заказ с идентификатором, временем заказа, кодом-бариста и кодом-гостя

    Примечания:\n
    - Класс предоставляет только базовую структуру для хранения данных о заказе.
    - Метод to_turple() полезен для представления данных объекта в виде кортежа.

    Пример использования:
        orders1 = Orders(1, '10-25-2025', 5, 5)\n
        print(orders1.to_turple())\n
        # Выведет: (1, '10-25-2025', 5, 5)
    """
    def __init__(self, a, b, c, d):
        if not isinstance(a, int):
            raise TypeError("ID должен быть целым числом")
        if not isinstance(b, str):
            raise TypeError("Дата заказа должна быть строкой")
        if not isinstance(c, int):
            raise TypeError("Код-бариста должен быть целым числом")
        if not isinstance(d, int):
            raise TypeError("Код-гостя должен быть целым числом")

        # try:
        #     datetime.strptime(b, '%m-%d-%Y')
        # except ValueError:
        #     raise ValueError("OrderData должен быть в формате MM-DD-YYYY")

        self.ID = a
        self.OrderData = b
        self.BaristaID = c
        self.GuestID = d

    def to_turple(self) -> tuple[int, str, int, int]:
        """
        Возвращает кортеж с данными текущего объекта Orders.

        Возвращает:
            - tuple[int, str, int, int]: Кортеж с идентификатором, полным именем и рабочим временем.
        """
        return (self.ID, self.OrderData, self.BaristaID, self.GuestID)


class Orders_has_Order:
    """
    Класс Orders_has_Order представляет объект связи заказа и единицы заказа с идентификатором, кодом-единицы-заказа и кодом-заказа.

    Атрибуты:\n
    - OrdersID (int): Идентификатор заказа.
    - OrderID (int): Идентификатор единицы заказа.
    - ID (int): Идентификатор записи.

    Методы:\n
    1) __init__(a, b, c):
        Конструктор класса Orders_has_Order, инициализирует объект с переданными параметрами.

    2) to_turple():
        Возвращает кортеж связи заказа и единицы заказа с идентификатором, кодом-единицы-заказа и кодом-заказа.

    Примечания:\n
    - Класс предоставляет только базовую структуру для хранения данных о заказе.
    - Метод to_turple() полезен для представления данных объекта в виде кортежа.

    Пример использования:
        o_H_o1 = Orders_has_Order(1, 1, 5)\n
        print(o_H_o1.to_turple())\n
        # Выведет: (1, 1, 5)
    """
    def __init__(self, a, b, c):
        if not isinstance(a, int):
            raise TypeError("ID должен быть целым числом")
        if not isinstance(b, int):
            raise TypeError("OrderID должен быть строкой")
        if not isinstance(c, int):
            raise TypeError("OrdersID телефона должен быть строкой")
        self.ID = a
        self.OrderID = b
        self.OrdersID = c

    def to_turple(self) -> tuple[int, int, int]:
        """
        Преобразует данные связи между заказом и его позициями в кортеж.

        Возвращает:
            - tuple[int, int, int]: Кортеж, содержащий ID, OrdersID и OrderID.
        """
        return (self.ID, self.OrdersID, self.OrderID)


class Order:
    """
    Класс Order представляет объект единицы заказа с идентификатором, кол-вом позиций и кодом-позиции-меню.

    Атрибуты:\n
    - ID (int): Идентификатор позиции заказа.
    - Count (int): Количество позиций.
    - MenuPosition (int): Идентификатор позиции меню

    Методы:\n
    1) __init__(a, b, c):
        Конструктор класса Order, инициализирует объект с переданными параметрами.

    2) to_turple():
        Возвращает кортеж единицы заказа с идентификатором, кол-вом позиций и кодом-позиции-меню

    Примечания:\n
    - Класс предоставляет только базовую структуру для хранения данных о заказе.
    - Метод to_turple() полезен для представления данных объекта в виде кортежа.

    Пример использования:
        order = Order(1, 1, 5)\n
        print(order.to_turple())\n
        # Выведет: (1, 1, 5)
    """
    def __init__(self, a, b, c):
        if not isinstance(a, int):
            raise TypeError("ID должен быть целым числом")
        if not isinstance(b, int):
            raise TypeError("Count должен быть строкой")
        if not isinstance(c, int):
            raise TypeError("MenuPosition телефона должен быть строкой")
        self.ID = a
        self.Count = b
        self.MenuPosition = c

    def to_turple(self) -> tuple[int, int, int]:
        """
        Преобразует данные позиции заказа в кортеж.

        Возвращает:
            - tuple[int, int, int]: Кортеж, содержащий ID, Count и MenuPosition.
        """
        return (self.ID, self.Count, self.MenuPosition)


class Menu:
    """
    Класс Menu представляет объект меню с идентификатором, названием товара и ценой товара.

    Атрибуты:\n
    - ID (int): Идентификатор позиции меню.
    - Name (str): Название позиции меню.
    - Price (int): Цена позиции меню.

    Методы:\n
    1) __init__(a, b, c):
        Конструктор класса Menu, инициализирует объект с переданными параметрами.

    2) to_turple():
        Возвращает кортеж меню с идентификатором, названием товара и ценой товара.

    Примечания:\n
    - Класс предоставляет только базовую структуру для хранения данных о заказе.
    - Метод to_turple() полезен для представления данных объекта в виде кортежа.

    Пример использования:
        menu = Menu(1, 1, 5)\n
        print(menu.to_turple())\n
        # Выведет: (1, 1, 5)
    """
    def __init__(self, a, b, c):
        if not isinstance(a, int):
            raise TypeError("ID должен быть целым числом")
        if not isinstance(b, str):
            raise TypeError("OrderID должен быть строкой")

        self.ID = a
        self.Name = b
        self.Price = c

    def to_turple(self) -> tuple[int, str, float]:
        """
        Преобразует данные элемента меню в кортеж.

        Возвращает:
            - tuple[int, str, float]: Кортеж, содержащий ID, Name и Price.
        """
        return (self.ID, self.Name, self.Price)