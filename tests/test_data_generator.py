import unittest
from lib.data_generator import DataGenerator
from unittest.mock import patch

class TestDataGenerator(unittest.TestCase):
    """
    Юнит-тесты для класса DataGenerator.
    """

    def test_initialization_with_default_values(self):
        """
        Тест инициализации DataGenerator с значениями по умолчанию.
        Проверяет, что вычисленные и заданные значения назначены корректно.
        """
        generator = DataGenerator(200)
        self.assertEqual(generator.GuestCount, 200)
        self.assertEqual(generator.BaristaCount, 2)  # math.ceil(200 / 100)
        self.assertEqual(generator.MenuCount, 25)
        self.assertEqual(generator.OrderCount, 227)  # 200 + math.ceil(200 / 7.5)
        self.assertEqual(generator.OrdersCount, 200)

    def test_initialization_with_custom_values(self):
        """
        Тест инициализации DataGenerator с значениями по умолчанию.
        Проверяет, что вычисленные и заданные значения назначены корректно.
        """
        generator = DataGenerator(GuestCount=150, BaristaCount=5, MenuCount=30, OrdersCount=180)
        self.assertEqual(generator.GuestCount, 150)
        self.assertEqual(generator.BaristaCount, 5)
        self.assertEqual(generator.MenuCount, 30)
        self.assertEqual(generator.OrdersCount, 180)
        self.assertEqual(generator.OrderCount, 170)  # 150 + math.ceil(150 / 7.5)

    @patch('lib.data_generator.DataGenerator.MenuGenerator')
    @patch('lib.data_generator.DataGenerator.OrderGenerator')
    @patch('lib.data_generator.DataGenerator.OrdersGenerator')
    @patch('lib.data_generator.DataGenerator.Orders_has_OrderGenerator')
    @patch('lib.data_generator.DataGenerator.BaristaGenerator')
    @patch('lib.data_generator.DataGenerator.GuestGenerator')
    def test_data_generator(self, mock_guest_gen, mock_barista_gen, mock_orders_has_order_gen, mock_orders_gen, mock_order_gen, mock_menu_gen):
        """
        Тест метода Data_Generator класса DataGenerator.
        Проверяет корректность генерации данных с использованием моков.
        """
        mock_menu_gen.return_value = ['menu_item1', 'menu_item2']
        mock_order_gen.return_value = ['order1', 'order2']
        mock_orders_gen.return_value = ['orders1', 'orders2']
        mock_orders_has_order_gen.return_value = ['orders_has_order1', 'orders_has_order2']
        mock_barista_gen.return_value = ['barista1', 'barista2']
        mock_guest_gen.return_value = ['guest1', 'guest2']

        generator = DataGenerator(GuestCount=200)
        menu, order, orders_has_order, orders, barista, guest = generator.Data_Generator()

        self.assertEqual(menu, ['menu_item1', 'menu_item2'])
        self.assertEqual(order, ['order1', 'order2'])
        self.assertEqual(orders, ['orders1', 'orders2'])
        self.assertEqual(orders_has_order, ['orders_has_order1', 'orders_has_order2'])
        self.assertEqual(barista, ['barista1', 'barista2'])
        self.assertEqual(guest, ['guest1', 'guest2'])

    def test_invalid_guest_count(self):
        """
        Тест некорректного значения GuestCount.
        Проверяет, что при передаче некорректного типа данных возникает ошибка TypeError.
        """
        with self.assertRaises(TypeError):
            DataGenerator("200")

    def test_invalid_barista_count(self):
        """
        Тест некорректного значения BaristaCount.
        Проверяет, что при передаче некорректного типа данных возникает ошибка TypeError.
        """
        with self.assertRaises(TypeError):
            DataGenerator(200, BaristaCount="5")

    def test_invalid_menu_count(self):
        """
        Тест некорректного значения MenuCount.
        Проверяет, что при передаче некорректного типа данных возникает ошибка TypeError.
        """
        with self.assertRaises(TypeError):
            DataGenerator(200, MenuCount="25")

    def test_invalid_order_count(self):
        """
        Тест некорректного значения OrderCount.
        Проверяет, что при передаче некорректного типа данных возникает ошибка TypeError.
        """
        with self.assertRaises(TypeError):
            DataGenerator(200, OrderCount="227")

    def test_invalid_orders_count(self):
        """
        Тест некорректного значения OrderCount.
        Проверяет, что при передаче некорректного типа данных возникает ошибка TypeError.
        """
        with self.assertRaises(TypeError):
            DataGenerator(200, OrdersCount="200")

if __name__ == '__main__':
    unittest.main()
