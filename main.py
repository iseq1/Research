import math
import numpy as np
from lib.graphs_creator import GraphBuilder
from lib.data_generator import DataGenerator
from lib.db_data_changer import DatabaseDataChanger
from lib.timer import query_time, generate_time
from lib.orm_classes import *


def generator_menu(n):
    """
    Генератор данных для таблицы "menu".

    Параметры:
    ----------
    n : int
        Количество записей, которые будут сгенерированы.

    Возвращает:
    -----------
    generator
        Генератор, который возвращает сгенерированные данные по одной записи за раз.

    Описание:
    ---------
    Эта функция использует класс `DataGenerator` для генерации данных для таблицы "menu". Для каждой записи генерируются следующие поля:
        - id : идентификатор записи
        - name : название позиции
        - prices : цена позиции

    """
    menu = DataGenerator(n).MenuGenerator(n)
    for i in range(n):
        instance_data = {}
        instance_data["id"] = menu[i].ID
        instance_data["name"] = menu[i].Name
        instance_data["prices"] = menu[i].Price
        yield instance_data


def generator_personal_order(n, MenuCount=None):
    """
    Генератор данных для таблицы "personal_order".

    Параметры:
    ----------
    n : int
        Количество записей, которые будут сгенерированы.
    MenuCount : int, optional
        Количество записей в таблице "menu". Если не указано, используется значение `n`.

    Возвращает:
    -----------
    generator
        Генератор, который возвращает сгенерированные данные по одной записи за раз.

    Описание:
    ---------
    Эта функция использует класс `DataGenerator` для генерации данных для таблицы "personal_order". Для каждой записи генерируются следующие поля:
        - id : идентификатор записи
        - count : количество заказанных элементов
        - menu_id : идентификатор позиции в меню

    """
    if MenuCount is None:
        menu_n = n
    else:
        menu_n = MenuCount
    personal_order = DataGenerator(n, MenuCount=menu_n).OrderGenerator(n)
    for i in range(n):
        instance_data = {}
        instance_data["id"] = personal_order[i].ID
        instance_data["count"] = personal_order[i].Count
        instance_data["menu_id"] = personal_order[i].MenuPosition
        yield instance_data


def generator_orders(n, BaristaCount=None, OrdersCount=None):
    """
    Генератор данных для таблицы "orders".

    Параметры:
    ----------
    n : int
        Количество записей, которые будут сгенерированы.
    BaristaCount : int, optional
        Количество бариста. Если не указано, используется значение `n`.
    OrdersCount : int, optional
        Количество заказов. Если не указано, используется значение `n`.

    Возвращает:
    -----------
    generator
        Генератор, который возвращает сгенерированные данные по одной записи за раз.

    Описание:
    ---------
    Эта функция использует класс `DataGenerator` для генерации данных для таблицы "orders". Для каждой записи генерируются следующие поля:
        - id : идентификатор записи
        - order_date : дата заказа
        - barista_id : идентификатор бариста, обслужившего заказ
        - guest_id : идентификатор гостя, сделавшего заказ

    """
    if BaristaCount is None:
        barista_n = n
    else:
        barista_n = BaristaCount
    if OrdersCount is None:
        orders_n = n
    else:
        orders_n = OrdersCount
    orders = DataGenerator(n, BaristaCount=barista_n, OrdersCount=orders_n).OrdersGenerator(n)
    for i in range(n):
        instance_data = {}
        instance_data["id"] = orders[i].ID
        instance_data["order_date"] = orders[i].OrderData
        instance_data["barista_id"] = orders[i].BaristaID
        instance_data["guest_id"] = orders[i].GuestID
        yield instance_data


def generator_barista(n):
    """
    Генератор данных для таблицы "barista".

    Параметры:
    ----------
    n : int
        Количество записей, которые будут сгенерированы.

    Возвращает:
    -----------
    generator
        Генератор, который возвращает сгенерированные данные по одной записи за раз.

    Описание:
    ---------
    Эта функция использует класс `DataGenerator` для генерации данных для таблицы "barista". Для каждой записи генерируются следующие поля:
        - id : идентификатор записи
        - name : полное имя бариста
        - work_time : время работы бариста

    """

    barista = DataGenerator(n, BaristaCount=n).BaristaGenerator(n)
    for i in range(n):
        instance_data = {}
        instance_data["id"] = barista[i].ID
        instance_data["name"] = barista[i].FullName
        instance_data["work_time"] = barista[i].WorkTime
        yield instance_data


