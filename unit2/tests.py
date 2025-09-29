import unittest # библиотека для юнит-тестов
import os # для работы с операционной системой (проверка существования файла)

# импортируем функции из основного файла
from main import calculate, load_params


class TestCalculateFunction(unittest.TestCase):
    # Тесты для функции calculate

    def test_division_1_by_2_epsilon_0_1(self):
        # Тест деления 1 на 2 с точностью 0.1
        result = calculate(1, 2, 0.1)
        self.assertEqual(result, 0.5)

    def test_division_1_by_1000_epsilon_0_001(self):
        # Тест деления 1 на 1000 с точностью 0.001
        result = calculate(1, 1000, 0.001)
        self.assertEqual(result, 0.001)

    def test_division_by_zero(self):
        # Тест деления на ноль
        result = calculate(1, 0)
        self.assertIsNone(result)


class TestLoadParamsFunction(unittest.TestCase):
     # Тесты для функции load_params

    def tearDown(self):
        # Выполняется после каждого теста и очищает тестовые файлы
        # Удаляем тестовый файл если он существует
        if os.path.exists('test_settings.ini'):
            os.remove('test_settings.ini')

    def test_file_opening_reading(self):
        # Тест открытия и чтения корректного конфигурационного файла
        # Создаем тестовый конфигурационный файл
        with open('test_settings.ini', 'w') as f:
            f.write('[SETTINGS]\n')
            f.write('epsilon = 0.01\n')

        # Загружаем параметры и проверяем значение
        epsilon = load_params('test_settings.ini')
        self.assertEqual(epsilon, 0.01)

    def test_epsilon_in_valid_range(self):
        # Тест различных значений epsilon на соответствие допустимому диапазону
        test_cases = [
            ('0.01', 0.01),  # В диапазоне (10^-9 < 0.01 < 10^-1)
            ('0.0001', 0.0001),  # В диапазоне (10^-9 < 0.0001 < 10^-1)
            ('0.1', 0.1),  # Граничное значение (близко к верхней границе)
            ('0.000000001', 0.0001),  # Ниже диапазона должно вернуть значение по умолчанию
            ('0.5', 0.0001),  # Выше диапазона должно вернуть значение по умолчанию
        ]

        for epsilon_str, expected in test_cases:
            # Создаем тестовый файл с каждым значением epsilon
            with open('test_settings.ini', 'w') as f:
                f.write('[SETTINGS]\n')
                f.write(f'epsilon = {epsilon_str}\n')

            # Проверяем что функция возвращает ожидаемое значение
            epsilon = load_params('test_settings.ini')
            self.assertEqual(epsilon, expected)

    def test_number_format_in_config_file(self):
        # Тест различных форматов чисел в конфигурационном файле
        test_cases = [
            ('0.001', 0.001),  # десятичный формат
            ('.005', 0.005),  # Формат без начального нуля
            ('1e-3', 0.001),  # Экспоненциальная запись
            ('0.0001', 0.0001),  # Меньшее значение в диапазоне
            ('invalid', 0.0001),  # Невалидный формат должен вернуть значение по умолчанию
        ]

        for epsilon_str, expected in test_cases:
            # Создаем тестовый файл с разными форматами чисел
            with open('test_settings.ini', 'w') as f:
                f.write('[SETTINGS]\n')
                f.write(f'epsilon = {epsilon_str}\n')

            # Проверяем обработку разных форматов
            epsilon = load_params('test_settings.ini')
            self.assertEqual(epsilon, expected)


if __name__ == '__main__':
    # Запуск всех тестов
    unittest.main()
