import mysql.connector
from mysql.connector import errorcode
from lib.data_generator import DataGenerator


class DatabaseDataPusher:
    """
    Класс для вставки и управления данными в базе данных MySQL.

    Атрибуты:
        - db_name (str): Имя базы данных.
        - host (str): Хост для подключения к базе данных.
        - user (str): Имя пользователя для подключения к базе данных.
        - password (str): Пароль для подключения к базе данных.
        - line_count (int): Количество строк для генерации данных.
        - data (DataGenerator): Экземпляр генератора данных.
        - conn (mysql.connector.Connection): Соединение с базой данных.
        - cursor (mysql.connector.Cursor): Курсор для выполнения SQL-запросов.
    """

    def __init__(self, host, user, password, db_name, line_count):
        """
        Инициализирует экземпляр DatabaseDataPusher.

        Параметры:
            - host (str): Хост для подключения к базе данных.
            - user (str): Имя пользователя для подключения к базе данных.
            - password (str): Пароль для подключения к базе данных.
            - db_name (str): Имя базы данных.
            - line_count (int): Количество строк для генерации данных.
        """
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.line_count = line_count
        self.data = DataGenerator(line_count)
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Устанавливает соединение с базой данных и создает курсор.

        Возвращает:
            - DatabaseDataPusher: Текущий экземпляр класса DatabaseDataPusher.
        """
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )
            self.cursor = self.conn.cursor()
            # print(f"Успешное соединение с БД: {self.db_name} для сохранения сгенерированных данных.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Ошибка в указанных параметрах.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"БД {self.db_name} не найдена.")
            else:
                print(err)
            exit(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрывает соединение с базой данных.

        Параметры:
            - exc_type (type): Тип исключения.
            - exc_val (Exception): Значение исключения.
            - exc_tb (traceback): Трассировка исключения.
        """
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def DeleteStoredData(self, table):
        """
        Удаляет все данные из указанной таблицы.

        Параметры:
            - table (str): Имя таблицы.
        """
        try:
            self.cursor.execute(f"DELETE FROM {table};")
        except Exception as e:
            print("Ошибка при удалении данных:", e)

    def PushData(self, table, data):
        """
        Вставляет данные в указанную таблицу.

        Параметры:
            - table (str): Имя таблицы.
            - data (list): Список объектов, представляющих данные для вставки.
        """
        try:
            data_tuples = [entry.to_turple() for entry in data]

            self.cursor.executemany(f"INSERT INTO {table} VALUES ({', '.join(['%s'] * len(data_tuples[0]))})",
                                    data_tuples)
            self.conn.commit()
        except Exception as e:
            print("Ошибка при добавлении данных:", e)


    def PushGenerateData(self, menuCount=None, guestCount=None, baristaCount=None, orderCount=None, ordersCount=None,
                         ohoCount=None):
        """
        Генерирует и вставляет данные в соответствующие таблицы.

        Параметры:
            - menuCount (int, optional): Количество записей для таблицы menu.
            - guestCount (int, optional): Количество записей для таблицы guest.
            - baristaCount (int, optional): Количество записей для таблицы barista.
            - orderCount (int, optional): Количество записей для таблицы personal_order.
            - ordersCount (int, optional): Количество записей для таблицы orders.
            - ohoCount (int, optional): Количество записей для таблицы orders_has_order.
        """
        self.PushGenerateMenuData(menuCount)
        self.PushGenerateGuestData(guestCount)
        self.PushGenerateBaristaData(baristaCount)
        self.PushGenerateOrderData(orderCount)
        self.PushGenerateOrdersData(ordersCount)
        self.PushGenerateOrders_has_orderData(ohoCount)


    def PushGenerateMenuData(self, menuCount=None):
        """
        Генерирует и вставляет данные в таблицу menu.

        Параметры:
            - menuCount (int, optional): Количество записей для таблицы menu.
        """
        menuData = self.data.MenuGenerator(menuCount)
        self.PushData("menu", menuData)

    def PushGenerateGuestData(self, guestCount=None):
        """
        Генерирует и вставляет данные в таблицу guest.

        Параметры:
            - guestCount (int, optional): Количество записей для таблицы guest.
        """
        guestData = self.data.GuestGenerator(guestCount)
        self.PushData("guest", guestData)

    def PushGenerateBaristaData(self, baristaCount=None):
        """
        Генерирует и вставляет данные в таблицу barista.

        Параметры:
            - baristaCount (int, optional): Количество записей для таблицы barista.
        """
        baristaData = self.data.BaristaGenerator(baristaCount)
        self.PushData("barista", baristaData)

    def PushGenerateOrderData(self, orderCount=None):
        """
        Генерирует и вставляет данные в таблицу personal_order.

        Параметры:
            - orderCount (int, optional): Количество записей для таблицы personal_order.
        """
        orderData = self.data.OrderGenerator(orderCount)
        self.PushData("personal_order", orderData)

    def PushGenerateOrdersData(self, ordersCount=None):
        """
        Генерирует и вставляет данные в таблицу orders.

        Параметры:
            - ordersCount (int, optional): Количество записей для таблицы orders.
        """
        ordersData = self.data.OrdersGenerator(ordersCount)
        self.PushData("orders", ordersData)

    def PushGenerateOrders_has_orderData(self, ohoCount=None):
        """
        Генерирует и вставляет данные в таблицу orders_has_order.

        Параметры:
            - ohoCount (int, optional): Количество записей для таблицы orders_has_order.
        """
        # Сначала получаем существующие идентификаторы заказов из таблицы orders
        existing_order_ids = self.GetExistingOrderIDs()

        # Затем генерируем данные для таблицы orders_has_order, используя существующие идентификаторы
        orders_has_order_data = self.data.Orders_has_OrderGenerator(ohoCount, existing_order_ids)

        # Вставляем сгенерированные данные в таблицу orders_has_order
        self.PushData("orders_has_order", orders_has_order_data)

    def GetExistingOrderIDs(self):
        """
        Получает существующие идентификаторы заказов из таблицы orders.

        Возвращает:
            - list: Список существующих идентификаторов заказов.
        """
        query = "SELECT id FROM orders"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        existing_order_ids = [row[0] for row in result]
        return existing_order_ids

    def get_method_lambda(self, method_name):
        """
        Возвращает лямбда-функцию для вызова метода генерации данных в зависимости от имени метода.

        Параметры:
            - method_name (str): Имя метода.

        Возвращает:
            - function: Лямбда-функция для вызова соответствующего метода генерации данных.
        """
        methods = {
            "menu": lambda count: self.PushGenerateMenuData(count),
            "guest": lambda count: self.PushGenerateGuestData(count),
            "barista": lambda count: self.PushGenerateBaristaData(count),
            "personal_order": lambda count: self.PushGenerateOrderData(count),
            "orders": lambda count: self.PushGenerateOrdersData(count),
            "orders_has_order": lambda count: self.PushGenerateOrders_has_orderData(count)
        }
        return methods[method_name]
