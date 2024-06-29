import timeit


def query_time(generation_func, query) -> str:
    """
    Измеряет время выполнения SQL-запроса.

    Параметры:
        - generation_func (function): Функция, выполняющая SQL-запрос.
        - query (str): SQL-запрос для выполнения.

    Возвращает:
        - str: Время выполнения запроса в секундах, форматированное до десяти знаков после запятой.
    """
    setup = f"from lib.db_data_changer import DatabaseDataChanger"  # Импортируем класс DataGenerator
    # print(generation_func(query))
    return format(timeit.timeit(lambda: generation_func(query), setup=setup, number=1), '.10f')


def generate_time(generation_func, model, n, **kwargs) -> str:
    """
    Измеряет время генерации данных.

    Параметры:
        - generation_func (function): Функция генерации данных.
        - model (class): Класс модели, для которой генерируются данные.
        - n (int): Количество генерируемых данных.
        - **kwargs: Дополнительные параметры для функции генерации.

    Возвращает:
        - str: Время генерации данных в секундах, форматированное до десяти знаков после запятой.
    """
    setup = (f"from lib.orm_classes import {model.__name__}\n"
             f"from lib.data_generator import DataGenerator\n"
             f"from __main__ import {generation_func.__name__}")  # Импортируем функцию генерации

    def wrapped_func():
        """
        Обертка для измерения времени выполнения функции генерации данных.

        Итерирует вызов функции генерации данных для модели с указанными параметрами.

        Параметры:
            - model (class): Класс модели, для которой генерируются данные.
            - n (int): Количество генерируемых данных.
            - **kwargs: Дополнительные параметры для функции генерации.

        Примечание:
            - Функция предназначена для использования в качестве аргумента в timeit.timeit.

        """
        for i in generation_func(model, n, **kwargs):
            # print(i)
            pass

    return format(timeit.timeit(wrapped_func, setup=setup, number=1), '.10f')