def generator_guest(n):
    """
    Генератор данных для таблицы "guest".

    Параметры:
    ----------
    n : int
        Количество записей, которые будут сгенерированы.

    Возвращает:
    -----------
    generator
        Генератор, который возвращает сгенерированные данные по одной записи за раз.

    Описание:
    ---------
    Эта функция использует класс `DataGenerator` для генерации данных для таблицы "guest". Для каждой записи генерируются следующие поля:
        - id : идентификатор записи
        - name : полное имя гостя
        - contact_number : контактный номер гостя

    """
    guest = DataGenerator(n).GuestGenerator(n)
    for i in range(n):
        instance_data = {}
        instance_data["id"] = guest[i].ID
        instance_data["name"] = guest[i].FullName
        instance_data["contact_number"] = guest[i].ContactNumber
        yield instance_data


def generator_orders_has_personal_order(n, PersonOrderCount=None, OrdersCount=None):
    """
    Генератор данных для таблицы связей "orders_has_personal_order".

    Параметры:
    ----------
    n : int
        Количество записей, которые будут сгенерированы.
    PersonOrderCount : int, optional
        Количество записей в таблице "personal_order" (по умолчанию равно `n`).
    OrdersCount : int, optional
        Количество записей в таблице "orders" (по умолчанию равно `n`).

    Возвращает:
    -----------
    generator
        Генератор, который возвращает сгенерированные данные по одной записи за раз.

    Описание:
    ---------
    Эта функция использует класс `DataGenerator` для генерации данных для таблицы связей "orders_has_personal_order".
    Для каждой записи генерируются следующие поля:
        - id : идентификатор записи
        - personal_order_id : идентификатор персонального заказа
        - orders_id : идентификатор заказа
    """
    if OrdersCount is None:
        order_n = n
    else:
        order_n = OrdersCount
    if PersonOrderCount is None:
        person_order_n = n
    else:
        person_order_n = PersonOrderCount
    oho = DataGenerator(n).Orders_has_OrderGenerator(count=person_order_n,
                                                     existing_order_ids=[i for i in range(1, order_n + 1)])
    for i in range(person_order_n):
        instance_data = {}
        instance_data["id"] = oho[i].ID
        instance_data["personal_order_id"] = oho[i].OrderID
        instance_data["orders_id"] = oho[i].OrdersID
        yield instance_data


def generate(model, n, MenuCount=None, BaristaCount=None, GuestCount=None, OrdersCount=None, PersonOrderCount=None):
    """
    Генератор данных для модели.

    Параметры:
    ----------
    model : класс модели
        Класс модели, для которой генерируются данные.
    n : int
        Количество записей, которые будут сгенерированы.
    MenuCount : int, optional
        Количество записей меню, используемое при генерации данных для модели Personal_Order.
    BaristaCount : int, optional
        Количество записей бариста, используемое при генерации данных для модели Orders.
    GuestCount : int, optional
        Количество записей гостя, не используется в текущей реализации.
    OrdersCount : int, optional
        Количество записей заказов, используемое при генерации данных для модели Orders и Orders_has_personal_order.
    PersonOrderCount : int, optional
        Количество записей личных заказов, используемое при генерации данных для модели Orders_has_personal_order.

    Возвращает:
    -----------
    generator
        Генератор, который возвращает объекты модели, созданные на основе сгенерированных данных.

    Описание:
    ---------
    Эта функция генерирует данные для заданной модели, используя соответствующие генераторы данных в зависимости от имени модели.
    Если имя модели совпадает с одним из предопределенных, вызывается соответствующий генератор данных (например, generator_menu для модели Menu).
    Для каждой сгенерированной записи создается объект модели с помощью конструктора model(**data), где data - словарь с данными для модели.
    """
    if model.__name__ == "Menu":
        for data in generator_menu(n):
            yield model(**data)
    elif model.__name__ == "Personal_Order":
        for data in generator_personal_order(n, MenuCount):
            yield model(**data)
    elif model.__name__ == "Orders":
        for data in generator_orders(n, BaristaCount, OrdersCount):
            yield model(**data)
    elif model.__name__ == "Barista":
        for data in generator_barista(n):
            yield model(**data)
    elif model.__name__ == "Guest":
        for data in generator_guest(n):
            yield model(**data)
    elif model.__name__ == "Orders_has_personal_order":
        for data in generator_orders_has_personal_order(n, PersonOrderCount, OrdersCount):
            yield model(**data)


