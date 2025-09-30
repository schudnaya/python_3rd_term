import unittest  # библиотека для написания и запуска тестов
import configparser  # библиотека для работы с конфигурационными файлами (читает settings.ini)
import os  # библиотека для работы с оперционной системой (файлы, папки)

# импортируем фукнции из нашей программы
def calculate(operand1, operand2, epsilon=0.0001):
    """
    Функция деления двух чисел с заданной точностью
    """
    if operand2 == 0:  # проверяем деление на ноль
        return None  # возвращаем None если делим на ноль

    result = operand1 / operand2  

    # применяем округление если epsilon в допустимом диапазоне
    if 10 ** -9 < epsilon < 10 ** -1:
        multiplier = 1 / epsilon  # вычисляем множитель для округления
        result = round(result * multiplier) / multiplier  # округляем результат

    return result 

def load_params(config_file='settings.ini'):
    """
    Функция загрузки параметров из конфигурационного файла
    """
    try:
        config = configparser.ConfigParser()  # создаем объект для чтения конфигов
        config.read(config_file)  # читаем файл конфигурации

        # получаем значение epsilon из файла, если нет - используем 0.0001
        epsilon_str = config.get('SETTINGS', 'epsilon', fallback='0.0001')
        epsilon = float(epsilon_str)  # преобразуем строку в число

        # проверяем что epsilon в допустимом диапазоне
        if 10 ** -9 < epsilon < 10 ** -1:
            return epsilon  # возвращаем epsilon из файла
        else:
            return 0.0001  # возвращаем по умолчанию если не в диапазоне

    except (FileNotFoundError, ValueError, configparser.Error):
        return 0.0001  # если ошибка, то возвращаем значение по умолчанию

class TestDivisionProgram(unittest.TestCase):
    """
    Класс для тестирования программы деления
    наследуется от unittest.TestCase чтобы использовать функции тестирования
    """
    
    def setUp(self):
        """
        Метод выполняется перед каждым тестом
        Подготавливаем данные для тестов
        """
        # Создаем временный конфиг файл для тестов
        self.test_config_file = 'test_settings.ini'  # имя временного файла
        
    def tearDown(self):
        """
        Этот метод выполняется после КАЖДОГО теста
        Здесь очищаем данные после тестов
        """
        # Удаляем временный файл если он существует
        if os.path.exists(self.test_config_file):
            os.remove(self.test_config_file)  # удаляем файл
    
    # ТЕСТЫ ДЛЯ ФУНКЦИИ calculate()
    
    def test_divide_1_by_2_with_epsilon_0_1(self):
        """Тест: 1 / 2 с epsilon = 0.1 должен вернуть 0.5"""
        result = calculate(1, 2, 0.1)  # вызываем функцию calculate
        self.assertEqual(result, 0.5)  # проверяем что результат равен 0.5
    
    def test_divide_1_by_1000_with_epsilon_0_001(self):
        """Тест: 1 / 1000 с epsilon = 0.001 должен вернуть 0.001"""
        result = calculate(1, 1000, 0.001)  # делим 1 на 1000
        self.assertEqual(result, 0.001)  # проверяем что результат 0.001
    
    def test_divide_by_zero(self):
        """Деление на ноль должно возвращать None"""
        result = calculate(5, 0)  # пробуем делить на ноль
        self.assertIsNone(result)  # проверяем что вернулся None
    
    # ТЕСТЫ ДЛЯ ФУНКЦИИ load_params()
    
    def test_load_epsilon_from_file_success(self):
        """Тест: успешное чтение epsilon из файла"""
        # Создаем тестовый конфиг файл
        with open(self.test_config_file, 'w') as f:  # открываем файл для записи
            f.write('[SETTINGS]\n')  # пишем секцию SETTINGS
            f.write('epsilon = 0.001\n')  # пишем параметр epsilon
        
        # Загружаем параметры из нашего тестового файла
        epsilon = load_params(self.test_config_file)  # вызываем функцию load_params
        self.assertEqual(epsilon, 0.001)  # проверяем что прочиталось правильное значение
    
    def test_epsilon_in_valid_range(self):
        """проврка что epsilon в допустимом диапазоне"""
        # Тестируем граничные значения
        result1 = calculate(1, 3, 0.1)  # верхняя граница диапазона
        result2 = calculate(1, 3, 0.000000001)  # почти нижняя граница диапазона
        
        self.assertIsNotNone(result1)  # проверяем что результат не None
        self.assertIsNotNone(result2)  # проверяем что результат не None
    
    def test_epsilon_out_of_range(self):
        """еpsilon вне диапазона должен использовать округление по умолчанию"""
        # Epsilon слишком маленький (меньше 10^-9)
        result1 = calculate(1, 3, 0.0000000001)
        # Epsilon слишком большой (больше 0.1)  
        result2 = calculate(1, 3, 0.5)
        
        # Оба должны работать, но без округления
        self.assertIsNotNone(result1)  # проверяем что функция работате
        self.assertIsNotNone(result2)  # проверяем что функция работает
    
    def test_file_not_found(self):
        """если файл не найден, используется значение по умолчанию"""
        epsilon = load_params('non_existent_file.ini')  # пробуем прочитать несуществующий файл
        self.assertEqual(epsilon, 0.0001)  # проверяем что вернулось значение по умолчанию
    
    def test_invalid_number_format_in_config(self):
        """неправильный формат числа в конфиг файле"""
        # Создаем файл с неправильным форматом числа
        with open(self.test_config_file, 'w') as f:
            f.write('[SETTINGS]\n')
            f.write('epsilon = not_a_number\n')  # пишем не число а текст
        
        # Должен вернуть значение по умолчанию
        epsilon = load_params(self.test_config_file)  # читаем файл с ошибкой
        self.assertEqual(epsilon, 0.0001)  # проверяем что вернулось значение по умолчанию
    
    def test_missing_epsilon_in_config(self):
        """если epsilon отсутствует в файле"""
        # Создаем файл без параметра epsilon
        with open(self.test_config_file, 'w') as f:
            f.write('[SETTINGS]\n')
            f.write('other_param = 123\n')  # пишем другой параметр
        
        # Должен вернуть значение по умолчанию
        epsilon = load_params(self.test_config_file)  # читаем файл без epsilon
        self.assertEqual(epsilon, 0.0001)  # проверяем что вернулось значение по умолчанию

# запускаем тесты когда запускаем файл
if __name__ == '__main__':
    unittest.main() 
