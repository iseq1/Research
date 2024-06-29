import mysql.connector
import mysql.connector
import re


class Field:
    """
    Класс представляет поле (столбец) в схеме базы данных.

    Атрибуты:
        - field_type (str): Тип поля.
        - primary_key (bool): Является ли поле первичным ключом (по умолчанию False).
        - foreign_key (str, optional): Ссылка на внешний ключ, если поле является внешним ключом.
        - constraints (dict): Дополнительные ограничения поля.

    Методы:
        - __init__(self, field_type, primary_key=False, foreign_key=None, **kwargs): Инициализирует экземпляр класса Field.

    Пример:
        - field = Field(field_type='INT', primary_key=True, auto_increment=True)
    """
    def __init__(self, field_type, primary_key=False, foreign_key=None, **kwargs):
        """
        Инициализирует экземпляр класса Field.

        Параметры:
            - field_type (str): Тип поля.
            - primary_key (bool, optional): Является ли поле первичным ключом (по умолчанию False).
            - foreign_key (str, optional): Ссылка на внешний ключ, если поле является внешним ключом.
            - **kwargs: Дополнительные ограничения поля.

        Атрибуты:
            - field_type (str): Тип поля.
            - primary_key (bool): Является ли поле первичным ключом.
            - foreign_key (str or None): Ссылка на внешний ключ, если поле является внешним ключом.
            - constraints (dict): Дополнительные ограничения поля.
        """
        self.field_type = field_type
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.constraints = kwargs


class IntegerField(Field):
    """
    Класс представляет целочисленное поле в схеме базы данных.

    Наследует от класса Field.

    Атрибуты:
        - field_type (str): Тип поля (всегда 'INTEGER' для IntegerField).
        - primary_key (bool): Является ли поле первичным ключом.
        - foreign_key (str or None): Ссылка на внешний ключ, если поле является внешним ключом.
        - constraints (dict): Дополнительные ограничения поля (например, min_value, max_value).

    Методы:
        - __init__(self, primary_key=False, foreign_key=None, min_value=None, max_value=None): Инициализирует экземпляр класса IntegerField.

    Пример:
        - intField = IntegerField(primary_key=True, min_value=1, max_value=100)
    """
    def __init__(self, primary_key=False, foreign_key=None, min_value=None, max_value=None):
        """
        Инициализирует экземпляр класса IntegerField.

        Параметры:
            - primary_key (bool, optional): Является ли поле первичным ключом (по умолчанию False).
            - foreign_key (str, optional): Ссылка на внешний ключ, если поле является внешним ключом.
            - min_value (int or None, optional): Минимальное значение поля.
            - max_value (int or None, optional): Максимальное значение поля.

        Атрибуты:
            - field_type (str): Тип поля (всегда 'INTEGER').
            - primary_key (bool): Является ли поле первичным ключом.
            - foreign_key (str or None): Ссылка на внешний ключ, если поле является внешним ключом.
            - constraints (dict): Дополнительные ограничения поля (например, min_value, max_value).

        Пример:
            - field = IntegerField(primary_key=True, min_value=1, max_value=100)
        """
        super().__init__("INTEGER", primary_key, foreign_key, min_value=min_value, max_value=max_value)


