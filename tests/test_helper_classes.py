import unittest
from lib.helper_classes import Guest, Barista, Orders, Orders_has_Order, Order, Menu

class TestGuest(unittest.TestCase):
    """
    Юнит-тесты для класса Guest.
    """

    def test_initialization(self):
        """
        Тестирует инициализацию класса Guest.
        """
        guest = Guest(1, 'Егоров Егор Егорыч', '+7(910)123-45-67')
        self.assertEqual(guest.ID, 1)
        self.assertEqual(guest.FullName, 'Егоров Егор Егорыч')
        self.assertEqual(guest.ContactNumber, '+7(910)123-45-67')

    def test_to_turple(self):
        """
        Тестирует метод to_turple класса Guest.
        """
        guest = Guest(1, 'Егоров Егор Егорыч', '+7(910)123-45-67')
        self.assertEqual(guest.to_turple(), (1, 'Егоров Егор Егорыч', '+7(910)123-45-67'))

    def test_invalid_id_type(self):
        """
        Тестирует инициализацию класса Guest с некорректным типом ID.
        """
        with self.assertRaises(TypeError):
            guest = Guest('1', 'Егоров Егор Егорыч', '+7(910)123-45-67')

    def test_invalid_fullname_type(self):
        """
        Тестирует инициализацию класса Guest с некорректным типом FullName.
        """
        with self.assertRaises(TypeError):
            guest = Guest(1, 12345, '+7(910)123-45-67')

    def test_invalid_contact_number_type(self):
        """
        Тестирует инициализацию класса Guest с некорректным типом ContactNumber.
        """
        with self.assertRaises(TypeError):
            guest = Guest(1, 'Егоров Егор Егорыч', 1234567)

    def test_missing_arguments(self):
        """
        Тестирует инициализацию класса Guest с недостающими аргументами.
        """
        with self.assertRaises(TypeError):
            guest = Guest(1, 'Егоров Егор Егорыч')

    def test_extra_arguments(self):
        """
        Тестирует инициализацию класса Guest с лишними аргументами.
        """
        with self.assertRaises(TypeError):
            guest = Guest(1, 'Егоров Егор Егорыч', '+7(910)123-45-67', 'доп_параметр')


class TestBarista(unittest.TestCase):
    """
    Юнит-тесты для класса Barista.
    """

    def test_initialization(self):
        """
        Тестирует инициализацию класса Barista.
        """
        barista = Barista(1, 'Егоров Егор Егорыч', 160)
        self.assertEqual(barista.ID, 1)
        self.assertEqual(barista.FullName, 'Егоров Егор Егорыч')
        self.assertEqual(barista.WorkTime, 160)

    def test_to_turple(self):
        """
        Тестирует метод to_turple класса Barista.
        """
        barista = Barista(1, 'Егоров Егор Егорыч', 160)
        self.assertEqual(barista.to_turple(), (1, 'Егоров Егор Егорыч', 160))

    def test_invalid_id_type(self):
        """
        Тестирует инициализацию класса Barista с некорректным типом ID.
        """
        with self.assertRaises(TypeError):
            barista = Barista('1', 'Егоров Егор Егорыч', 160)

    def test_invalid_fullname_type(self):
        """
        Тестирует инициализацию класса Barista с некорректным типом FullName.
        """
        with self.assertRaises(TypeError):
            barista = Barista(1, 55555, 160)

    def test_invalid_contact_number_type(self):
        """
        Тестирует инициализацию класса Barista с некорректным типом WorkTime.
        """
        with self.assertRaises(TypeError):
            barista = Barista(1, 'Егоров Егор Егорыч', '160')

    def test_missing_arguments(self):
        """
        Тестирует инициализацию класса Barista с недостающими аргументами.
        """
        with self.assertRaises(TypeError):
            barista = Barista(1, 'Егоров Егор Егорыч')

    def test_extra_arguments(self):
        """
        Тестирует инициализацию класса Barista с лишними аргументами.
        """
        with self.assertRaises(TypeError):
            barista = Barista(1, 'Егоров Егор Егорыч', 160, 'доп_параметр')


