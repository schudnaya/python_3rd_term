import pytest
from gen_fib import my_genn


def test_fib_positive() -> None:
    # создаём сопрограмму
    gen = my_genn()

    # запускаем
    next(gen)

    # проверяем работу
    assert gen.send(3) == [0, 1, 1]
    assert gen.send(5) == [0, 1, 1, 2, 3]


def test_fib_zero() -> None:
    gen = my_genn()
    next(gen)

    assert gen.send(0) == []


def test_fib_negative() -> None:
    gen = my_genn()
    next(gen)

    with pytest.raises(ValueError):
        gen.send(-1)