class CharField(Field):
    """
    Класс представляет символьное поле в схеме базы данных.

    Наследует от класса Field.

    Атрибуты:
        - field_type (str): Тип поля (формат: 'VARCHAR(max_length)').
        - max_length (int): Максимальная длина поля.
        - primary_key (bool): Является ли поле первичным ключом.
        - foreign_key (str or None): Ссылка на внешний ключ, если поле является внешним ключом.
        - constraints (dict): Дополнительные ограничения поля.

    Методы:
        - __init__(self, max_length, primary_key=False, foreign_key=None, **constraints): Инициализирует экземпляр класса CharField.

    Пример использования:
       - field = CharField(max_length=50, primary_key=True)
    """
    def __init__(self, max_length, primary_key=False, foreign_key=None, **constraints):
        """
        Инициализирует экземпляр класса CharField.

        Параметры:
            - max_length (int): Максимальная длина поля.
            - primary_key (bool, optional): Является ли поле первичным ключом (по умолчанию False).
            - foreign_key (str, optional): Ссылка на внешний ключ, если поле является внешним ключом.
            - **constraints: Дополнительные ограничения поля.

        Атрибуты:
            - field_type (str): Тип поля (формат: 'VARCHAR(max_length)').
            - max_length (int): Максимальная длина поля.
            - primary_key (bool): Является ли поле первичным ключом.
            - foreign_key (str or None): Ссылка на внешний ключ, если поле является внешним ключом.
            - constraints (dict): Дополнительные ограничения поля.

        Пример:
           - field = CharField(max_length=50, primary_key=True)
        """
        self.max_length = max_length
        self.constraints = constraints
        super().__init__(f"VARCHAR({max_length})", primary_key, foreign_key, **constraints)


class FloatField(Field):
    """
    Класс представляет поле с плавающей точкой в схеме базы данных.

    Наследует от класса Field.

    Атрибуты:
        - field_type (str): Тип поля (в данном случае 'FLOAT').
        - primary_key (bool): Является ли поле первичным ключом.
        - foreign_key (str or None): Ссылка на внешний ключ, если поле является внешним ключом.
        - constraints (dict): Дополнительные ограничения поля.

    Методы:
        - __init__(self, primary_key=False, foreign_key=None, min_value=None, max_value=None): Инициализирует экземпляр класса FloatField.

    Пример использования:
       - field = FloatField(primary_key=True, min_value=0.0, max_value=100.0)
    """
    def __init__(self, primary_key=False, foreign_key=None, min_value=None, max_value=None):
        """
       Инициализирует экземпляр класса FloatField.

       Параметры:
           - primary_key (bool, optional): Является ли поле первичным ключом (по умолчанию False).
           - foreign_key (str, optional): Ссылка на внешний ключ, если поле является внешним ключом.
           - min_value (float or None): Минимальное значение поля (по умолчанию None).
           - max_value (float or None): Максимальное значение поля (по умолчанию None).

       Атрибуты:
           - field_type (str): Тип поля (в данном случае 'FLOAT').
           - primary_key (bool): Является ли поле первичным ключом.
           - foreign_key (str or None): Ссылка на внешний ключ, если поле является внешним ключом.
           - constraints (dict): Дополнительные ограничения поля.

       Пример:
          - field = FloatField(primary_key=True, min_value=0.0, max_value=100.0)
       """
        super().__init__("FLOAT", primary_key, foreign_key, min_value=min_value, max_value=max_value)


class ForeignKey(Field):
    """
    Класс представляет внешний ключ в схеме базы данных.

    Наследует от класса Field.

    Атрибуты:
        - field_type (str): Тип поля (в данном случае 'INTEGER').
        - primary_key (bool): Является ли поле первичным ключом (в данном случае False).
        - foreign_key (str): Ссылка на таблицу и поле, на которое ссылается внешний ключ.
        - constraints (dict): Дополнительные ограничения поля.

    Методы:
        - __init__(self, to): Инициализирует экземпляр класса ForeignKey.

    Пример использования:
       - field = ForeignKey(to='other_table.id')
    """
    def __init__(self, to):
        """
        Инициализирует экземпляр класса ForeignKey.

        Параметры:
            - to (str): Строка, указывающая на таблицу и поле, на которое ссылается внешний ключ.

        Атрибуты:
            - field_type (str): Тип поля (в данном случае 'INTEGER').
            - primary_key (bool): Является ли поле первичным ключом (в данном случае False).
            - foreign_key (str): Ссылка на таблицу и поле, на которое ссылается внешний ключ.
            - constraints (dict): Дополнительные ограничения поля.

        Пример:
           - field = ForeignKey(to='other_table.id')
        """
        super().__init__("INTEGER", foreign_key=to)


