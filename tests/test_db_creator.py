import textwrap
import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from mysql.connector import errorcode
from lib.db_creator import DatabaseCreator


class TestDatabaseCreator(unittest.TestCase):
    """
    Юнит-тесты для класса DatabaseCreator.
    """

    @patch('mysql.connector.connect')
    def test_enter_successful_connection(self, mock_connect):
        """
        Тест успешного подключения в методе __enter__.
        Проверяет, что соединение и курсор создаются корректно, и база данных создается.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        with DatabaseCreator('test_db', 'root', '123456', 'localhost') as db_creator:
            self.assertIsNotNone(db_creator.conn)
            self.assertIsNotNone(db_creator.cursor)
            mock_connect.assert_called_once_with(user='root', password='123456', host='localhost')
            mock_conn.cursor.assert_called_once()
            mock_conn.cursor().execute.assert_any_call(
                "CREATE DATABASE IF NOT EXISTS test_db DEFAULT CHARACTER SET 'utf8'")

    @patch('mysql.connector.connect')
    def test_enter_database_already_exists(self, mock_connect):
        """
        Тест обработки ситуации, когда база данных уже существует.
        Проверяет, что ошибка обрабатывается и выполняется повторная попытка создания базы данных.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # Имитация ошибки при первом вызове и успешное выполнение при втором
        mock_cursor.execute.side_effect = [
            mysql.connector.Error(errno=errorcode.ER_BAD_DB_ERROR),
            None
        ]

        with DatabaseCreator('test_db', 'root', '123456', 'localhost') as db_creator:
            self.assertIsNotNone(db_creator.conn)
            self.assertIsNotNone(db_creator.cursor)
            mock_connect.assert_called_once_with(user='root', password='123456', host='localhost')
            mock_conn.cursor.assert_called_once()
            mock_cursor.execute.assert_any_call("CREATE DATABASE IF NOT EXISTS test_db DEFAULT CHARACTER SET 'utf8'")

    @patch('mysql.connector.connect')
    def test_exit(self, mock_connect):
        """
        Тест метода __exit__.
        Проверяет, что курсор и соединение закрываются корректно и изменения коммитятся.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        db_creator = DatabaseCreator('test_db', 'root', '123456', 'localhost')
        db_creator.conn = mock_conn
        db_creator.cursor = mock_cursor
        db_creator.__exit__(None, None, None)

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_create_database(self, mock_connect):
        """
        Тест метода create_database.
        Проверяет, что SQL-запрос для создания базы данных выполняется корректно.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        with DatabaseCreator('test_db', 'root', '123456', 'localhost') as db_creator:
            db_creator.create_database()
            mock_cursor.execute.assert_called_with("CREATE DATABASE IF NOT EXISTS test_db DEFAULT CHARACTER SET 'utf8'")

    @patch('mysql.connector.connect')
    def test_database_creation(self, mock_connect):
        """
        Тест метода Database_Creation.
        Проверяет, что все необходимые SQL-запросы для создания таблиц выполняются корректно.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        with DatabaseCreator('test_db', 'root', '123456', 'localhost') as db_creator:
            db_creator.Database_Creation()
            self.assertEqual(mock_cursor.execute.call_count, 6+1)


if __name__ == '__main__':
    unittest.main()
