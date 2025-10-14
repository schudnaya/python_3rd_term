import configparser # библиотека для работы с конфигурационными файлами

def calculate(operand1, operand2, epsilon=0.0001):
    """
    выполняет деление operand1 на operand2 с заданной точностью epsilon.

    operand1: первый операнд (целое или дробное число)
    operand2: второй операнд (целое или дробное число)
    epsilon: точность (по умолчанию 0.0001)

    возвращает результат деления или None при делении на ноль
    """
    if operand2 == 0:
        return None

    result = operand1 / operand2

    # округляем результат до нужной точности
    if 10 ** -9 < epsilon < 10 ** -1:
        multiplier = 1 / epsilon
        result = round(result * multiplier) / multiplier

    return result


def load_params(config_file='settings.ini'):
    """
    считывает значение точности из конфигурационного файла.

    config_file: путь к конфигурационному файлу

    возвращает значение epsilon из файла или 0.0001 по умолчанию
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    epsilon_str = config.get('SETTINGS', 'epsilon', fallback='0.0001')
    epsilon = float(epsilon_str)

        # проверяем, что epsilon в допустимом диапазоне
    if 10 ** -9 < epsilon < 10 ** -1:
        return epsilon
    else:
        return 0.0001


# ввод операндов
try:
    operand1 = float(input("Введите первый операнд: "))
    operand2 = float(input("Введите второй операнд: "))
except ValueError:
    print("Ошибка: введите числа!")
    exit()

# загрузка точности из конфигурационного файла
epsilon = load_params()
print(f"Точность из файла settings.ini: {epsilon}")

# вычисление результата
result = calculate(operand1, operand2, epsilon)

# вывод результата
if result is None:
    print("На ноль делить нельзя! >:C")
else:
    print(f"Результат деления: {operand1} / {operand2} = {result}")
