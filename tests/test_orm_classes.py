import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from lib.orm_classes import Field, IntegerField, CharField, FloatField, ForeignKey, ManyToManyField, Model, ModelMeta


class TestField(unittest.TestCase):
    """
    Юнит-тесты для класса Field.
    """

    def test_field_initialization(self):
        """
        Тестирует инициализацию класса Field.
        """
        field = Field(field_type='INTEGER', primary_key=True, foreign_key='other_table.id', auto_increment=True)
        self.assertEqual(field.field_type, 'INTEGER')
        self.assertTrue(field.primary_key)
        self.assertEqual(field.foreign_key, 'other_table.id')
        self.assertIn('auto_increment', field.constraints)
        self.assertTrue(field.constraints['auto_increment'])


class TestIntegerField(unittest.TestCase):
    """
    Юнит-тесты для класса IntegerField.
    """

    def test_integer_field_initialization(self):
        """
        Тестирует инициализацию класса IntegerField.
        """
        field = IntegerField(primary_key=True, min_value=0, max_value=100)
        self.assertEqual(field.field_type, 'INTEGER')
        self.assertTrue(field.primary_key)
        self.assertEqual(field.constraints['min_value'], 0)
        self.assertEqual(field.constraints['max_value'], 100)


class TestCharField(unittest.TestCase):
    """
    Юнит-тесты для класса CharField.
    """

    def test_char_field_initialization(self):
        """
        Тестирует инициализацию класса CharField.
        """
        field = CharField(max_length=50, primary_key=True, words_count=2)
        self.assertEqual(field.field_type, 'VARCHAR(50)')
        self.assertTrue(field.primary_key)
        self.assertEqual(field.max_length, 50)
        self.assertEqual(field.constraints['words_count'], 2)


class TestFloatField(unittest.TestCase):
    """
    Юнит-тесты для класса FloatField.
    """

    def test_float_field_initialization(self):
        """
        Тестирует инициализацию класса FloatField.
        """
        field = FloatField(primary_key=True, min_value=0.0, max_value=100.0)
        self.assertEqual(field.field_type, 'FLOAT')
        self.assertTrue(field.primary_key)
        self.assertEqual(field.constraints['min_value'], 0.0)
        self.assertEqual(field.constraints['max_value'], 100.0)


class TestForeignKey(unittest.TestCase):
    """
    Юнит-тесты для класса ForeignKey.
    """

    def test_foreign_key_initialization(self):
        """
        Тестирует инициализацию класса ForeignKey.
        """
        field = ForeignKey(to='other_table.id')
        self.assertEqual(field.field_type, 'INTEGER')
        self.assertEqual(field.foreign_key, 'other_table.id')


class TestManyToManyField(unittest.TestCase):
    """
    Юнит-тесты для класса ManyToManyField.
    """

    def test_many_to_many_field_initialization(self):
        """
        Тестирует инициализацию класса ManyToManyField.
        """
        field = ManyToManyField(to='Menu')
        self.assertEqual(field.to, 'Menu')


class TestModelMeta(unittest.TestCase):
    """
    Юнит-тесты для класса ModelMeta.
    """

    def test_model_meta_creation(self):
        """
        Тестирует создание метакласса модели (ModelMeta).
        """
        class TestModel(Model):
            """
            id: IntegerField(primary_key=True)
            name: CharField(max_length=50)
            related_model: ForeignKey(to='RelatedModel')
            related_models: ManyToManyField(to='RelatedModel')
            """

        self.assertIn('id', TestModel._meta['columns'])
        self.assertIn('name', TestModel._meta['columns'])
        self.assertIn('related_model', TestModel._meta['columns'])
        self.assertIn('related_models', [field_name for field_name, _ in TestModel._meta['many_to_many']])


class TestModel(unittest.TestCase):
    """
    Юнит-тесты для класса Model.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        """
        class TestModel(Model):
            """
            id: IntegerField(primary_key=True)
            name: CharField(max_length=50)
            age: IntegerField(min_value=0, max_value=100)
            related_model: ForeignKey(to='RelatedModel')
            related_models: ManyToManyField(to='RelatedModel')
            """
        self.TestModel = TestModel

    def test_model_initialization(self):
        """
        Тестирует инициализацию экземпляра модели.
        """
        instance = self.TestModel(id=1, name='John Doe', age=30)
        self.assertEqual(instance._data['id'], 1)
        self.assertEqual(instance._data['name'], 'John Doe')
        self.assertEqual(instance._data['age'], 30)

    def test_model_invalid_attribute(self):
        """
        Тестирует создание модели с недопустимым атрибутом.
        """
        with self.assertRaises(AttributeError):
            self.TestModel(invalid_field='test')

    @patch('mysql.connector.connect')
    def test_execute_query(self, mock_connect):
        """
        Тестирует выполнение SQL-запроса моделью.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.with_rows = True
        mock_cursor.fetchall.return_value = [(1, 'Джо Уайт')]
        mock_cursor.column_names = ['id', 'name']

        result, columns = self.TestModel.execute_query("SELECT * FROM testmodel WHERE id = %s", (1,))
        self.assertEqual(result, [(1, 'Джо Уайт')])
        self.assertEqual(columns, ['id', 'name'])

    @patch('mysql.connector.connect')
    def test_create_database(self, mock_connect):
        """
        Тестирует создание базы данных.
        """
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        self.TestModel.create_database()
        mock_conn.cursor().execute.assert_called_with("CREATE DATABASE IF NOT EXISTS my_sandbox_database")


if __name__ == '__main__':
    unittest.main()
