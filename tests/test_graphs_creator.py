import unittest
import os
import matplotlib.pyplot as plt
from lib.graphs_creator import GraphBuilder


class TestGraphBuilder(unittest.TestCase):

    def setUp(self):
        """
        Метод setUp вызывается перед выполнением каждого теста.
        """
        self.graph_builder = GraphBuilder("Название", "Ось Икас", "Ось Игрек")

    def tearDown(self):
        """
        Метод tearDown вызывается после выполнения каждого теста.
        Выполняет очистку и освобождение ресурсов.
        """
        # Удаляем временные файлы, если они были созданы
        if os.path.exists('test_graph.png'):
            os.remove('test_graph.png')

    def test_add_series(self):
        """
        Тест для метода add_series.
        """
        x_data = [1, 2, 3, 4, 5]
        y_data = [5, 4, 3, 2, 1]
        label = "Имя"

        # Вызываем метод add_series
        self.graph_builder.add_series(x_data, y_data, label)

        # Проверяем, что количество линий увеличилось на 1
        self.assertEqual(self.graph_builder.line_count, 1)

    def test_build(self):
        """
        Тест для метода build.
        """
        # Вызываем метод build
        self.graph_builder.build()

        # Проверяем, что заголовок, метки осей и легенда установлены правильно
        self.assertEqual(self.graph_builder.ax.get_title(), "Название")
        self.assertEqual(self.graph_builder.ax.get_xlabel(), "Ось Икас")
        self.assertEqual(self.graph_builder.ax.get_ylabel(), "Ось Игрек")
        self.assertTrue(self.graph_builder.ax.get_legend() is not None)

    def test_save(self):
        """
        Тест для метода save.
        """
        # Добавляем серию данных на график
        self.graph_builder.add_series([1, 2, 3], [3, 2, 1], "Легенда")

        # Сохраняем график в файл
        self.graph_builder.save('test_graph.png')

        # Проверяем, что файл был создан
        self.assertTrue(os.path.exists('test_graph.png'))

    def test_show(self):
        """
        Тест для метода show.
        """
        # Добавляем серию данных на график
        self.graph_builder.add_series([1, 2, 3], [3, 2, 1], "Легенда")

        # Отображаем график на экране (закомментировано, чтобы не вызывать блокировку интерфейса)
        # self.graph_builder.show()

        # Вместо проверки интерактивного отображения, проверим, что метод build вызывается перед отображением
        self.graph_builder.show()
        self.assertTrue(self.graph_builder.ax.get_legend() is not None)


if __name__ == '__main__':
    unittest.main()

