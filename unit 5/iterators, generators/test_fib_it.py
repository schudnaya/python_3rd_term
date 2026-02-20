from fibonacci_lst import FibonacchiLst


def test_normal_case() -> None:
    result = list(FibonacchiLst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    assert result == [0, 1, 2, 3, 5, 8]


def test_empty_list() -> None:
    result = list(FibonacchiLst([]))
    assert result == []


def test_single_element() -> None:
    result = list(FibonacchiLst([4]))
    assert result == []

    result = list(FibonacchiLst([1]))
    assert result == [1]