def generate_all(guest_count=None, same_lenth_table=False):
    """
    Генерация данных для всех таблиц.

    Параметры:
    ----------
    guest_count : int, optional
        Количество записей гостей для генерации.
    same_length_table : bool, optional
        Флаг указывающий, следует ли создать таблицы с одинаковым количеством записей или нет.

    Возвращает:
    -----------
    tuple
        Кортеж, содержащий сгенерированные данные для всех таблиц:
        (menus, personal_orders, baristas, guests, orders, ohos)

    Примеры использования:
    ----------------------
    1. Генерация данных для всех таблиц с предопределенными количествами записей:
        - generate_all()

    2. Генерация данных для всех таблиц с заданным количеством записей гостей:
        - generate_all(guest_count=200)

    3. Генерация данных для всех таблиц с одинаковым количеством записей:
        - generate_all(guest_count=200, same_length_table=True)

    Описание:
    ---------
    Эта функция генерирует данные для всех таблиц базы данных:
        - Menu
        - Personal_Order
        - Barista
        - Guest
        - Orders
        - Orders_has_personal_order

    В зависимости от переданных параметров guest_count и same_length_table, генерируются данные с разными количествами записей для каждой таблицы
    """
    if guest_count is None and not same_lenth_table:
        menus = generate(Menu, 25)
        personal_orders = generate(Personal_Order, 120, MenuCount=25)
        baristas = generate(Barista, 15)
        guests = generate(Guest, 100)
        orders = generate(Orders, 100, BaristaCount=15, OrdersCount=120)
        ohos = generate(Orders_has_personal_order, 100, PersonOrderCount=120, OrdersCount=100)
        return menus, personal_orders, baristas, guests, orders, ohos
    elif guest_count is not None and not same_lenth_table:
        menus = generate(Menu, 25)
        personal_orders = generate(Personal_Order, guest_count + math.ceil(guest_count / 7.5), MenuCount=25)
        baristas = generate(Barista, math.ceil(guest_count / 70))
        guests = generate(Guest, guest_count)
        orders = generate(Orders, guest_count, BaristaCount=math.ceil(guest_count / 70), OrdersCount=guest_count)
        ohos = generate(Orders_has_personal_order, guest_count,
                        PersonOrderCount=guest_count + math.ceil(guest_count / 7.5), OrdersCount=guest_count)
        return menus, personal_orders, baristas, guests, orders, ohos
    elif guest_count is not None and same_lenth_table:
        menus = generate(Menu, guest_count)
        personal_orders = generate(Personal_Order, guest_count, MenuCount=guest_count)
        baristas = generate(Barista, guest_count)
        guests = generate(Guest, guest_count)
        orders = generate(Orders, guest_count, BaristaCount=guest_count, OrdersCount=guest_count)
        ohos = generate(Orders_has_personal_order, guest_count,
                        PersonOrderCount=guest_count, OrdersCount=guest_count)
        return menus, personal_orders, baristas, guests, orders, ohos
    else:
        print("Вы не указали кол-во строк для таблиц")
        return 0