class ManyToManyField:
    """
      Класс представляет поле многие-ко-многим в схеме базы данных.

      Атрибуты:
          - to (str): Строка, указывающая на таблицу, с которой установлена связь многие-ко-многим.

      Методы:
          - __init__(self, to): Инициализирует экземпляр класса ManyToManyField.

      Пример использования:
          - field = ManyToManyField(to='Menu')
      """
    def __init__(self, to):
        """
        Инициализирует экземпляр класса ManyToManyField.

        Параметры:
            - to (str): Строка, указывающая на таблицу, с которой установлена связь многие-ко-многим.

        Атрибуты:
            - to (str): Строка, указывающая на таблицу, с которой установлена связь многие-ко-многим.

        Пример:
           - field = ManyToManyField(to='Menu')
        """
        self.to = to


class ModelMeta(type):
    """
    Метакласс для определения моделей в ORM системе.

    Атрибуты:
        - parse_docstring (staticmethod): Метод для парсинга docstring модели.

    Методы:
        - __new__(cls, name, bases, attrs):  Создает новый класс модели с атрибутами _meta, содержащими информацию о полях и связях многие-ко-многим.

        - parse_docstring(docstring): Статический метод для парсинга docstring модели и извлечения информации о полях и связях.

    """
    def __new__(cls, name, bases, attrs):
        """
       Создает новый класс модели с атрибутами _meta, содержащими информацию о полях и связях многие-ко-многим.

       Параметры:
           - cls (type): Тип метакласса.
           - name (str): Имя класса.
           - bases (tuple): Кортеж базовых классов.
           - attrs (dict): Словарь атрибутов и методов класса.

       Возвращает:
           - type: Новый класс модели.
        """
        if name == "Model":
            return super().__new__(cls, name, bases, attrs)

        docstring = attrs.get("__doc__", "")
        columns, many_to_many = cls.parse_docstring(docstring)
        attrs["_meta"] = {"columns": columns, "many_to_many": many_to_many}

        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def parse_docstring(docstring):
        """
        Парсит docstring модели и извлекает информацию о полях и связях.

        Параметры:
            - docstring (str): Docstring модели.

        Возвращает:
            - tuple: Кортеж, содержащий словарь колонок (columns) и список связей многие-ко-многим (many_to_many).

        Пример:
            Для docstring:\n
            "\n
            id: IntegerField(primary_key=True)\n
            name: CharField(max_length=50)\n
            related_model: ForeignKey(to='RelatedModel')\n
            related_models: ManyToManyField(to='RelatedModel')\n
            "\n
            Возвращает ({'id': IntegerField(primary_key=True), 'name': CharField(max_length=50),
            'related_model': ForeignKey(to='RelatedModel')}, [('related_models', 'RelatedModel')])
        """
        columns = {}
        many_to_many = []
        for line in docstring.strip().split("\n"):
            match = re.match(r"(\w+):\s*(\w+)(?:\((.*?)\))?", line.strip())
            if match:
                name, field_type, params = match.groups()
                if field_type == "IntegerField":
                    columns[name] = IntegerField(primary_key="primary_key=True" in (params or ""))
                elif field_type == "CharField":
                    max_length_match = re.search(r"max_length=(\d+)", params)
                    max_length = int(max_length_match.group(1)) if max_length_match else 255
                    constraints = {}
                    if "words_count" in params:
                        words_count_match = re.search(r"words_count=(\d+)", params)
                        constraints["words_count"] = int(words_count_match.group(1))
                    columns[name] = CharField(max_length, primary_key="primary_key=True" in (params or ""), **constraints)
                elif field_type == "FloatField":
                    columns[name] = FloatField()
                elif field_type == "ForeignKey":
                    foreign_key = params.split("=")[-1]
                    columns[name] = ForeignKey(foreign_key)
                elif field_type == "ManyToManyField":
                    many_to_many.append((name, params.split("=")[-1]))
        return columns, many_to_many


