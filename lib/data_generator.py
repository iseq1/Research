import math
import random
import string
from lib.helper_classes import *


class DataGenerator:
    """
    Класс DataGenerator используется для генерации данных, необходимых для моделирования системы кафе.
    \n
    Атрибуты:\n
    - GuestCount (int): Количество гостей, для которых генерируются данные.
    - BaristaCount (int): Количество бариста. Если не указано при инициализации, вычисляется как
      округленное вверх значение отношения GuestCount к 100.
    - MenuCount (int): Количество позиций в меню. По умолчанию 25.
    - OrderCount (int): Количество заказов. Если не указано, вычисляется как сумма GuestCount и
      округленное вверх значение отношения GuestCount к 7.5.
    - OrdersCount (int): Альтернативное количество заказов, если указано. Иначе равно GuestCount.

    Пример использования:\n
        generator = DataGenerator(GuestCount=200)
        # Создание объекта generator с заданным GuestCount, а другие параметры вычисляются автоматически.
    """

    def __init__(self, GuestCount, BaristaCount=None, MenuCount=None, OrderCount=None, OrdersCount=None):
        if not isinstance(GuestCount, int):
            raise TypeError("GuestCount должен быть целым числом")
        if not isinstance(BaristaCount, int) and BaristaCount is not None:
            raise TypeError("BaristaCount должен быть целым числом")
        if not isinstance(MenuCount, int) and MenuCount is not None:
            raise TypeError("MenuCount должен быть целым числом")
        if not isinstance(OrderCount, int) and OrderCount is not None:
            raise TypeError("OrderCount должен быть целым числом")
        if not isinstance(OrdersCount, int) and OrdersCount is not None:
            raise TypeError("OrdersCount должен быть целым числом")
        self.GuestCount = GuestCount
        if BaristaCount is not None:
            self.BaristaCount = BaristaCount
        else:
            self.BaristaCount = math.ceil(self.GuestCount / 100)
        if MenuCount is not None:
            self.MenuCount = MenuCount
        else:
            self.MenuCount = 25
        if OrderCount is not None:
            self.OrdersCount = OrdersCount
        else:
            self.OrderCount = self.GuestCount + math.ceil(self.GuestCount / 7.5)
        if OrdersCount is not None:
            self.OrdersCount = OrdersCount
        else:
            self.OrdersCount = self.GuestCount

    def Data_Generator(self) -> tuple[list[Menu], list[Order], list[Orders_has_Order], list[Orders], list[Barista], list[Guest]]:
        """
        Метод Data_Generator класса, который создаёт и возвращает данные, сгенерированные для моделирования системы кафе.

        Возвращает:

        - tuple[list[Menu], list[Order], list[Orders_has_Order], list[Orders], list[Barista], list[Guest]]: Кортеж списков соответствующих данных.

            - Menu: Данные о позициях в меню, сгенерированные методом MenuGenerator().
            - Order: Данные о заказах, сгенерированные методом OrderGenerator().
            - Orders: Данные о количестве заказов, сгенерированные методом OrdersGenerator().
            - Orders_has_Order: Данные о связях между заказами и позициями в заказе, сгенерированные методом Orders_has_OrderGenerator().
            - Barista: Данные о баристах, сгенерированные методом BaristaGenerator().
            - Guest: Данные о гостях, сгенерированные методом GuestGenerator().

        Пример использования:\n
            generator = DataGenerator() \n
            menu, order, orders_has_order, orders, barista, guest = generator.Data_Generator()
            # Получение сгенерированных данных для моделирования системы кафе.
        """

        Menu = self.MenuGenerator()
        Order = self.OrderGenerator()
        Orders = self.OrdersGenerator()
        Orders_has_Order = self.Orders_has_OrderGenerator()
        Barista = self.BaristaGenerator()
        Guest = self.GuestGenerator()

        return Menu, Order, Orders_has_Order, Orders, Barista, Guest

    def MenuGenerator(self, count=None) -> list[Menu]:
        """
        Метод MenuGenerator класса DataGenerator, который генерирует данные о позициях в меню для таблицы "Menu"\n

        Аргументы:\n
        - count (int, optional): Количество позиций в меню для генерации. Если не указан, используется значение self.MenuCount.

        Возвращает:\n
        - list[Menu]: Список объектов Menu, каждый из которых представляет собой позицию в меню с уникальным идентификатором (ID), названием(Name) и ценой(Prices).
        \n
        Пример использования:\n
            generator = DataGenerator()\n
            menu_items = generator.MenuGenerator(count=10)\n
            # Генерация 10 позиций в меню.
        """

        if count is None:
            count = self.MenuCount
        IDs = self.IDGenerator(count)
        Names = self.MenuNamesGenerator(count)
        Prices = self.PriceGenerator(count)
        return [Menu(IDs[i], Names[i], Prices[i]) for i in range(count)]

    def IDGenerator(self, count) -> list[int]:
        """
        Метод IDGenerator класса DataGenerator, который генерирует уникальные идентификаторы для объектов.

        Аргументы:\n
        - count (int): Количество идентификаторов для генерации.

        Возвращает:\n
        - list[int]: Список целых чисел, представляющих уникальные идентификаторы, начиная с 1 и до count (включительно).

        Пример использования:\n
            generator = DataGenerator()\n
            ids = generator.IDGenerator(count=10)\n
            # Генерация 10 уникальных идентификаторов.
        """

        return [i for i in range(1, count + 1)]

    def MenuNamesGenerator(self, count) -> list[str]:
        """
        Метод MenuNamesGenerator класса DataGenerator, который генерирует случайные имена для меню.

        Аргументы:\n
        - count (int): Количество имен меню для генерации.

        Возвращает:\n
        - list[str]: Список строк, представляющих случайно сгенерированные имена для меню, длина каждой из которых от 4 до 10 символов.

        Пример использования:
            generator = DataGenerator()\n
            names = generator.MenuNamesGenerator(count=10)\n
            # Генерация 10 случайных имен для меню.
        """

        return [(''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(4, 10)))) for _ in
                range(count)]

    def PriceGenerator(self, count) -> list[int]:
        """
        Метод PriceGenerator класса DataGenerator, который генерирует случайные цены для меню.\n

        Аргументы:\n
        - count (int): Количество цен для генерации.

        Возвращает:\n
        - list[int]: Список случайных цен для меню от 159 до 500 с разницей в 20 единиц.

        Пример использования:
            generator = DataGenerator()\n
            prices = generator.PriceGenerator(count=10)\n
            # Генерация 10 случайных цен для меню.
        """

        return [random.randrange(159, 500, 20) for _ in range(count)]

    def OrderGenerator(self, count=None) -> list[Order]:
        """
        Метод OrderGenerator класса DataGenerator, который генерирует заказы для таблицы "Personal_order"

        Аргументы:\n
        - count (int, optional): Количество заказов для генерации. Если не указано, используется значение self.OrderCount.

        Возвращает:\n
        - list[Order]: Список объектов Order, каждый из которых представляет собой единицу заказа с уникальным идентификатором (ID), количеством товара(Count) и позицией из меню(menu_id).

        Пример использования:
            generator = DataGenerator()\n
            orders = generator.OrderGenerator(count=20)\n
            # Генерация 20 заказов.
        """

        if count is None:
            count = self.OrderCount
        IDs = self.IDGenerator(count)
        Counts = self.CountGenerator(count)
        MenuIDs = self.IDGeneratorMenuInOrder(count)
        return [Order(IDs[i], Counts[i], MenuIDs[i]) for i in range(count)]

    def CountGenerator(self, count) -> list[int]:
        """
        Метод CountGenerator класса DataGenerator, который генерирует случайные количества товаров в заказе.

        Аргументы:\n
        - count (int): Количество записей для генерации случайных количеств товаров.

        Возвращает:\n
        - list[int]: Список случайных количеств товаров в заказе от 1 до 4.

        Пример использования:
            generator = DataGenerator()\n
            counts = generator.CountGenerator(count=20)\n
            # Генерация 20 случайных кол-во товара в заказе.
        """
        return [random.randrange(1, 4) for _ in range(count)]

    def IDGeneratorMenuInOrder(self, count) -> list[int]:
        """
        Метод IDGeneratorMenuInOrder класса DataGenerator, который генерирует случайные идентификаторы меню для заказов.

        Аргументы:\n
        - count (int): Количество записей для генерации случайных идентификаторов меню.

        Возвращает:\n
         - list[int]: Список случайных идентификаторов меню.

        Пример использования:
            generator = DataGenerator()\n
            menu_ids = generator.IDGeneratorMenuInOrder(count=20)\n
            # Генерация 20 случайных идентификаторов меню для заказов.
        """
        MenuIDs = self.IDGenerator(self.MenuCount)
        return [random.choice(MenuIDs) for _ in range(count)]

    def BaristaGenerator(self, count=None) -> list[Barista]:
        """
        Метод BaristaGenerator класса DataGenerator, который генерирует данные для таблицы "Barista".

        Аргументы:\n
        - count (int, optional): Количество бариста. По умолчанию равно self.BaristaCount.

        Возвращает:\n
        - list[Barista]: Список объектов Barista, каждый из которых представляет собой бариста с уникальным идентификатором(ID), именем(FullName) и отработанным временем(WorkTime).

        Пример использования:
            generator = DataGenerator()\n
            barista_data = generator.BaristaGenerator(count=10)\n
            # Генерация данных для 10 бариста.
        """
        if count is None:
            count = self.BaristaCount
        IDs = self.IDGenerator(count)
        FullNames = self.FullNamesGeneartor(count)
        WorkTime = self.WorkTimeGenerator(count)
        return [Barista(IDs[i], FullNames[i], WorkTime[i]) for i in range(count)]

    def FullNamesGeneartor(self, count) -> list[str]:
        """
        Метод FullNamesGeneartor класса DataGenerator, который генерирует случайные полные имена.

        Аргументы:\n
        - count (int): Количество имен.

        Возвращает:\n
        - list[str]: Список строк, представляющих сгенерированные полные имена в формате "Фамилия Имя Отчество".

        Пример использования:
            generator = DataGenerator()\n
            full_names = generator.FullNamesGeneartor(count=10)\n
            # Генерация 10 случайных полных имен.
        """
        Names = [(''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(4, 9)))) for _ in
                 range(count)]
        Surnames = [(''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(6, 13)))) for _ in
                    range(count)]
        Midnames = [(''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(7, 15)))) for _ in
                    range(count)]
        for i in range(len(Names)):
            Names[i] = Names[i][0].upper() + Names[i][1:]
            Surnames[i] = Surnames[i][0].upper() + Surnames[i][1:]
            Midnames[i] = Midnames[i][0].upper() + Midnames[i][1:]
        return [f'{Surnames[i]} {Names[i]} {Midnames[i]}' for i in range(count)]

    def WorkTimeGenerator(self, count) -> list[int]:
        """
        Метод WorkTimeGenerator класса DataGenerator, который генерирует случайные значения рабочего времени для бариста.

        Аргументы:\n
        - count (int): Количество значений рабочего времени.

        Возвращает:\n
        - list[int]: Список случайных целых чисел, представляющих рабочее время в часах от 80 до 280 с разницей в 8 единиц.

        Пример использования:
            generator = DataGenerator()\n
            work_times = generator.WorkTimeGenerator(count=10)\n
            # Генерация 10 случайных значений рабочего времени для бариста.
        """

        return [random.randrange(80, 280, 8) for _ in range(count)]

    def GuestGenerator(self, count=None) -> list[Guest]:
        """
        Метод GuestGenerator класса DataGenerator, который генерирует данные для таблицы "Guest".

        Аргументы:\n
        - count (int, optional): Количество посетителей для генерации. По умолчанию равно self.GuestCount.

        Возвращает:\n
        - list[Guest]: Список объектов Guest, каждый из которых представляет собой гостя с уникальным идентификатором(ID), именем(FullName) и контактным номером(ContactNumber).

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            guests = generator.GuestGenerator(count=10)\n
            # Генерация данных для 10 посетителей.
        """

        if count is None:
            count = self.GuestCount
        IDs = self.IDGenerator(count)
        FullNames = self.FullNamesGeneartor(count)
        CNumber = self.ContactNumberGenerator(count)
        return [Guest(IDs[i], FullNames[i], CNumber[i]) for i in range(count)]

    def ContactNumberGenerator(self, count) -> list[str]:
        """
        Метод ContactNumberGenerator класса DataGenerator, который генерирует случайные контактные номера для посетителей.

        Аргументы:\n
        - count (int): Количество номеров для генерации.

        Возвращает:\n
        - list[str]: Список строковых значений, представляющих сгенерированные контактные номера формата "+7(ХХХ)YYY-YY-YY", где ХХХ - число от 900 до 997, Y - цифра от 0 до 9

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            contact_numbers = generator.ContactNumberGenerator(count=10)\n
            # Генерация данных для 10 контактных номеров.
        """

        return ["+7(" + str(random.randrange(900, 997)) + ")" + str(random.randrange(0, 9)) + str(
            random.randrange(0, 9)) + str(random.randrange(0, 9)) + "-" + str(random.randrange(0, 9)) + str(
            random.randrange(0, 9)) + "-" + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) for _ in
                range(count)]

    def OrdersGenerator(self, count=None) -> list[Orders]:
        """
        Метод OrdersGenerator класса DataGenerator, который генерирует данные для таблицы "Orders".

        Аргументы:\n
        - count (int, optional): Количество заказов для генерации. По умолчанию равно self.OrdersCount.

        Возвращает:\n
        - list[Orders]: Список объектов Orders, каждый из которых представляет собой заказ с уникальным идентификатором(ID), датой(OrdersDate), кодом-бариста(BaristaID) и кодом-гостя(GuestID).

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            orders = generator.OrdersGenerator(count=20)\n
            # Генерация данных для 20 заказов.
        """

        if count is None:
            count = self.OrdersCount
        IDs = self.IDGenerator(count)
        Dates = self.DatesGenerator(count)
        BaristaIDs = self.IDGeneratorBaristaInOrders(count)
        GuestIDs = self.IDGeneratorGuestInOrders(count)
        return [Orders(IDs[i], Dates[i], BaristaIDs[i], GuestIDs[i]) for i in range(count)]

    def IDGeneratorBaristaInOrders(self, count) -> list[int]:
        """
        Метод IDGeneratorBaristaInOrders класса DataGenerator, который генерирует случайные идентификаторы бариста для заказов.

        Аргументы:\n
        - count (int): Количество записей, для которых генерируются идентификаторы бариста.

        Возвращает:\n
        - list[int]: Список случайно выбранных идентификаторов бариста.

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            barista_ids = generator.IDGeneratorBaristaInOrders(count=20)\n
            # Генерация данных для 20 заказов с случайными идентификаторами бариста.
        """

        BaristaIDs = self.IDGenerator(self.BaristaCount)
        return [random.choice(BaristaIDs) for _ in range(count)]

    def IDGeneratorGuestInOrders(self, count) -> list[int]:
        """
        Метод IDGeneratorGuestInOrders класса DataGenerator, который генерирует случайные идентификаторы посетителей для заказов.

        Аргументы:\n
        - count (int): Количество записей, для которых генерируются идентификаторы посетителей.

        Возвращает:\n
        - list[int]: Список случайно выбранных идентификаторов посетителей.

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            guest_ids = generator.IDGeneratorGuestInOrders(count=20)\n
            # Генерация данных для 20 заказов с случайными идентификаторами посетителей.
        """
        GuestIDs = self.IDGenerator(self.GuestCount)
        return [random.choice(GuestIDs) for _ in range(count)]

    def DatesGenerator(self, count) -> list[str]:
        """
        Метод DatesGenerator класса DataGenerator, который генерирует случайные даты для заказов.

        Аргументы:\n
        - count (int): Количество дат, которые необходимо сгенерировать.

        Возвращает:\n
        - list[str]: Список строковых представлений случайных дат в формате 'MM-DD-YYYY', где MM - месяц, DD - день, YYYY - год.

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            dates = generator.DatesGenerator(count=20)\n
            # Генерация списка из 20 случайных дат.
        """
        return [str(random.randrange(1, 13)) + "-" + str(random.randrange(1, 31)) + "-2024" for _ in range(count)]

    def Orders_has_OrderGenerator(self, count=None, existing_order_ids=None) -> list[Orders_has_Order]:
        """
        Метод Orders_has_OrderGenerator класса DataGenerator, который генерирует данные для таблицы "Orders_has_personal_order".

        Аргументы:\n
        - count (int, optional): Количество записей. По умолчанию равно self.OrderCount.
        - existing_order_ids (list, optional): Список существующих идентификаторов заказов.

        Возвращает:\n
        - list[Orders_has_Order]: Список объектов Orders_has_Order, каждый из которых представляет собой связь заказа и единицы заказа с уникальным идентификатором(ID), кодом-единицы-заказа(OrderID) и кодом-заказа(OrdersID).

        Примечания:\n
        - Если параметр existing_order_ids не указан, сгенерируются случайные идентификаторы для связей.
        - Каждая связь (Orders_has_Order) связывает два заказа.

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            orders = generator.OrderGenerator(count=50)\n
            orders_has_order = generator.Orders_has_OrderGenerator(existing_order_ids=[order.id for order in orders])\n
            # Генерация списка связей между заказами, используя идентификаторы существующих заказов.
        """

        if count is None:
            count = self.OrderCount
        if existing_order_ids is None:
            existing_order_ids = []
        IDs = self.IDGenerator(count)
        order_ids = random.choices(existing_order_ids, k=count)
        t = [Orders_has_Order(IDs[i], IDs[i], order_ids[i]) for i in range(count)]
        # for itm in t:
        #     print(itm.to_turple())
        return t


    def OrderIDGenerator(self, count) -> list[int]:
        """
        Метод OrderIDGenerator класса DataGenerator, который генерирует случайные идентификаторы заказов.

        Аргументы:\n
        - count (int): Количество записей.

        Возвращает:\n
        - list[int]: Список случайных идентификаторов заказов.

        Примечания:\n
        - Идентификаторы заказов генерируются с использованием метода IDGenerator, а затем перемешиваются.

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            order_ids = generator.OrderIDGenerator(count=50)\n
            # Генерация списка случайных идентификаторов заказов.
        """

        IDs = self.IDGenerator(count)
        random.shuffle(IDs)
        return IDs

    def OrdersIDGenerator(self) -> list[int]:
        """
        Метод OrdersIDGenerator класса DataGenerator, который генерирует идентификаторы для заказов в таблице "Orders_has_order".

        Возвращает:\n
        - list[int]: Список идентификаторов заказов.

        Примечания:\n
        - Идентификаторы заказов генерируются с использованием метода IDGenerator, и затем случайным образом выбираются некоторые из них для дополнения до нужного количества.

        Пример использования:
            generator = DataGenerator(GuestCount=100)\n
            order_ids = generator.OrdersIDGenerator()\n
            # Генерация списка идентификаторов заказов.
        """

        IDs = self.IDGenerator(self.OrdersCount)
        return IDs + random.choices(IDs, k=(self.OrderCount - self.OrdersCount))