class TestOrders(unittest.TestCase):
    """
    Юнит-тесты для класса Orders.
    """

    def test_initialization(self):
        """
        Тестирует инициализацию класса Orders.
        """
        order = Orders(1, '6-16-2024', 5, 5)
        self.assertEqual(order.ID, 1)
        self.assertEqual(order.OrderData, '6-16-2024')
        self.assertEqual(order.BaristaID, 5)
        self.assertEqual(order.GuestID, 5)

    def test_to_turple(self):
        """
        Тестирует метод to_turple класса Orders.
        """
        order = Orders(1, '6-16-2024', 5, 5)
        self.assertEqual(order.to_turple(), (1, '6-16-2024', 5, 5))

    def test_invalid_id_type(self):
        """
        Тестирует инициализацию класса Orders с некорректным типом ID.
        """
        with self.assertRaises(TypeError):
            Orders('1', '6-16-2024', 5, 5)

    def test_invalid_orderdata_type(self):
        """
        Тестирует инициализацию класса Orders с некорректным типом OrderData.
        """
        with self.assertRaises(TypeError):
            Orders(1, 6162024, 5, 5)

    def test_invalid_orderdata_format(self):
        """
        Тестирует инициализацию класса Orders с некорректным форматом OrderData.
        """
        with self.assertRaises(ValueError):
            Orders(1, '2024-6-16', 5, 5)

    def test_invalid_baristaid_type(self):
        """
        Тестирует инициализацию класса Orders с некорректным типом BaristaID.
        """
        with self.assertRaises(TypeError):
            Orders(1, '6-16-2024', '5', 5)

    def test_invalid_guestid_type(self):
        """
        Тестирует инициализацию класса Orders с некорректным типом GuestID.
        """
        with self.assertRaises(TypeError):
            Orders(1, '6-16-2024', 5, '5')

    def test_missing_arguments(self):
        """
        Тестирует инициализацию класса Orders с недостающими аргументами.
        """
        with self.assertRaises(TypeError):
            Orders(1, '6-16-2024', 5)

    def test_extra_arguments(self):
        """
        Тестирует инициализацию класса Orders с лишними аргументами.
        """
        with self.assertRaises(TypeError):
            Orders(1, '6-16-2024', 5, 5, 'extra_argument')


class TestOrders_has_order(unittest.TestCase):
    """
    Юнит-тесты для класса Orders_has_Order.
    """

    def test_initialization(self):
        """
        Тестирует инициализацию класса Orders_has_Order.
        """
        oho = Orders_has_Order(1, 1, 1)
        self.assertEqual(oho.ID, 1)
        self.assertEqual(oho.OrderID, 1)
        self.assertEqual(oho.OrdersID, 1)

    def test_to_turple(self):
        """
        Тестирует метод to_turple класса Orders_has_Order.
        """
        oho = Orders_has_Order(1, 1, 1)
        self.assertEqual(oho.to_turple(), (1, 1, 1))

    def test_invalid_id_type(self):
        """
        Тестирует инициализацию класса Orders_has_Order с некорректным типом ID.
        """
        with self.assertRaises(TypeError):
            oho = Orders_has_Order('1', 1, 1)

    def test_invalid_order_id_type(self):
        """
        Тестирует инициализацию класса Orders_has_Order с некорректным типом OrderID.
        """
        with self.assertRaises(TypeError):
            oho = Orders_has_Order(1, '1', 1)

    def test_invalid_orders_id_type(self):
        """
        Тестирует инициализацию класса Orders_has_Order с некорректным типом OrdersID.
        """
        with self.assertRaises(TypeError):
            oho = Orders_has_Order(1, 1, '1')

    def test_missing_arguments(self):
        """
        Тестирует инициализацию класса Orders_has_Order с недостающими аргументами.
        """
        with self.assertRaises(TypeError):
            menu = Menu(1, 'Latte')

    def test_extra_arguments(self):
        """
          Тестирует инициализацию класса Orders_has_Order с лишними аргументами.
          """
        with self.assertRaises(TypeError):
            menu = Menu(1, 'Latte', 1, 'доп_параметр')


if __name__ == '__main__':
    unittest.main()
