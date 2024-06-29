import unittest
from unittest.mock import patch, MagicMock
import timeit
from lib.timer import query_time, generate_time

class TestTimeMeasure(unittest.TestCase):
    """
    Юнит-тесты для измерения времени выполнения функций.
    """

    @patch('timeit.timeit')
    def test_query_time(self, mock_timeit):
        """
        Тестирует функцию query_time для измерения времени выполнения запроса.
        """
        # Arrange
        mock_generation_func = MagicMock()
        mock_timeit.return_value = 1.2345678901
        query = "SELECT * FROM table"

        # Act
        result = query_time(mock_generation_func, query)

        # Assert
        mock_timeit.assert_called_once()
        self.assertEqual(result, '1.2345678901')

    @patch('timeit.timeit')
    def test_generate_time(self, mock_timeit):
        """
        Тестирует функцию generate_time для измерения времени выполнения генерации данных.
        """
        # Arrange
        mock_generation_func = MagicMock()
        mock_generation_func.__name__ = 'mock_generation_func'
        mock_timeit.return_value = 2.3456789012
        mock_model = MagicMock()
        mock_model.__name__ = 'MockModel'
        n = 10
        kwargs = {'param1': 'value1'}

        # Act
        result = generate_time(mock_generation_func, mock_model, n, **kwargs)

        # Assert
        mock_timeit.assert_called_once()
        self.assertEqual(result, '2.3456789012')

if __name__ == '__main__':
    unittest.main()
