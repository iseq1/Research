import unittest
from unittest.mock import MagicMock, patch, call
from lib.db_data_pusher import DatabaseDataPusher
from lib.db_data_changer import DatabaseDataChanger


class TestDatabaseDataChanger(unittest.TestCase):
    """
    Юнит-тесты для класса DatabaseDataChanger.
    """

    def setUp(self):
        """
       Устанавливает начальные условия для тестов.
       Патчит конструктор DatabaseDataPusher, чтобы избежать реального подключения к базе данных,
       и создает экземпляр DatabaseDataChanger с замоканными cursor и conn.
       """
        # Патчинг конструктора DatabaseDataPusher, чтобы избежать реального подключения к базе данных
        with patch('lib.db_data_pusher.DatabaseDataPusher.__init__', return_value=None):
            self.changer = DatabaseDataChanger('host', 'root', '123456', 'db_name', 10)
            self.changer.cursor = MagicMock()
            self.changer.conn = MagicMock()

    def test_clear_table(self):
        """
        Тестирует метод clear_table.
        Проверяет, что выполняются правильные SQL-запросы для очистки таблицы и что транзакция коммитится.
        """
        table_name = 'test_table'

        self.changer.clear_table(table_name)

        cursor_calls = [
            call.execute("SET FOREIGN_KEY_CHECKS = 0"),
            call.execute(f"TRUNCATE TABLE {table_name}"),
            call.execute("SET FOREIGN_KEY_CHECKS = 1")
        ]

        self.changer.cursor.assert_has_calls(cursor_calls, any_order=False)
        self.changer.conn.commit.assert_called_once()

    def test_replace_table_data(self):
        """
        Тестирует метод replace_table_data.
        Проверяет, что таблица очищается и данные заменяются правильным образом.
        """
        table_name = 'test_table'
        count = 5

        self.changer.clear_table = MagicMock()
        self.changer.get_method_lambda = MagicMock(return_value=lambda count: None)

        self.changer.replace_table_data(table_name, count)

        self.changer.clear_table.assert_called_once_with(table_name)
        self.changer.get_method_lambda.assert_called_once_with(table_name)
        self.changer.get_method_lambda(table_name)(count)

    def test_get_method_lambda(self):
        """
        Тестирует метод get_method_lambda.
        Проверяет, что возвращается корректный метод для указанного имени таблицы.
        """
        method = self.changer.get_method_lambda('menu')
        self.assertTrue(callable(method))

        # Проверка вызова правильного метода
        self.changer.PushGenerateMenuData = MagicMock()
        method(10)
        self.changer.PushGenerateMenuData.assert_called_once_with(10)

    def test_execute_query(self):
        """
        Тестирует метод execute_query.
        Проверяет, что запрос выполняется и возвращает корректные данные.
        """
        query = "SELECT * FROM test_table"
        self.changer.cursor.execute = MagicMock()
        self.changer.cursor.fetchall = MagicMock(return_value=[('row1',), ('row2',)])

        result = self.changer.execute_query(query)

        self.changer.cursor.execute.assert_called_once_with(query)
        self.changer.cursor.fetchall.assert_called_once()
        self.assertEqual(result, [('row1',), ('row2',)])

    def test_execute_query_with_exception(self):
        """
        Тестирует метод execute_query с исключением.
        Проверяет, что при возникновении исключения метод возвращает None.
        """
        query = "SELECT * FROM test_table"
        self.changer.cursor.execute = MagicMock(side_effect=Exception('Test Exception'))

        result = self.changer.execute_query(query)

        self.changer.cursor.execute.assert_called_once_with(query)
        self.assertIsNone(result)

    def test_get_max_id(self):
        """
       Тестирует метод get_max_id.
       Проверяет, что возвращается максимальный ID из указанной таблицы.
       """
        table_name = 'test_table'
        self.changer.cursor.execute = MagicMock()
        self.changer.cursor.fetchone = MagicMock(return_value=(10,))

        result = self.changer.get_max_id(table_name)

        self.changer.cursor.execute.assert_called_once_with(f"SELECT MAX(id) FROM {table_name}")
        self.changer.cursor.fetchone.assert_called_once()
        self.assertEqual(result, 10)

    def test_get_max_id_with_none(self):
        """
        Тестирует метод get_max_id, когда максимальный ID отсутствует.
        Проверяет, что метод возвращает 0 в этом случае.
        """
        table_name = 'test_table'
        self.changer.cursor.execute = MagicMock()
        self.changer.cursor.fetchone = MagicMock(return_value=(None,))

        result = self.changer.get_max_id(table_name)

        self.changer.cursor.execute.assert_called_once_with(f"SELECT MAX(id) FROM {table_name}")
        self.changer.cursor.fetchone.assert_called_once()
        self.assertEqual(result, 0)

    def test_get_max_id_with_exception(self):
        """
        Тестирует метод get_max_id с исключением.
        Проверяет, что при возникновении исключения метод возвращает 0.
        """
        table_name = 'test_table'
        self.changer.cursor.execute = MagicMock(side_effect=Exception('Test Exception'))

        result = self.changer.get_max_id(table_name)

        self.changer.cursor.execute.assert_called_once_with(f"SELECT MAX(id) FROM {table_name}")
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
