import unittest # библиотека для тестирования
import os # для работы с файлами
from main import calculate, load_params # импортируем функции из программы


class TestDivisionProgram(unittest.TestCase):
    """
    Тесты для программы деления
    """

    def setUp(self):
        """Создаём временный ini-файл перед каждым тестом"""
        self.test_config_file = "test_settings.ini"

    def tearDown(self):
        """Удаляем временный ini-файл после каждого теста"""
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)

    # Тесты для функции calculate

    def test_divide_simple(self):
        """Проверяем простое деление"""
        result = calculate(10, 2, 0.001)
        self.assertEqual(result, 5.0)

    def test_divide_with_rounding(self):
        """Проверяем округление"""
        result = calculate(1, 3, 0.1)
        # 1/3 = 0.3333, округляем до 0.3
        self.assertEqual(result, 0.3)

    def test_divide_by_zero(self):
        """Деление на ноль должно вернуть None"""
        result = calculate(5, 0, 0.001)
        self.assertIsNone(result)

    def test_epsilon_out_of_range(self):
        """Если epsilon слишком большой или маленький — всё равно работает"""
        result1 = calculate(1, 3, 0.5) # слишком большой
        result2 = calculate(1, 3, 0.0000000001) # слишком маленький
        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)


    # Тесты для функции load_params

    def test_load_epsilon_from_file(self):
        """Проверяем, что epsilon читается из файла"""
        with open(self.test_config_file, "w") as f:
            f.write("[SETTINGS]\n")
            f.write("epsilon = 0.001\n")

        eps = load_params(self.test_config_file)
        self.assertEqual(eps, 0.001)

    def test_file_not_found(self):
        """Если файл не найден — возвращается значение по умолчанию"""
        eps = load_params("no_such_file.ini")
        self.assertEqual(eps, 0.0001)

    def test_wrong_format_in_file(self):
        """Если epsilon не число — возвращается 0.0001"""
        with open(self.test_config_file, "w") as f:
            f.write("[SETTINGS]\n")
            f.write("epsilon = not_a_number\n")

        eps = load_params(self.test_config_file)
        self.assertEqual(eps, 0.0001)

    def test_missing_section(self):
        """Если в файле нет секции SETTINGS"""
        with open(self.test_config_file, "w") as f:
            f.write("[OTHER]\n")
            f.write("epsilon = 0.01\n")

        eps = load_params(self.test_config_file)
        self.assertEqual(eps, 0.0001)

    def test_missing_epsilon_param(self):
        """Если epsilon отсутствует"""
        with open(self.test_config_file, "w") as f:
            f.write("[SETTINGS]\n")
            f.write("some_other_param = 123\n")

        eps = load_params(self.test_config_file)
        self.assertEqual(eps, 0.0001)


# запуск всех тестов
if __name__ == "__main__":
    unittest.main()
