import matplotlib.pyplot as plt
import random


class GraphBuilder:
    """
   Класс для построения графиков с использованием matplotlib.

   Атрибуты:
       - title (str): Заголовок графика.
       - x_label (str): Название оси X.
       - y_label (str): Название оси Y.
       - fig (matplotlib.figure.Figure): Фигура для графика.
       - ax (matplotlib.axes._subplots.AxesSubplot): Ось для графика.
       - lines_styles (list): Список стилей линий для графика.
       - markers (list): Список маркеров для точек на графике.
       - colors (list): Список цветов для линий на графике.
       - line_count (int): Счетчик количества добавленных линий.
   """
    def __init__(self, title, x_label, y_label):
        """
        Инициализирует экземпляр GraphBuilder.

        Параметры:
            - title (str): Заголовок графика.
            - x_label (str): Название оси X.
            - y_label (str): Название оси Y.
        """
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.fig, self.ax = plt.subplots()
        self.lines_styles = ['-', '--', '-.', ':']
        self.markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H']
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        self.line_count = 0

    def add_series(self, x_data, y_data, label):
        """
        Добавляет серию данных на график.

        Параметры:
            - x_data (list): Данные для оси X.
            - y_data (list): Данные для оси Y.
            - label (str): Название графика.
        """
        color = self.colors[self.line_count % len(self.colors)]
        line_style = self.lines_styles[self.line_count % len(self.lines_styles)]
        marker = self.markers[self.line_count % len(self.markers)] if len(x_data) < 10 else None
        self.ax.plot(x_data, y_data, label=label, color=color, linestyle=line_style, marker=marker)
        self.line_count += 1

    def build(self):
        """
        Устанавливает заголовок, метки осей и легенду для графика.
        """
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.ax.legend()

    def save(self, filename, format='png'):
        """
        Сохраняет график в файл.

        Параметры:
            - filename (str): Имя файла для сохранения графика.
            - format (str, optional): Формат файла (по умолчанию 'png').
        """
        self.build()
        self.fig.savefig(filename, format=format)

    def show(self):
        """
        Отображает график на экране.
        """
        self.build()
        plt.show()



