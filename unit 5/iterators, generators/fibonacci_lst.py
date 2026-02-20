from typing import Iterable, Iterator, List


def is_fibonacci_number(x: int) -> bool:
    """
    проверяет, является ли число числом Фибоначчи

    N является числом Фибоначчи тогда и только тогда,
    когда 5*N^2 + 4 или 5*N^2 - 4 является полным квадратом
    """

    # отрицательные числа не считаем числами Фибоначчи
    if x < 0:
        return False

    # вспомогательная функция проверяет, является ли число полным квадратом
    def is_square(num: int) -> bool:
        root: int = int(num ** 0.5)
        return root * root == num

    return is_square(5 * x * x + 4) or is_square(5 * x * x - 4)


class FibonacchiLst:
    """
    итератор принимает список чисел,
    и при переборе возвращает те числа,
    которые являются числами Фибоначчи

        list(FibonacchiLst([0,1,2,3,4,5]))
        -> [0,1,2,3,5]
    """

    def __init__(self, data: Iterable[int]) -> None:
        # сохраняем входные данные как список
        self.data: List[int] = list(data)

        # индекс текущего элемента
        self.index: int = 0

    def __iter__(self) -> "FibonacchiLst":
        """
        __iter__ возвращает объект-итератор.
        в этом случае сам объект является итератором
        """
        return self

    def __next__(self) -> int:
        """
        __next__ вызывается при каждой итерации. Он должен вернуть следующее подходящее значение
        или вызвать StopIteration, если данные закончились
        """

        # пока индекс меньше длины списка
        while self.index < len(self.data):

            # берём текущее число
            current_value: int = self.data[self.index]

            # увеличиваем индекс, чтобы не зациклиться
            self.index += 1

            # проверяем является ли число числом Фибоначчи или нет
            if is_fibonacci_number(current_value):
                return current_value

        # если дошли до конца списка, то завершаем итерацию
        raise StopIteration