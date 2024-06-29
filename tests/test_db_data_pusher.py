import unittest
from unittest.mock import MagicMock, patch, call
import mysql.connector
from lib.db_data_pusher import DatabaseDataPusher


class TestDatabaseDataPusher(unittest.TestCase):
    """
    Юнит-тесты для класса DatabaseDataPusher.
    """

    def setUp(self):
        """
        Устанавливает начальные условия для тестов.
        Патчит конструктор DatabaseDataPusher, чтобы избежать реального подключения к базе данных,
        и создает экземпляр DatabaseDataPusher с замоканными cursor и conn.
        """
        # Патчинг конструктора DatabaseDataPusher, чтобы избежать реального подключения к базе данных
        with patch('lib.data_generator.DataGenerator'):
            self.pusher = DatabaseDataPusher('host', 'root', '123456', 'db_name', 10)
            self.pusher.conn = MagicMock()
            self.pusher.cursor = MagicMock()

    @patch('mysql.connector.connect')
    def test_enter_exit(self, mock_connect):
        """
        Тестирует методы __enter__ и __exit__.
        Проверяет, что при входе в контекстный менеджер устанавливается соединение с базой данных,
        а при выходе выполняются commit, закрытие курсора и соединения.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        with DatabaseDataPusher('host', 'root', '123456', 'db_name', 10) as pusher:
            # Check that connect was called
            mock_connect.assert_called_once_with(
                host='host', user='root', password='123456', database='db_name'
            )

            # Check that cursor was accessed
            self.assertTrue(mock_conn.cursor.called)

        # After exiting the context manager, check for commit, close, and connection close
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_delete_stored_data(self):
        """
         Тестирует метод DeleteStoredData.
         Проверяет, что выполняется правильный SQL-запрос для удаления данных из таблицы.
        """
        table = 'test_table'
        self.pusher.DeleteStoredData(table)
        self.pusher.cursor.execute.assert_called_once_with(f"DELETE FROM {table};")

    def test_push_data(self):
        """
        Тестирует метод PushData.
        Проверяет, что данные правильно вставляются в таблицу и выполняется commit.
        """
        table = 'test_table'
        data = [MagicMock() for _ in range(5)]
        for entry in data:
            entry.to_turple = MagicMock(return_value=('val1', 'val2'))

        self.pusher.PushData(table, data)

        self.pusher.cursor.executemany.assert_called_once_with(
            f"INSERT INTO {table} VALUES (%s, %s)",
            [entry.to_turple() for entry in data]
        )
        self.pusher.conn.commit.assert_called_once()

    def test_push_generate_data(self):
        """
        Тестирует метод PushGenerateData.
        Проверяет, что все необходимые методы для генерации данных вызываются с правильными аргументами.
        """
        with patch.object(self.pusher, 'PushGenerateMenuData') as mock_menu, \
             patch.object(self.pusher, 'PushGenerateGuestData') as mock_guest, \
             patch.object(self.pusher, 'PushGenerateBaristaData') as mock_barista, \
             patch.object(self.pusher, 'PushGenerateOrderData') as mock_order, \
             patch.object(self.pusher, 'PushGenerateOrdersData') as mock_orders, \
             patch.object(self.pusher, 'PushGenerateOrders_has_orderData') as mock_oho:

            self.pusher.PushGenerateData(5, 5, 5, 5, 5, 5)

            mock_menu.assert_called_once_with(5)
            mock_guest.assert_called_once_with(5)
            mock_barista.assert_called_once_with(5)
            mock_order.assert_called_once_with(5)
            mock_orders.assert_called_once_with(5)
            mock_oho.assert_called_once_with(5)

    def test_push_generate_menu_data(self):
        """
        Тестирует метод PushGenerateMenuData.
        Проверяет, что данные меню правильно генерируются и вставляются в таблицу.
        """
        with patch.object(self.pusher, 'PushData') as mock_push_data:
            self.pusher.data.MenuGenerator = MagicMock(return_value=[MagicMock() for _ in range(5)])

            self.pusher.PushGenerateMenuData(5)

            self.pusher.data.MenuGenerator.assert_called_once_with(5)
            mock_push_data.assert_called_once_with('menu', self.pusher.data.MenuGenerator.return_value)

    def test_push_generate_guest_data(self):
        """
        Тестирует метод PushGenerateGuestData.
        Проверяет, что данные гостей правильно генерируются и вставляются в таблицу.
        """
        with patch.object(self.pusher, 'PushData') as mock_push_data:
            self.pusher.data.GuestGenerator = MagicMock(return_value=[MagicMock() for _ in range(5)])

            self.pusher.PushGenerateGuestData(5)

            self.pusher.data.GuestGenerator.assert_called_once_with(5)
            mock_push_data.assert_called_once_with('guest', self.pusher.data.GuestGenerator.return_value)

    def test_push_generate_barista_data(self):
        """
        Тестирует метод PushGenerateBaristaData.
        Проверяет, что данные бариста правильно генерируются и вставляются в таблицу.
        """
        with patch.object(self.pusher, 'PushData') as mock_push_data:
            self.pusher.data.BaristaGenerator = MagicMock(return_value=[MagicMock() for _ in range(5)])

            self.pusher.PushGenerateBaristaData(5)

            self.pusher.data.BaristaGenerator.assert_called_once_with(5)
            mock_push_data.assert_called_once_with('barista', self.pusher.data.BaristaGenerator.return_value)

    def test_push_generate_order_data(self):
        """
        Тестирует метод PushGenerateOrderData.
        Проверяет, что данные заказа правильно генерируются и вставляются в таблицу.
        """
        with patch.object(self.pusher, 'PushData') as mock_push_data:
            self.pusher.data.OrderGenerator = MagicMock(return_value=[MagicMock() for _ in range(5)])

            self.pusher.PushGenerateOrderData(5)

            self.pusher.data.OrderGenerator.assert_called_once_with(5)
            mock_push_data.assert_called_once_with('personal_order', self.pusher.data.OrderGenerator.return_value)

    def test_push_generate_orders_data(self):
        """
        Тестирует метод PushGenerateOrdersData.
        Проверяет, что данные заказов правильно генерируются и вставляются в таблицу.
        """
        with patch.object(self.pusher, 'PushData') as mock_push_data:
            self.pusher.data.OrdersGenerator = MagicMock(return_value=[MagicMock() for _ in range(5)])

            self.pusher.PushGenerateOrdersData(5)

            self.pusher.data.OrdersGenerator.assert_called_once_with(5)
            mock_push_data.assert_called_once_with('orders', self.pusher.data.OrdersGenerator.return_value)

    def test_push_generate_orders_has_order_data(self):
        """
        Тестирует метод PushGenerateOrders_has_orderData.
        Проверяет, что данные связей заказов правильно генерируются и вставляются в таблицу.
        """
        with patch.object(self.pusher, 'PushData') as mock_push_data:
            self.pusher.GetExistingOrderIDs = MagicMock(return_value=[1, 2, 3])
            self.pusher.data.Orders_has_OrderGenerator = MagicMock(return_value=[MagicMock() for _ in range(5)])

            self.pusher.PushGenerateOrders_has_orderData(5)

            self.pusher.GetExistingOrderIDs.assert_called_once()
            self.pusher.data.Orders_has_OrderGenerator.assert_called_once_with(5, [1, 2, 3])
            mock_push_data.assert_called_once_with('orders_has_order', self.pusher.data.Orders_has_OrderGenerator.return_value)

    def test_get_existing_order_ids(self):
        """
        Тестирует метод GetExistingOrderIDs.
        Проверяет, что правильно извлекаются и возвращаются существующие ID заказов из таблицы.
        """
        self.pusher.cursor.execute = MagicMock()
        self.pusher.cursor.fetchall = MagicMock(return_value=[(1,), (2,), (3,)])

        result = self.pusher.GetExistingOrderIDs()

        self.pusher.cursor.execute.assert_called_once_with("SELECT id FROM orders")
        self.pusher.cursor.fetchall.assert_called_once()
        self.assertEqual(result, [1, 2, 3])

    def test_get_method_lambda(self):
        """
         Тестирует метод get_method_lambda.
         Проверяет, что возвращается корректный метод для указанного имени таблицы.
         """
        method = self.pusher.get_method_lambda('menu')
        self.assertTrue(callable(method))

        with patch.object(self.pusher, 'PushGenerateMenuData') as mock_push_menu:
            method(5)
            mock_push_menu.assert_called_once_with(5)

if __name__ == '__main__':
    unittest.main()
