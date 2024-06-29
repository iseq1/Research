import csv
import json
from lib.db_data_changer import DatabaseDataChanger


class DatabaseBackupRestore(DatabaseDataChanger):
    """
    Класс DatabaseBackupRestore предоставляет функциональность для создания резервных копий и восстановления данных из базы данных.

    Атрибуты:
        Наследует все атрибуты и методы класса DatabaseDataChanger.

    Методы:
        backup_table_data(table_name, file_path, file_format='csv'):
            Создает резервную копию данных из указанной таблицы и сохраняет их в файл.

            Параметры:
                table_name (str): Имя таблицы.
                file_path (str): Путь к файлу для сохранения данных.
                file_format (str): Формат файла ('csv' или 'json').

            Исключения:
                В случае возникновения ошибок при сохранении данных, выводит сообщение об ошибке.

        restore_table_data(table_name, file_path, file_format='csv'):
            Восстанавливает данные в указанной таблице из файла бэкапа.

            Параметры:
                table_name (str): Имя таблицы.
                file_path (str): Путь к файлу с данными для восстановления.
                file_format (str): Формат файла ('csv' или 'json').

            Исключения:
                В случае возникновения ошибок при восстановлении данных, выводит сообщение об ошибке.

    Примечания:
        - Класс наследует функциональность от класса DatabaseDataChanger, который, предоставляет базовые методы для взаимодействия с базой данных.
        - Методы backup_table_data и restore_table_data поддерживают два формата файлов: 'csv' и 'json'.
        - В случае успешного выполнения операций выводят сообщения о завершении операции.
    """

    def backup_table_data(self, table_name, file_path, file_format='csv'):
        """
        Создает резервную копию данных из указанной таблицы и сохраняет их в файл.

        Параметры:
            - table_name (str): Имя таблицы.\n
            - file_path (str): Путь к файлу для сохранения данных.\n
            - file_format (str): Формат файла ('csv' или 'json').

        Исключения:
            - В случае возникновения ошибок при сохранении данных, выводит сообщение об ошибке.

        Примечания:
            - Метод предназначен для создания резервной копии данных из указанной таблицы.
            - Поддерживаемые форматы файлов: 'csv' и 'json'.
            - Если указан формат 'csv', первая строка файла содержит заголовки столбцов.
            - Если указан формат 'json', данные сохраняются в формате JSON.
            - Перед сохранением данных извлекает все строки именованных столбцов из таблицы.
            - В случае успешного сохранения данных выводит сообщение об успешном завершении операции.
        """

        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()

            # Получаем имена столбцов
            column_names = [desc[0] for desc in self.cursor.description]

            if file_format == 'csv':
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(column_names)  # Записываем заголовок
                    writer.writerows(rows)         # Записываем данные

            elif file_format == 'json':
                with open(file_path, mode='w', encoding='utf-8') as file:
                    json_data = [dict(zip(column_names, row)) for row in rows]
                    json.dump(json_data, file, indent=4)

            print(f"Данные из таблицы '{table_name}' успешно сохранены в файл '{file_path}'.")
        except Exception as e:
            print(f"Ошибка при сохранении данных из таблицы '{table_name}':", e)


    def restore_table_data(self, table_name, file_path, file_format='csv'):
        """
        Восстанавливает данные в указанной таблице из файла бэкапа.

        Параметры:
            - table_name (str): Имя таблицы.
            - file_path (str): Путь к файлу с данными для восстановления.
            - file_format (str): Формат файла ('csv' или 'json').

        Исключения:
            - В случае возникновения ошибок при восстановлении данных, выводит сообщение об ошибке.

        Примечания:
            - Метод предназначен для восстановления данных в указанную таблицу из файла бэкапа.
            - Поддерживаемые форматы файлов: 'csv' и 'json'.
            - Если указан формат 'csv', первая строка файла содержит заголовки столбцов.
            - Если указан формат 'json', данные в файле должны быть в формате JSON.
            - Перед восстановлением данных метод очищает указанную таблицу.
            - В случае успешного восстановления данных выводит сообщение об успешном завершении операции.
        """

        try:
            if file_format == 'csv':
                with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    column_names = next(reader)  # Пропускаем заголовок
                    rows = [tuple(row) for row in reader]

            elif file_format == 'json':
                with open(file_path, mode='r', encoding='utf-8') as file:
                    json_data = json.load(file)
                    column_names = json_data[0].keys()
                    rows = [tuple(item.values()) for item in json_data]

            # Очищаем таблицу перед восстановлением данных
            self.clear_table(table_name)

            # Вставляем данные обратно в таблицу
            placeholders = ', '.join(['%s'] * len(column_names))
            columns = ', '.join(column_names)
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.executemany(sql, rows)
            self.conn.commit()

            print(f"Данные из файла '{file_path}' успешно восстановлены в таблице '{table_name}'.")
        except Exception as e:
            print(f"Ошибка при восстановлении данных в таблице '{table_name}':", e)