class Model(metaclass=ModelMeta):
    """
        Базовый класс модели, использующий метакласс ModelMeta для автоматического определения полей и связей.

        Атрибуты класса:
            - db_name (str): Название базы данных по умолчанию.
            - host (str): Хост базы данных.
            - user (str): Пользователь базы данных.
            - password (str): Пароль пользователя базы данных.

        Атрибуты экземпляра:
            - _data (dict): Словарь для хранения значений полей модели.
    """
    db_name = "my_sandbox_database"
    host = "localhost"
    user = "root"
    password = "123456"

    def __init__(self, **kwargs):
        """
        Инициализирует экземпляр модели, проверяя и устанавливая значения полей на основе переданных аргументов.

        Параметры:
            - **kwargs: Ключевые аргументы, соответствующие именам полей модели.

        Исключения:
            - AttributeError: Если передан ключ, не соответствующий ни одному полю модели.

        Пример:
            my_model = MyModel(id=1, name="Example")
            print(my_model._data)  # {'id': 1, 'name': 'Example'}
        """
        self._data = {}
        for key, value in kwargs.items():
            if key in self._meta["columns"]:
                field = self._meta["columns"][key]
                self.validate_field(key, value, field)
                self._data[key] = value
            else:
                raise AttributeError(f"Invalid attribute: {key}")

    def validate_field(self, key, value, field):
        """
        Проверяет значение поля на соответствие ограничениям, определённым в классе поля.

        Параметры:
        ----------
        key : str
            Название поля, которое проверяется.
        value : any
            Значение поля, которое проверяется.
        field : Field
            Объект поля, который содержит тип и ограничения для проверки.

        Исключения:
        -----------
        ValueError:
        Возникает, если значение поля не удовлетворяет ограничениям.\n
            1) Для IntegerField:
                * Если значение меньше min_value.
                * Если значение больше max_value.
            2) Для CharField:
                * Если количество слов в значении не совпадает с параметром words_count.
                * Если длина значения превышает max_length.
            3) Для FloatField:
                * Если значение меньше min_value.
                * Если значение больше max_value.
        """
        if isinstance(field, IntegerField):
            if field.constraints.get('min_value') is not None and value < field.constraints['min_value']:
                raise ValueError(f"Поле '{key}' должно быть больше или равно {field.constraints['min_value']}")
            if field.constraints.get('max_value') is not None and value > field.constraints['max_value']:
                raise ValueError(f"Поле '{key}' должно быть меньше или равно {field.constraints['max_value']}")
        elif isinstance(field, CharField):
            if field.constraints.get('words_count') is not None:
                words = value.split()
                if len(words) != field.constraints['words_count']:
                    raise ValueError(f"Поле '{key}' должно состоять из {field.constraints['words_count']} слов")
            if len(value) > field.max_length:
                raise ValueError(f"Поле '{key}' должно быть длиной не превышать {field.max_length}")

        elif isinstance(field, FloatField):
            if field.constraints.get('min_value') is not None and value < field.constraints['min_value']:
                raise ValueError(f"Поле '{key}' должно быть больше или равно {field.constraints['min_value']}")
            if field.constraints.get('max_value') is not None and value > field.constraints['max_value']:
                raise ValueError(f"Поле '{key}' должно быть меньше или равно {field.constraints['max_value']}")

    def __getattr__(self, item):
        """
        Возвращает значение атрибута, если он существует в _data.

        Параметры:
        ----------
        item : str
            Название атрибута.

        Возвращает:
        -----------
        any:
            Значение атрибута, если он существует в _data.

        Исключения:
        -----------
        AttributeError:
            Возникает, если атрибут не найден в _data.
        """
        if item in self._data:
            return self._data[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        """
       Устанавливает значение атрибута, если он существует в _meta["columns"].
       В противном случае устанавливает значение в стандартном порядке.

       Параметры:
       ----------
       key : str
           Название атрибута.
       value : any
           Значение атрибута.
       """
        if key in self._meta["columns"]:
            self._data[key] = value
        else:
            super().__setattr__(key, value)

    @classmethod
    def execute_query(cls, query, params=None):
        """
        Выполняет SQL-запрос к базе данных и возвращает результаты запроса и имена столбцов.

        Параметры:
        ----------
        query : str
            SQL-запрос для выполнения.
        params : tuple, optional
            Параметры для использования в SQL-запросе.

        Возвращает:
        -----------
        tuple: Кортеж, содержащий результаты запроса (или None, если запрос не возвращает строки) и имена столбцов (или None, если запрос не возвращает строки).

        Исключения:
        -----------
        mysql.connector.Error: Вызывается, если возникает ошибка при выполнении SQL-запроса.

        Пример использования:
        ---------------------
        result, columns = Model.execute_query("SELECT * FROM my_table WHERE id = %s", (1,))
        """
        conn = None
        try:
            conn = mysql.connector.connect(
                host=cls.host,
                user=cls.user,
                password=cls.password,
                database=cls.db_name
            )
            cursor = conn.cursor()
            cursor.execute(query, params)
            if cursor.with_rows:
                result = cursor.fetchall()
                column_names = cursor.column_names
            else:
                result, column_names = None, None
            conn.commit()
            return result, column_names
        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")
        finally:
            if conn:
                conn.close()

    @classmethod
    def create_database(cls):
        """
        Создает базу данных, если она не существует.

        Параметры:
        ----------
        None

        Исключения:
        -----------
        mysql.connector.Error:
            Вызывается, если возникает ошибка при создании базы данных.

        Пример использования:
        ---------------------
        Model.create_database()
       """
        try:
            conn = mysql.connector.connect(
                host=cls.host,
                user=cls.user,
                password=cls.password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.db_name}")
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Ошибка при создании базы данных: {err}")
        finally:
            if conn:
                conn.close()

    @classmethod
    def create_table(cls):
        """
           Создает таблицу в базе данных для модели, если она не существует.

           Параметры:
           ----------
           None

           Примечания:
           -----------
           - Метод создает таблицу на основе атрибутов модели, включая поля, первичные и внешние ключи.
           - Также создает таблицы для связей Many-to-Many, если таковые имеются.

           Исключения:
           -----------
           mysql.connector.Error:
               Вызывается, если возникает ошибка при выполнении запроса к базе данных.

           Пример использования:
           ---------------------
            Model.create_table()
           """
        columns = []
        primary_keys = []
        for name, field in cls._meta["columns"].items():
            columns.append(f"{name} {field.field_type}")
            if field.primary_key:
                primary_keys.append(name)
            if field.foreign_key:
                columns.append(f"FOREIGN KEY ({name}) REFERENCES {field.foreign_key}(id)")
        if primary_keys:
            columns.append(f"PRIMARY KEY ({', '.join(primary_keys)})")
        columns_sql = ", ".join(columns)

        query = f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} ({columns_sql})"
        cls.execute_query(query)

        # Создание таблиц для Many-to-Many связей
        for field_name, related_model_name in cls._meta["many_to_many"]:
            cls.create_many_to_many_table(field_name, related_model_name)

    @classmethod
    def create_all_tables(cls):
        """
        Создает таблицы для всех моделей, наследующих данный класс, если они не существуют.

        Параметры:
        ----------
        None

        Примечания:
        -----------
        - Метод создает таблицы для всех моделей, которые наследуются от данного класса.
        - Также создает таблицы для связей Many-to-Many для каждой модели.

        Исключения:
        -----------
        mysql.connector.Error:
            Вызывается, если возникает ошибка при выполнении запроса к базе данных.

        Пример использования:
        ---------------------
        Model.create_all_tables()
        """
        for subclass in cls.__subclasses__():
            subclass.create_table()
            # Проверяем и создаем таблицы many-to-many
            for field_name, related_model_name in subclass._meta["many_to_many"]:
                subclass.create_many_to_many_table(field_name, related_model_name)

    @classmethod
    def create_many_to_many_table(cls, field_name, related_model_name):
        """
          Создает таблицу для связи Many-to-Many между двумя моделями, если она не существует.

          Параметры:
          ----------
          field_name : str
              Имя поля, которое устанавливает связь.
          related_model_name : str
              Имя модели, с которой устанавливается связь.

          Примечания:
          -----------
          - Метод создает таблицу для связи Many-to-Many между двумя моделями.
          - Название таблицы создается по шаблону "{модель}_has_{связанная_модель}".

          Исключения:
          -----------
          mysql.connector.Error:
              Вызывается, если возникает ошибка при выполнении запроса к базе данных.

          Пример использования:
          ---------------------
          Model.create_many_to_many_table("Personal_order", "Personal_order")
          """
        table_name = f"{cls.__name__.lower()}_has_{related_model_name}"
        print(table_name)
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            {cls.__name__.lower()}_id INTEGER,
            {related_model_name}_id INTEGER,
            FOREIGN KEY ({cls.__name__.lower()}_id) REFERENCES {cls.__name__.lower()}(id),
            FOREIGN KEY ({related_model_name}_id) REFERENCES {related_model_name}(id)
        )
        """
        cls.execute_query(query)

    def save(self):
        """
        Сохраняет текущий объект модели в базе данных, выполняя операцию INSERT.

        Примечания:
        -----------
        - Метод собирает все атрибуты объекта и сохраняет их в соответствующую таблицу базы данных.
        - Имя таблицы берется из имени класса в нижнем регистре.
        - Для каждого атрибута из метаданных (_meta["columns"]) объекта формируются столбцы и значения для вставки.

        Исключения:
        -----------
        mysql.connector.Error:
            Вызывается, если возникает ошибка при выполнении запроса к базе данных.

        Пример использования:
        ---------------------
         obj = MyModel(field1=value1, field2=value2)\n
         obj.save()
        """
        columns = []
        values = []
        for name in self._meta["columns"].keys():
            columns.append(name)
            values.append(getattr(self, name))
        columns_sql = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(values))

        query = f"INSERT INTO {self.__class__.__name__.lower()} ({columns_sql}) VALUES ({placeholders})"
        self.execute_query(query, values)

    @classmethod
    def all(cls):
        """
         Возвращает список всех объектов данного класса из базы данных.

         Возвращает:
         -----------
         list:
             Список объектов данного класса, соответствующих всем записям в таблице базы данных.

         Примечания:
         -----------
         - Метод выполняет запрос SELECT * FROM <table_name> для текущего класса.
         - Результаты запроса преобразуются в список экземпляров класса, инициализированных данными из базы данных.

         Исключения:
         -----------
         mysql.connector.Error:
             Вызывается, если возникает ошибка при выполнении запроса к базе данных.

         Пример использования:
         ---------------------
          objects = MyModel.all()
         """
        query = f"SELECT * FROM {cls.__name__.lower()}"
        results, column_names = cls.execute_query(query)
        if results is not None:
            return [cls(**dict(zip(column_names, result))) for result in results]
        return []

    @classmethod
    def get(cls, **kwargs):
        """
        Возвращает объект данного класса из базы данных, соответствующий заданным условиям.

        Параметры:
        ----------
        **kwargs:
            Условия для фильтрации записей в формате ключ=значение.

        Возвращает:
        -----------
        object or None:
            Объект данного класса, соответствующий первой найденной записи с заданными условиями.
            Возвращает None, если запись не найдена.

        Примечания:
        -----------
        - Метод выполняет запрос SELECT * FROM <table_name> WHERE <условия> для текущего класса.
        - Результат запроса преобразуется в экземпляр класса, инициализированный данными из первой найденной записи.

        Исключения:
        -----------
        mysql.connector.Error:
            Вызывается, если возникает ошибка при выполнении запроса к базе данных.

        Пример использования:
        ---------------------
         obj = MyModel.get(id=1)
        """
        conditions = []
        values = []
        for key, value in kwargs.items():
            conditions.append(f"{key}=%s")
            values.append(value)
        conditions_sql = " AND ".join(conditions)

        query = f"SELECT * FROM {cls.__name__.lower()} WHERE {conditions_sql}"
        results, column_names = cls.execute_query(query, values)
        if results:
            return cls(**dict(zip(column_names, results[0])))
        return None


# Определение моделей
class Menu(Model):
    """
    id: IntegerField(primary_key=True)    \n
    name: CharField(max_length=100)    \n
    prices: FloatField(min_value=1, max_value=1000)    \n
    """
    def __repr__(self):
        return f"Menu(id={self.id}, name='{self.name}', prices={self.prices})"

    def __str__(self):
        return f'Menu:\n[\n\t"id": {self.id},\n\t"name": {self.name},\n\t"prices": {self.prices}\n]'


class Barista(Model):
    """
    id: IntegerField(primary_key=True)    \n
    name: CharField(max_length=255, words_count=3)    \n
    work_time: IntegerField(min_value=0, max_value=160)    \n
    """
    def __repr__(self):
        return f"Barista(id={self.id}, name='{self.name}', work_time={self.work_time})"

    def __str__(self):
        return f'Barista:\n[\n\t"id": {self.id},\n\t"name": {self.name},\n\t"work_time": {self.work_time}\n]'


class Guest(Model):
    """
    id: IntegerField(primary_key=True)    \n
    name: CharField(max_length=255, words_count=3)    \n
    contact_number: CharField(max_length=16)    \n
    """
    def __repr__(self):
        return f"Guest(id={self.id}, name='{self.name}', contact_number='{self.contact_number}')"

    def __str__(self):
        return f'Guest:\n[\n\t"id": {self.id},\n\t"name": {self.name},\n\t"contact_number": {self.contact_number}\n]'


class Personal_Order(Model):
    """
    id: IntegerField(primary_key=True)    \n
    count: IntegerField(min_value=1, max_value=5)    \n
    menu_id: ForeignKey(to=Menu)    \n
    """
    def __repr__(self):
        return f"Personal_Order(id={self.id}, count={self.count}, menu_id={self.menu_id})"

    def __str__(self):
        return f'Personal_Order:\n[\n\t"id": {self.id},\n\t"count": {self.count},\n\t"menu_id": {self.menu_id}\n]'


class Orders(Model):
    """
    id: IntegerField(primary_key=True)    \n
    order_date: CharField(max_length=10)    \n
    guest_id: ForeignKey(to=Guest)    \n
    barista_id: ForeignKey(to=Barista)    \n
    """
    def __repr__(self):
        return f"Orders(id={self.id}, order_date='{self.order_date}', guest_id={self.guest_id}, barista_id={self.barista_id})"

    def __str__(self):
        return f'Orders:\n[\n\t"id": {self.id},\n\t"order_date": {self.order_date},\n\t"guest_id": {self.guest_id},\n\t"barista_id": {self.barista_id}\n]'


class Orders_has_personal_order(Model):
    """
    id: IntegerField(primary_key=True)
    personal_order_id: ForeignKey(to=Personal_order)
    orders_id: ForeignKey(to=Orders)
    """
    def __repr__(self):
        return f"Orders_has_personal_order(id={self.id}, personal_order_id={self.personal_order_id}, orders_id={self.orders_id})"

    def __str__(self):
        return f'Orders_has_personal_order:\n[\n\t"id": {self.id},\n\t"personal_order_id": {self.personal_order_id},\n\t"orders_id": {self.orders_id}\n]'