def data_generate_grpah(models, start_row=10, stop_row=10000, step=5):
    """
    Генерирует и строит график сравнения времени генерации данных для заданных моделей.

    Аргументы:
        - models (list): Список классов моделей, представляющих таблицы базы данных.
        - start_row (int, optional): Начальное количество строк для генерации данных. По умолчанию 10.
        - stop_row (int, optional): Конечное количество строк для генерации данных. По умолчанию 10000.
        - step (int, optional): Шаг для генерации точек данных между start_row и stop_row. По умолчанию 5.

    Возвращает:
        - None

    Эта функция генерирует график с использованием GraphBuilder для сравнения времени, затраченного на генерацию
    данных для различных моделей.
    """
    graph = GraphBuilder(title="Сравнение времени генерации данных", x_label="Количество строк",
                         y_label="Время выполнения")
    name = []
    funcs = []


    for model in models:
        if model == Menu:
            name.append('Menu')
            funcs.append(lambda j: float(generate_time(generate, Menu, j)))
        elif model == Personal_Order:
            name.append('Personal_order + FK(Menu)')
            funcs.append(lambda j: float(generate_time(generate, Personal_Order, j, MenuCount=50)) +
                                   float(generate_time(generate, Menu, 50)))
        elif model == Orders_has_personal_order:
            # тут я полагаю надо все таблицы генерировать т.к. у OHPO два FK, у которых в свою очередь один и два FK, что в итоге составляет всю бд
            name.append('Orders_has_personal_order (all DB)')
            # тут надо посчитать, чтобы все сходилось по цифрам
            funcs.append(lambda j: float(generate_time(generate, Menu, 50)) +
                                   float(generate_time(generate, Personal_Order, int(j+j*0.2), MenuCount=50)) +
                                   float(generate_time(generate, Barista, math.ceil(int(j+j*0.2) / 100))) +
                                   float(generate_time(generate, Guest, j)) +
                                   float(generate_time(generate, Orders, j, BaristaCount=math.ceil(int(j+j*0.2) / 100), OrdersCount=int(j+j*0.2))) +
                                   float(generate_time(generate, Orders_has_personal_order, j, PersonOrderCount=int(j+j*0.2), OrdersCount=j)))

        elif model == Orders:
            name.append('Orders + FK(Barista) + FK(Guest)')
            funcs.append(lambda j: float(generate_time(generate, Orders, int(j-j*0.1), BaristaCount=math.ceil(int(j-j*0.1) / 100), OrdersCount=j)) +
                                   float(generate_time(generate, Guest, int(j - j*0.2))) +
                                   float(generate_time(generate, Barista, math.ceil(int(j-j*0.1) / 100))))
        elif model == Barista:
            name.append('Barista')
            funcs.append(lambda j: float(generate_time(generate, Barista, j)))
        elif model == Guest:
            name.append('Guest')
            funcs.append(lambda j: float(generate_time(generate, Guest, j)))


    for i in range(len(name)):
        x = np.linspace(start_row, stop_row, step)
        x = list(map(int, x))
        y = []
        for j in range(len(x)):
            y.append(funcs[i](x[j]))
        graph.add_series(x, y, label=f"{name[i]}")

    models_str = '_'.join([model.__name__[0] if len(model.__name__.split('_')) == 1 else ''.join(
        [word[0].upper() for word in model.__name__.split('_')]) for model in models])
    graph_filename = f"graphs/generate/generate_data_{models_str}.png"
    graph.save(graph_filename)

    graph.show()


