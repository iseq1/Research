import mysql.connector
from mysql.connector import errorcode


class SandboxCreator:
    """
    Класс для создания песочницы базы данных на основе существующей базы данных MySQL.

    Атрибуты:
        - host (str): Хост для подключения к базе данных.
        - user (str): Имя пользователя для подключения к базе данных.
        - password (str): Пароль для подключения к базе данных.
        - original_db_name (str): Имя оригинальной базы данных.
        - sandbox_db_name (str): Имя базы данных песочницы.
        - conn (mysql.connector.Connection): Соединение с базой данных.
        - cursor (mysql.connector.Cursor): Курсор для выполнения SQL-запросов.
    """
    def __init__(self, host, user, password, original_db, sandbox_db):
        """
        Инициализирует экземпляр SandboxCreator.

        Параметры:
            - host (str): Хост для подключения к базе данных.
            - user (str): Имя пользователя для подключения к базе данных.
            - password (str): Пароль для подключения к базе данных.
            - original_db (str): Имя оригинальной базы данных.
            - sandbox_db (str): Имя базы данных песочницы.
        """
        self.host = host
        self.user = user
        self.password = password
        self.original_db_name = original_db
        self.sandbox_db_name = sandbox_db
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
       Устанавливает соединение с базой данных и создает песочницу при входе в контекст.

       Возвращает:
           - SandboxCreator: Текущий экземпляр класса SandboxCreator.
       """
        self.connect()
        self.create_sandbox()
        self.conn.database = self.sandbox_db_name
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закрывает соединение с базой данных при выходе из контекста.
        """
        self.close()

    def connect(self, db_name=None):
        """
        Устанавливает соединение с базой данных и создает курсор.

        Параметры:
            - db_name (str, optional): Имя базы данных для подключения. Если не указано, используется значение по умолчанию.

        Исключения:
            - mysql.connector.Error: Ошибка подключения к базе данных, например, неверные параметры или база данных не найдена.
        """
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=db_name
            )
            self.cursor = self.conn.cursor()
            print(f"Успешное соединение с БД: {db_name} - для создания песочницы")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Ошибка в указанных параметрах.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"БД {db_name} не найдена.")
            else:
                print(err)
            exit(1)

    def close(self):
        """
        Закрывает соединение с базой данных и курсор.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def create_sandbox(self):
        """
        Создает базу данных песочницы и копирует в нее таблицы из основной базы данных.

        Примечания:
            - Создает базу данных с именем, заданным в атрибуте `self.sandbox_db_name`.
            - Если база данных уже существует, выводит соответствующее сообщение.
            - Если произошла ошибка при создании базы данных, выводит сообщение об ошибке.
            - После успешного создания базы данных вызывается метод `copy_tables` для копирования таблиц.
        """
        try:
            self.cursor.execute(f"CREATE DATABASE {self.sandbox_db_name}")
            print(f"Песочница {self.sandbox_db_name} успешно создана.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                print(f"Песочница {self.sandbox_db_name} уже существует.")
            else:
                print(err.msg)

        self.copy_tables()

    def get_table_dependencies(self) -> dict:
        """
        Определяет зависимости таблиц в базе данных.\n

        Подключается к исходной базе данных, получает список всех таблиц и анализирует их
        для определения зависимостей. Зависимости определяются по наличию упоминаний других
        таблиц в SQL-запросах на создание таблиц.

        Возвращает:
            - dict: Словарь, где ключи - это имена таблиц, а значения - списки зависимых таблиц.

        Примечания:
            - Подключается к базе данных, имя которой указано в `self.original_db_name`.
            - Для каждой таблицы выполняет запрос "SHOW CREATE TABLE", чтобы получить SQL-запрос
              создания таблицы и анализирует его на наличие имен других таблиц.
            - Если имя другой таблицы найдено в SQL-запросе и оно не совпадает с текущим именем
              таблицы, то оно добавляется в список зависимостей.
        """
        self.connect(self.original_db_name)
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]

        dependencies = {table: [] for table in tables}

        for table in tables:
            self.cursor.execute(f"SHOW CREATE TABLE {table}")
            create_table_stmt = self.cursor.fetchone()[1]

            for other_table in tables:
                if other_table in create_table_stmt and other_table != table:
                    dependencies[table].append(other_table)

        return dependencies

    def copy_tables(self):
        """
           Копирует таблицы из исходной базы данных в песочницу с учетом их зависимостей.\n

           Определяет зависимости таблиц, упорядочивает их в правильном порядке и копирует данные
           из каждой таблицы исходной базы данных в соответствующую таблицу в базе данных песочницы.

           Алгоритм:
               1. Определяет зависимости таблиц с помощью метода `get_table_dependencies()`.
               2. Разрешает зависимости таблиц, чтобы определить правильный порядок копирования.
               3. Для каждой таблицы:
                   - Подключается к исходной базе данных.
                   - Получает SQL-запрос создания таблицы.
                   - Подключается к базе данных песочницы.
                   - Создает таблицу в базе данных песочницы.
                   - Подключается к исходной базе данных.
                   - Копирует данные из исходной таблицы в соответствующую таблицу в песочнице.
               4. Подключается к базе данных песочницы.

           Примечания:
               - Для каждой таблицы сначала создается таблица в песочнице с использованием SQL-запроса
                 создания таблицы, полученного из исходной базы данных.
               - Затем данные из исходной таблицы копируются в новую таблицу в песочнице.
               - В конце метод устанавливает подключение к базе данных песочницы.
           """
        dependencies = self.get_table_dependencies()
        ordered_tables = self.resolve_dependencies(dependencies)

        for table_name in ordered_tables:
            self.connect(self.original_db_name)
            self.cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_table_stmt = self.cursor.fetchone()[1]

            self.connect(self.sandbox_db_name)
            self.cursor.execute(create_table_stmt)

            self.connect(self.original_db_name)
            self.cursor.execute(f"INSERT INTO {self.sandbox_db_name}.{table_name} SELECT * FROM {self.original_db_name}.{table_name}")

            self.conn.commit()

        self.connect(self.sandbox_db_name)

    def resolve_dependencies(self, dependencies) -> list:
        """
        Разрешает зависимости таблиц и определяет правильный порядок для их копирования.\n

        Этот метод использует алгоритм обхода графа с рекурсией для определения порядка,
        в котором таблицы должны быть скопированы, чтобы учесть их зависимости.

        Параметры:
            - dependencies (dict): Словарь, где ключи - это имена таблиц, а значения - списки имен таблиц, от которых они зависят.

        Возвращает:
            - list: Список имен таблиц в порядке, в котором они должны быть скопированы.

        Исключения:
            - Exception: Если обнаружена циклическая зависимость между таблицами.

        Алгоритм:
            1. Инициализирует списки `resolved` для хранения таблиц без неудовлетворенных зависимостей и `unresolved` для хранения таблиц с неудовлетворенными зависимостями.
            2. Определяет внутреннюю рекурсивную функцию `resolve`, которая:
                - Добавляет таблицу в `unresolved` если она еще не в `resolved`.
                - Для каждой зависимости таблицы вызывает `resolve` рекурсивно.
                - Добавляет таблицу в `resolved` и удаляет из `unresolved` после обработки всех зависимостей.
            3. Обходит каждую таблицу в `dependencies`, вызывая `resolve` для каждой таблицы.
            4. Возвращает список `resolved` как результат.

        Примечание:
            - В случае обнаружения циклической зависимости выбрасывается исключение с сообщением об ошибке.
        """
        resolved = []
        unresolved = []

        def resolve(table):
            """
            Рекурсивно разрешает зависимости таблиц.

            Рекурсивно обходит зависимости таблицы и добавляет их в список resolved,
            убеждаясь при этом, что нет циклических зависимостей.

            Параметры:
                - table (str): Название таблицы, для которой разрешаются зависимости.

            Исключения:
                - Exception: Возникает, если обнаружена циклическая зависимость между таблицами.

            """
            if table not in resolved:
                unresolved.append(table)
                for dep in dependencies[table]:
                    if dep not in resolved:
                        if dep in unresolved:
                            raise Exception(f"Обнаружена циклическая зависимость: {table} -> {dep}")
                        resolve(dep)
                resolved.append(table)
                unresolved.remove(table)

        for table in dependencies:
            resolve(table)

        return resolved


