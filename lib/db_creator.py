import mysql.connector
from mysql.connector import errorcode

class DatabaseCreator:
    """
    Класс для создания базы данных MySQL.

    Атрибуты:\n
    - db_name (str): Имя базы данных.
    - user (str): Имя пользователя базы данных.
    - password (str): Пароль пользователя базы данных.
    - host (str): Адрес хоста базы данных.
    - conn (mysql.connector.connection_cext.CMySQLConnection): Объект соединения с базой данных.
    - cursor (mysql.connector.cursor_cext.CMySQLCursor): Объект курсора для выполнения SQL-запросов.

    """
    def __init__(self, db_name, user, password, host='localhost'):
        """
        Инициализирует экземпляр DatabaseCreator.

        Параметры:\n
        - db_name (str): Имя базы данных.
        - user (str): Имя пользователя базы данных.
        - password (str): Пароль пользователя базы данных.
        - host (str): Адрес хоста базы данных (по умолчанию 'localhost').
        """
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Метод для поддержки контекстного управления.

        При использовании контекстного менеджера создаёт подключение к базе данных MySQL,
        инициализирует курсор и устанавливает соединение с заданной базой данных.

        Returns:
            DatabaseCreator: Возвращает экземпляр DatabaseCreator.

        Raises:
            mysql.connector.Error: Возникает при ошибке подключения к базе данных.
        """
        try:
            self.conn = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host
            )
            self.cursor = self.conn.cursor()
            self.create_database()
            self.conn.database = self.db_name
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                self.conn.database = self.db_name
            else:
                print(err)
                exit(1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Метод для завершения работы с базой данных при использовании контекстного управления.

        Аргументы:
            exc_type (type): Тип исключения (если есть).\n
            exc_val (Exception): Исключение, возникшее в блоке контекста.\n
            exc_tb (traceback): Трассировка стека исключения.

        Завершает соединение с базой данных, закрывает курсор и фиксирует изменения в базе данных,
        если они были внесены.
        """
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def create_database(self):
        """
        Создает базу данных, если она не существует.\n

        При создании базы данных используется имя, указанное при инициализации
        экземпляра класса DatabaseCreator.

        Параметры:
            self.db_name (str): Имя базы данных.

        Исключения:
            mysql.connector.Error: Возникает при ошибке выполнения SQL-запроса.

        Примечания:
            Метод использует соединение и курсор, созданные при инициализации класса.
            По умолчанию устанавливается кодировка 'utf8' для базы данных.

        """
        try:
            self.cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.db_name} DEFAULT CHARACTER SET 'utf8'"
            )
        except mysql.connector.Error as err:
            print(f"Ошибка при создании БД: {err}")
            raise

    def Database_Creation(self):
        """
        Создает необходимые таблицы в базе данных, выводя прогресс создания.

        Примечания:
            Метод вызывает последовательно генераторы данных для создания таблиц:
            Menu, Barista, Guest, Order, Orders, Orders_has_Order. Каждый вызов
            соответствует определенному этапу создания таблицы, отображаемому
            в консоли с указанием процентного выполнения.

        Выводит сообщение об успешном создании базы данных после завершения всех операций.
        """
        print("||==========|Создание БД: 17%|==========||")
        self.MenuGenerator()
        print("||==========|Создание БД: 34%|==========||")
        self.BaristaGenerator()
        print("||==========|Создание БД: 50%|==========||")
        self.GuestGenerator()
        print("||==========|Создание БД: 65%|==========||")
        self.OrderGenerator()
        print("||==========|Создание БД: 81%|==========||")
        self.OrdersGenerator()
        print("||==========|Создание БД: 97%|==========||")
        self.Orders_has_OrderGenerator()
        print(f"||==========|База данных {self.db_name} успешно создана|==========||")

    def MenuGenerator(self):
        """
        Создает таблицу "menu" в базе данных.

        Примечания:
            Таблица "menu" содержит следующие поля:\n
            - id: INT, автоинкрементируемый первичный ключ.\n
            - name: VARCHAR(255), обязательное поле для названия меню.\n
            - prices: INT, обязательное поле для цены меню.\n

        В таблице используется автоинкрементируемый первичный ключ для идентификации записей.

        """

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                prices INT NOT NULL
            )
        ''')

    def OrderGenerator(self):
        """
        Создает таблицу "personal_order" в базе данных.

        Примечания:
            Таблица "personal_order" содержит следующие поля:\n
            - id: INT, автоинкрементируемый первичный ключ.\n
            - count: INT, обязательное поле для количества товаров в заказе.\n
            - menu_id: INT, обязательное поле для идентификатора меню, связанного с заказом.\n
            Содержит внешний ключ, связывающийся с полем id из таблицы "menu".

        В таблице используется автоинкрементируемый первичный ключ для идентификации записей.
        """

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS personal_order (
                id INT AUTO_INCREMENT PRIMARY KEY,
                count INT NOT NULL,
                menu_id INT NOT NULL,
                FOREIGN KEY(menu_id) REFERENCES menu(id)
            )
        ''')

    def Orders_has_OrderGenerator(self):
        """
        Создает таблицу "orders_has_order" в базе данных.

        Примечания:
            Таблица "orders_has_order" содержит следующие поля:\n
            - id: INT, автоинкрементируемый первичный ключ.\n
            - order_id: INT, обязательное поле для идентификатора позиции заказа.\n
            Содержит внешний ключ, связывающийся с полем id из таблицы "personal_order".\n
            - orders_id: INT, обязательное поле для идентификатора заказа.\n
            Содержит внешний ключ, связывающийся с полем id из таблицы "orders".

        В таблице используется автоинкрементируемый первичный ключ для идентификации записей.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders_has_order (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                orders_id INT NOT NULL,
                FOREIGN KEY(order_id) REFERENCES personal_order(id),
                FOREIGN KEY(orders_id) REFERENCES orders(id)
            )
        ''')

    def OrdersGenerator(self):
        """
        Создает таблицу "orders" в базе данных.

        Примечания:
            Таблица "orders" содержит следующие поля:\n
            - id: INT, автоинкрементируемый первичный ключ.\n
            - order_date: VARCHAR(255), обязательное поле для даты заказа.\n
            - barista_id: INT, обязательное поле для идентификатора баристы.\n
            Содержит внешний ключ, связывающийся с полем id из таблицы "barista".\n
            - guest_id: INT, обязательное поле для идентификатора посетителя.\n
            Содержит внешний ключ, связывающийся с полем id из таблицы "guest".

        В таблице используется автоинкрементируемый первичный ключ для идентификации записей.
        """

        self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS orders (
               id INT AUTO_INCREMENT PRIMARY KEY,
               order_date VARCHAR(255) NOT NULL,
               barista_id INT NOT NULL,
               guest_id INT NOT NULL,
               FOREIGN KEY(barista_id) REFERENCES barista(id),
               FOREIGN KEY(guest_id) REFERENCES guest(id)
           )
       ''')

    def BaristaGenerator(self):
        """
        Создает таблицу "barista" в базе данных.

        Примечания:
            Таблица "barista" содержит следующие поля:\n
            - id: INT, автоинкрементируемый первичный ключ.\n
            - name: VARCHAR(255), обязательное поле для имени баристы.\n
            - work_time: INT, обязательное поле для рабочего времени баристы.

        В таблице используется автоинкрементируемый первичный ключ для идентификации записей.
        """

        self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS barista (
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(255) NOT NULL,
               work_time INT NOT NULL
           )
        ''')

    def GuestGenerator(self):
        """
        Создает таблицу "guest" в базе данных.

        Примечания:\n
            Таблица "guest" содержит следующие поля:\n
            - id: INT, автоинкрементируемый первичный ключ.\n
            - name: VARCHAR(255), обязательное поле для имени посетителя.\n
            - contact_number: VARCHAR(255), обязательное поле для контактного номера посетителя.

        В таблице используется автоинкрементируемый первичный ключ для идентификации записей.
        """

        self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS guest (
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(255) NOT NULL,
               contact_number VARCHAR(255) NOT NULL
           )
       ''')

