import configparser   # библиотека для работы с ini-файлами
import logging # библиотека для логирования (записи событий в файл)
import sys # для exit(1)

# Классы ошибок
class InvalidInputError(Exception):
    """Ошибка: пользователь ввёл не число"""
    pass

class ConfigLoadError(Exception):
    """Ошибка: не удалось загрузить epsilon из файла"""
    pass


# Настройка логгера
logging.basicConfig(
    filename="program.log",  # файл для логов
    level=logging.INFO,      # уровень логов: INFO, WARNING, ERROR
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()


# Функция вычисления
def calculate(operand1, operand2, epsilon):
    """
    Делит operand1 на operand2 с точностью epsilon
    """
    if operand2 == 0:
        logger.error("Ошибка: попытка деления на ноль!")
        return None

    result = operand1 / operand2
    logger.info(f"Деление выполнено: {operand1} / {operand2} = {result}")

    # если epsilon в допустимом диапазоне, округляем
    if 10 ** -9 < epsilon < 10 ** -1:
        multiplier = 1 / epsilon
        result = round(result * multiplier) / multiplier
        logger.info(f"Результат округлён до точности {epsilon}: {result}")
    else:
        logger.warning(f"Значение epsilon ({epsilon}) вне диапазона!")

    return result


# Функция загрузки параметров
def load_params(config_file="settings.ini"):
    """
    Считывает значение epsilon из конфигурационного файла
    """
    config = configparser.ConfigParser()
    logger.info(f"Пробуем прочитать файл {config_file}")

    try:
        config.read(config_file)

        if "SETTINGS" not in config:
            raise ConfigLoadError("В файле нет секции [SETTINGS]")

        epsilon_str = config.get("SETTINGS", "epsilon", fallback=None)
        if epsilon_str is None:
            raise ConfigLoadError("Параметр epsilon отсутствует в файле")

        epsilon = float(epsilon_str)

        if not (10 ** -9 < epsilon < 10 ** -1):
            raise ConfigLoadError(f"Epsilon вне диапазона: {epsilon}")

        logger.info(f"Epsilon успешно загружен из файла: {epsilon}")
        return epsilon

    except ValueError:
        logger.error("Ошибка: значение epsilon не является числом")
        raise ConfigLoadError("Ошибка: значение epsilon должно быть числом")
    except ConfigLoadError as e:
        logger.error(f"Ошибка загрузки epsilon: {e}")
        raise
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при чтении файла: {e}")
        raise ConfigLoadError("Произошла непредвиденная ошибка при чтении файла")


# Основная часть программы
try:
    operand1 = float(input("Введите первый операнд: "))
    operand2 = float(input("Введите второй операнд: "))
except ValueError:
    logger.error("Пользователь ввёл нечисловое значение")
    print("Ошибка: нужно ввести число!")
    sys.exit(1)

# Загружаем epsilon из ini-файла
try:
    epsilon = load_params()
    print(f"Точность (epsilon) из файла: {epsilon}")
except ConfigLoadError as e:
    print("Ошибка: не удалось загрузить параметр epsilon из файла настроек.")
    print("Проверьте, что файл settings.ini существует и содержит строку:")
    print("[SETTINGS]\nepsilon = 0.001")
    logger.error(f"Программа остановлена: {e}")
    sys.exit(1)

# Выполняем деление
result = calculate(operand1, operand2, epsilon)

# Вывод результата
if result is None:
    print("На ноль делить нельзя! >:C")
else:
    print(f"Результат деления: {operand1} / {operand2} = {result}")
