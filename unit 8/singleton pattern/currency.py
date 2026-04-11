import requests
import time
from xml.etree import ElementTree as ET
from decimal import Decimal
import matplotlib.pyplot as plt

from singleton_metaclass import SingletonMeta


class Currency:
    def __init__(self, code: str, name: str, value: str, nominal: int):
        self.__code = code
        self.__name = name
        self.__nominal = nominal

        # разделяем float
        integer, fraction = value.replace(',', '.').split('.')
        self.__value = (integer, fraction)

    # геттеры
    def get_code(self):
        return self.__code

    def get_name(self):
        return self.__name

    def get_value(self):
        return self.__value

    def get_nominal(self):
        return self.__nominal

    # сеттер
    def set_value(self, value: str):
        integer, fraction = value.replace(',', '.').split('.')
        self.__value = (integer, fraction)

    def __del__(self):
        pass