def query_graph(name, query_type, table, conditions=None, values=None, num_rows_list=None, join=None, order_by=None,
                group_by=None, having=None, insert_select=None):
    """
    Строит график времени выполнения запросов для заданной таблицы.

    Параметры:
        query_type (list[str]): Тип запроса ('SELECT', 'INSERT', 'DELETE').
        table (list[str]): Имя таблицы.
        conditions (list[str], optional): Условие для WHERE в запросах SELECT и DELETE.
        values (list[list[dict]], optional): Значения для вставки в запросах INSERT.
        num_rows_list (list[list[int]], optional): Список количества строк для запроса.
        join (list[str], optional): JOIN условие для запросов SELECT.
        order_by (list[str], optional): ORDER BY условие для запросов SELECT.
        group_by (list[str], optional): GROUP BY условие для запросов SELECT.
        having (list[str], optional): HAVING условие для запросов SELECT.
        insert_select (list[list[dict]], optional): Условие для INSERT SELECT запросов.
    """
    if num_rows_list is None:
        x = np.linspace(10, 1500, 9)
        num_rows_list = list(map(int, x))

    times = []
    names = []
    for num_rows in num_rows_list:
        for i in range(len(query_type)):
            if 'SELECT' in query_type[i]:
                if query_type[i] == 'SELECT':
                    query = f"SELECT * FROM {table[i]}"
                else:
                    query = f"{query_type[i]} FROM {table[i]}"
                if join:
                    for j in range(0, len(join[i]), 2):
                        query += f" JOIN {join[i][j]} ON {join[i][j+1]}"
                if conditions:
                    query += f" WHERE {conditions[i]}"
                if group_by:
                    query += f" GROUP BY {group_by[i]}"
                if having:
                    query += f" HAVING {having[i]}"
                if order_by:
                    query += f" ORDER BY {order_by[i]}"
                query += f" LIMIT {num_rows}"
            elif 'INSERT' in query_type[i]:
                if values and len(values[i]) > 0:
                    columns = list(values[i][0].keys())
                    max_id = get_max_id(table[i]) + 1
                    # Тут выводит ошибку, хотя запрос выполняется
                    # Ошибка при выполнении запроса: 1062 (23000): Duplicate entry '6239' for key 'menu.PRIMARY'
                    # Но вставка данных происходит и происходит корректно
                    values_str = ', '.join(
                        [f"({max_id + j}, {', '.join(map(repr, row.values()))})" for j, row in zip([i for i in range(num_rows)],values[i])])
                    query = f"INSERT INTO {table[i]} (id, {', '.join(columns)}) VALUES {values_str}"
                    query += f" LIMIT {num_rows}"
                elif insert_select and insert_select[i]:
                    max_id = get_max_id(table[i])

                    target_columns = ', '.join(['id'] + insert_select[i]['target_columns'])
                    source_columns = ', '.join(
                        [f"{max_id} + ROW_NUMBER() OVER ()"] + insert_select[i]['source_columns'])
                    source_table = insert_select[i]['source_table']
                    query = f"INSERT INTO {table[i]} ({target_columns}) SELECT {source_columns} FROM {source_table}"
                    if 'conditions' in insert_select[i] and insert_select[i]['conditions']:
                        query += f" WHERE {insert_select[i]['conditions']}"
                    query += f" LIMIT {num_rows}"
                else:
                    raise ValueError("Не указаны значения для вставки.")
            elif query_type[i] == 'DELETE':
                query = f"DELETE FROM {table[i]}"
                if conditions:
                    query += f" WHERE {conditions[i]} LIMIT {num_rows}"
                else:
                    query += f" LIMIT {num_rows}"
            else:
                raise ValueError("Неверный тип запроса. Ожидается 'SELECT', 'INSERT' или 'DELETE'.")

            with DatabaseDataChanger(host="localhost", user="root", password="123456", db_name="my_sandbox_database",
                                     line_count=100) as db_changer:

                if query.startswith('DELETE'):
                    db_changer.execute_query("SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS;")
                    # Отключаем проверку внешних ключей
                    db_changer.execute_query("SET FOREIGN_KEY_CHECKS = 0;")

                execution_time = query_time(db_changer.execute_query, query)
                print(f'ЗАПРОС(n={num_rows}):  ' + query + '; Время:' + execution_time)
                times.append(float(execution_time))
                names.append(query[:-(7+len(str(num_rows)))])

                if query.startswith('DELETE'):
                    # Восстанавливаем состояние внешних ключей
                    db_changer.execute_query("SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;")

    graph = GraphBuilder(title="Сравнение времени выполнения запроса", x_label="Количество строк",
                         y_label="Время выполнения")

    for i in range(len(query_type)):
        x = num_rows_list
        y = []
        for j in range(len(x)):
            # 0 1 2 3 4 5 6 7 8 / 9 10 11 12 13 14 15 16 17
            y.append(times[j + len(x)*i])
        graph.add_series(x, y, label=f"{names[i]}")

    # x = num_rows_list
    # y = times
    # graph.add_series(x, y, label=f"{query}")


    graph_filename = f"graphs/query/{name}.png"
    graph.save(graph_filename)

    graph.show()

    return times


