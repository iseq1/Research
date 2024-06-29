from lib.db_data_pusher import DatabaseDataPusher

class DatabaseDataChanger(DatabaseDataPusher):
    """
    Класс DatabaseDataChanger предоставляет функциональность для вставки, управления и изменения данных в базе данных MySQL.

    Атрибуты:
        Наследует все атрибуты и методы класса DatabaseDataPusher.

    Методы:
        __init__(host, user, password, db_name, line_count):
            Инициализирует экземпляр DatabaseDataChanger.
            Принимает параметры:
                host (str): Адрес хоста базы данных.
                user (str): Имя пользователя базы данных.
                password (str): Пароль пользователя базы данных.
                db_name (str): Имя базы данных.
                line_count (int): Количество строк.

        clear_table(table_name):
            Удаляет все данные из указанной таблицы.
            Параметры:
                table_name (str): Имя таблицы.
            Исключения:
                В случае ошибки выводит сообщение об ошибке.

        replace_table_data(table_name, count=None):
            Заменяет все данные в указанной таблице новыми сгенерированными данными.
            Параметры:
                table_name (str): Имя таблицы.
                count (int, optional): Количество данных для генерации (по умолчанию None).
            Исключения:
                В случае ошибки выводит сообщение об ошибке.

        get_method_lambda(method_name):
            Возвращает лямбда-функцию для вызова метода генерации данных в зависимости от имени таблицы.
            Параметры:
                method_name (str): Имя таблицы.
            Возвращает:
                lambda: Лямбда-функция для генерации данных.

        execute_query(query):
            Выполняет произвольный SQL-запрос к базе данных.
            Параметры:
                query (str): SQL-запрос.
            Возвращает:
                list: Результат выполнения запроса или None в случае ошибки.
            Исключения:
                В случае ошибки выводит сообщение об ошибке.

        get_max_id(table_name):
            Получает максимальное значение идентификатора (id) из указанной таблицы.
            Параметры:
                table_name (str): Имя таблицы.
            Возвращает:
                int: Максимальное значение идентификатора (id) или 0 в случае ошибки.
            Исключения:
                В случае ошибки выводит сообщение об ошибке.

    Примечания:
        - Класс наследует функциональность от класса DatabaseDataPusher, который, предоставляет базовые методы для взаимодействия с базой данных.
        - Методы clear_table и replace_table_data используются для удаления данных из таблицы и замены их новыми данными соответственно.
        - Метод get_method_lambda используется для динамического вызова методов генерации данных в зависимости от имени таблицы.
        - Методы execute_query и get_max_id предоставляют возможность выполнения произвольных SQL-запросов и получения максимального значения идентификатора из таблицы соответственно.
    """


    def __init__(self, host, user, password, db_name, line_count):
        """
        Инициализирует экземпляр DatabaseDataChanger.

        Параметры:
            - host (str): Адрес хоста базы данных.
            - user (str): Имя пользователя базы данных.
            - password (str): Пароль пользователя базы данных.
            - db_name (str): Имя базы данных.
            - line_count (int): Количество строк.

        Примечания:
            - Вызывает конструктор родительского класса DatabaseDataPusher с передачей параметров host, user, password, db_name и line_count.
        """
        super().__init__(host, user, password, db_name, line_count)

    def clear_table(self, table_name):
        """
        Удаляет все данные из указанной таблицы.

        Параметры:
            - table_name (str): Имя таблицы, из которой будут удалены данные.

        Примечания:
            - В начале временно отключает проверку внешних ключей (SET FOREIGN_KEY_CHECKS = 0).
            - После удаления данных включает проверку внешних ключей (SET FOREIGN_KEY_CHECKS = 1).

        В случае ошибки выводит сообщение об ошибке и ее описание.
        """

        try:
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            self.cursor.execute(f"TRUNCATE TABLE {table_name}")
            self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.conn.commit()
            print(f"Все данные из таблицы '{table_name}' успешно удалены.")
        except Exception as e:
            print(f"Ошибка при удалении данных из таблицы '{table_name}':", e)


    def replace_table_data(self, table_name, count=None):
        """
        Заменяет все данные в указанной таблице новыми сгенерированными данными.

        Параметры:
            - table_name (str): Имя таблицы, в которой будут заменены данные.
            - count (int, optional): Количество новых записей, которые необходимо сгенерировать (по умолчанию None).

        Примечания:
            - Перед заменой данных вызывает метод clear_table(table_name) для удаления всех существующих данных.
            - Использует метод get_method_lambda(table_name) для получения функции генерации данных в зависимости от имени таблицы.
            - Вызывает полученную функцию для генерации новых данных и их вставки в таблицу.
            - Выводит сообщение об успешной замене данных в таблице после выполнения операции.

        В случае ошибки выводит сообщение об ошибке и ее описание.
        """

        try:
            # Удаляем все существующие данные
            self.clear_table(table_name)

            # Получаем лямбда-функцию для генерации данных
            generate_data_function = self.get_method_lambda(table_name)

            # Генерируем новые данные и сразу их вставляем
            generate_data_function(count)


            print(f"Все данные в таблице '{table_name}' успешно заменены.")
        except Exception as e:
            print(f"Ошибка при замене данных в таблице '{table_name}':", e)


    def get_method_lambda(self, method_name):
        """
        Возвращает лямбда-функцию для вызова метода генерации данных в зависимости от имени метода.

        Параметры:
            - method_name (str): Имя метода, для которого нужно получить лямбда-функцию.

        Возвращает:
            - function: Лямбда-функция, которая вызывает соответствующий метод генерации данных.

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

    def execute_query(self, query):
        """
        Выполняет произвольный SQL-запрос к базе данных.

        Параметры:
            - query (str): SQL-запрос, который нужно выполнить.

        Возвращает:
            - list or None: Результат выполнения SQL-запроса в виде списка кортежей или None в случае ошибки.

        """
        try:
            # Выполняем SQL-запрос
            self.cursor.execute(query)
            # Получаем результат выполнения запроса
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def get_max_id(self, table_name):
        """
        Получает максимальный идентификатор (id) из указанной таблицы.

        Параметры:
            - table_name (str): Имя таблицы, из которой нужно получить максимальный id.

        Возвращает:
            - int: Максимальный идентификатор (id) из указанной таблицы. Если таблица пуста, возвращает 0.

        """
        try:
            self.cursor.execute(f"SELECT MAX(id) FROM {table_name}")
            result = self.cursor.fetchone()
            return result[0] if result[0] is not None else 0
        except Exception as e:
            print(f"Ошибка при получении max(id): {e}")
            return 0