def get_max_id(table_name):
    """
     Получает максимальное значение ID из указанной таблицы.

    Параметры:
    ----------
    table_name : str
        - Название таблицы, из которой требуется получить максимальное значение ID.

    Возвращает:
    -----------
    int
        - Максимальное значение ID в указанной таблице.
    """
    with DatabaseDataChanger(host="localhost", user="root", password="123456", db_name="my_sandbox_database", line_count=100) as db_changer:
        return db_changer.get_max_id(table_name)


if __name__ == "__main__":

    # 4.a
    # with DatabaseCreator(db_name='my_database', user='root', password='123456') as db_creator:
    #     """
    #     Создает базу данных и выполняет необходимые операции для ее инициализации.
    #
    #     Параметры:
    #     ----------
    #     db_name : str
    #         Имя создаваемой базы данных.
    #     user : str
    #         Имя пользователя для подключения к базе данных.
    #     password : str
    #         Пароль пользователя для подключения к базе данных.
    #
    #     Контекстный менеджер:
    #     ---------------------
    #     При входе в блок `with` выполняется метод `__enter__` класса `DatabaseCreator`, который осуществляет подключение к базе данных и создает базу данных.
    #     При выходе из блока `with` выполняется метод `__exit__`, который закрывает соединение с базой данных.
    #
    #     Методы:
    #     -------
    #     Database_Creation()
    #         Метод, выполняющий создание базы данных и необходимые операции для ее инициализации.
    #
    #     Исключения:
    #     -----------
    #     mysql.connector.Error:
    #         Вызывается, если возникает ошибка при выполнении операций с базой данных.
    #     """
    #     db_creator.Database_Creation()

    # # 4.d + 4.b
    # with DatabaseDataPusher(host='localhost', db_name='my_database', user='root', password='123456', line_count=100) as db_data_pusher:
    #     """
    #     Инициализирует и заполняет базу данных случайно сгенерированными данными.
    #
    #     Параметры:
    #     ----------
    #     host : str
    #         Хост для подключения к базе данных.
    #     db_name : str
    #         Имя базы данных, в которую будут добавлены данные.
    #     user : str
    #         Имя пользователя для подключения к базе данных.
    #     password : str
    #         Пароль пользователя для подключения к базе данных.
    #     line_count : int
    #         Количество строк данных, которое будет сгенерировано и добавлено в базу данных.
    #
    #     Контекстный менеджер:
    #     ---------------------
    #     При входе в блок `with` выполняется метод `__enter__` класса `DatabaseDataPusher`, который осуществляет подключение к базе данных.
    #     При выходе из блока `with` выполняется метод `__exit__`, который закрывает соединение с базой данных.
    #
    #     Методы:
    #     -------
    #     PushGenerateData()
    #         Метод, который генерирует случайные данные и вставляет их в базу данных.
    #
    #     Исключения:
    #     -----------
    #     mysql.connector.Error:
    #         Вызывается, если возникает ошибка при выполнении операций с базой данных.
    #     """
    #     db_data_pusher.PushGenerateData()

    # # 4.c
    # with SandboxCreator(host='localhost', user='root', password='123456', original_db='my_database', sandbox_db='my_sandbox_database') as sandbox_creator:
    #     """
    #         Создает песочницу для указанной базы данных.
    #
    #         Параметры:
    #         ----------
    #         host : str
    #             Хост для подключения к базе данных.
    #         user : str
    #             Имя пользователя для подключения к базе данных.
    #         password : str
    #             Пароль пользователя для подключения к базе данных.
    #         original_db : str
    #             Имя оригинальной базы данных, для которой создается песочница.
    #         sandbox_db : str
    #             Имя базы данных-песочницы, которая будет создана.
    #
    #         Контекстный менеджер:
    #         ---------------------
    #         При входе в блок `with` выполняется метод `__enter__` класса `SandboxCreator`, который осуществляет подключение к оригинальной базе данных и создает базу данных-песочницу.
    #         При выходе из блока `with` выполняется метод `__exit__`, который закрывает соединение с базой данных.
    #
    #         Методы:
    #         -------
    #         __enter__():
    #             Подключается к оригинальной базе данных, создает базу данных-песочницу и копирует все таблицы и данные из оригинальной базы данных.
    #         __exit__(exc_type, exc_val, exc_tb):
    #             Закрывает соединение с базой данных.
    #
    #         Исключения:
    #         -----------
    #         mysql.connector.Error:
    #             Вызывается, если возникает ошибка при выполнении операций с базой данных.
    #     """
    #     pass

    # # 4.e
    # with DatabaseDataChanger(host="localhost", user="root", password="123456", db_name="my_sandbox_database", line_count=100) as db_changer:
    #     """
    #     Контекстный менеджер для изменения данных в таблицах базы данных.
    #
    #     Параметры:
    #     ----------
    #     host : str
    #         Хост для подключения к базе данных.
    #     user : str
    #         Имя пользователя для подключения к базе данных.
    #     password : str
    #         Пароль пользователя для подключения к базе данных.
    #     db_name : str
    #         Имя базы данных, в которой будут изменяться данные.
    #     line_count : int
    #         Количество строк данных, которые будут изменены в каждой таблице по умолчанию.
    #
    #     Контекстный менеджер:
    #     ---------------------
    #     При входе в блок `with` выполняется метод `__enter__` класса `DatabaseDataChanger`, который осуществляет подключение к базе данных.
    #     При выходе из блока `with` выполняется метод `__exit__`, который закрывает соединение с базой данных.
    #
    #     Методы:
    #     -------
    #     __enter__():
    #         Подключается к базе данных.
    #     __exit__(exc_type, exc_val, exc_tb):
    #         Закрывает соединение с базой данных.
    #     replace_table_data(table_name, count):
    #         Заменяет данные в указанной таблице на новые случайные данные.
    #
    #         Параметры:
    #         ----------
    #         table_name : str
    #             Имя таблицы, в которой будут заменены данные.
    #         count : int
    #             Количество строк данных, которые будут заменены.
    #
    #     Исключения:
    #     -----------
    #     mysql.connector.Error:
    #         Вызывается, если возникает ошибка при выполнении операций с базой данных.
    #
    #     """
    #     db_changer.replace_table_data(table_name='menu', count=50)
    #     db_changer.replace_table_data(table_name='guest', count=100)

    # # 4.f
    # with DatabaseBackupRestore(host='localhost', user='root', password='123456', db_name='my_sandbox_database', line_count=100) as db_backup:
    #     """
    #     Контекстный менеджер для резервного копирования и восстановления данных таблиц базы данных,
    #     а также замены данных в таблицах на новые случайные данные.
    #
    #     Параметры:
    #     ----------
    #     host : str
    #         Хост для подключения к базе данных.
    #     user : str
    #         Имя пользователя для подключения к базе данных.
    #     password : str
    #         Пароль пользователя для подключения к базе данных.
    #     db_name : str
    #         Имя базы данных, в которой будут выполняться операции.
    #     line_count : int
    #         Количество строк данных, которые будут заменены в каждой таблице по умолчанию.
    #
    #     Контекстный менеджер:
    #     ---------------------
    #     При входе в блок `with` выполняется метод `__enter__` класса `DatabaseBackupRestore`, который осуществляет подключение к базе данных.
    #     При выходе из блока `with` выполняется метод `__exit__`, который закрывает соединение с базой данных.
    #
    #     Методы:
    #     -------
    #     __enter__():
    #         Подключается к базе данных.
    #     __exit__(exc_type, exc_val, exc_tb):
    #         Закрывает соединение с базой данных.
    #
    #     backup_table_data(table_name, file_path, file_format):
    #         Создает резервную копию данных из указанной таблицы и сохраняет в файл.
    #
    #     replace_table_data(table_name, count):
    #         Заменяет данные в указанной таблице на новые случайные данные.
    #
    #     restore_table_data(table_name, file_path, file_format):
    #         Восстанавливает данные в указанной таблице из резервной копии.
    #
    #     Исключения:
    #     -----------
    #     mysql.connector.Error:
    #         Вызывается, если возникает ошибка при выполнении операций с базой данных.
    #
    #     """
    #     db_backup.backup_table_data('menu', 'lib/backup/menu_backup.csv', 'csv')
    #     db_backup.backup_table_data('guest', 'lib/backup/guest_backup.json', 'json')
    #
    #     db_backup.replace_table_data(table_name='menu', count=50)
    #     db_backup.replace_table_data(table_name='guest', count=100)
    #
    #     db_backup.restore_table_data('menu', 'lib/backup/menu_backup.csv', 'csv')
    #     db_backup.restore_table_data('guest', 'lib/backup/guest_backup.json', 'json')

    # # 4.h
    # with DatabaseDataChanger(host="localhost", user="root", password="123456", db_name="my_sandbox_database", line_count=100) as db_changer:
    #     """
    #    Контекстный менеджер для изменения данных в базе данных.
    #
    #    Параметры:
    #    ----------
    #    host : str
    #        Хост для подключения к базе данных.
    #    user : str
    #        Имя пользователя для подключения к базе данных.
    #    password : str
    #        Пароль пользователя для подключения к базе данных.
    #    db_name : str
    #        Имя базы данных, в которой будут выполняться операции.
    #    line_count : int
    #        Количество строк данных, которые будут изменены в каждой таблице по умолчанию.
    #
    #    Контекстный менеджер:
    #    ---------------------
    #    При входе в блок `with` выполняется метод `__enter__` класса `DatabaseDataChanger`, который осуществляет подключение к базе данных.
    #    При выходе из блока `with` выполняется метод `__exit__`, который закрывает соединение с базой данных.
    #
    #    Методы:
    #    -------
    #    __enter__():
    #        Подключается к базе данных.
    #
    #    __exit__(exc_type, exc_val, exc_tb):
    #        Закрывает соединение с базой данных.
    #
    #    execute_query(query, params=None):
    #        Выполняет SQL-запрос и возвращает результаты.
    #
    #     """
    #     query = "SELECT * FROM menu WHERE prices = 259"
    #     query_time = query_time(db_changer.execute_query, query)
    #     print(f"Время выполнения запроса: {query_time} секунд")

    # Создание БД через ORM
    Model.create_database()

    # # Создание каждой из таблиц через ORM
    # Menu.create_table()
    # Guest.create_table()
    # Barista.create_table()
    # Orders.create_table()
    # Personal_Order.create_table()
    # Orders.create_many_to_many_table(field_name="personal_orders", related_model_name="personal_order")

    # Создание всех таблиц через ORM
    Model.create_all_tables()

    # # Создание записей через модели и сохранение их
    # m = Menu(id=1, name="Latte", prices=259.5)
    # m.save()
    #
    # g = Guest(id=1, name="Alica Bobson A", contact_number="+7(960)655-12-00")
    # g.save()
    #
    # b = Barista(id=1, name='Bob Alexandrovich A', work_time=90)
    # b.save()
    #
    # po = Personal_Order(id=1, menu_id=1, count=2)
    # po.save()
    #
    # o = Orders(id=1, guest_id=1, barista_id=1, order_date=f'{datetime.datetime.now().strftime("%d-%m-%Y")}')
    # o.save()
    #
    # oh = Orders_has_personal_order(id=1, personal_order_id=1, orders_id=1)
    # oh.save()
    #
    # # Получить все данные для каждой модели
    # menus = Menu.all()
    # guests = Guest.all()
    # barista = Barista.all()
    # personal_orders = Personal_Order.all()
    # orders = Orders.all()
    # ohpo = Orders_has_personal_order.all()
    #
    # print(menus)
    # for item in menus:
    #     print(item)
    # print(guests)
    # print(personal_orders)
    # print(orders)
    # print(ohpo)
    #
    # # Получить определенную запись
    # menu_item = Menu.get(id=1)
    # print(menu_item.name, menu_item.prices)
    #
    # guest = Guest.get(id=1)
    # print(guest.name)

    # Генерация данных для всех моделей и их запись
    for models in generate_all(10000, same_lenth_table=True):
        for entry in models:
            entry.save()
            print(entry)

