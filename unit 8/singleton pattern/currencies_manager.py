import time
import requests
from xml.etree import ElementTree as ET
import matplotlib.pyplot as plt

from currency import Currency
from singleton_metaclass import SingletonMeta


class CurrencyManager(metaclass=SingletonMeta):

    def __init__(self, delay: float = 1.0):
        self.__delay = delay
        self.__last_request_time = 0
        self.__currencies = []

    # сеттер delay
    def set_delay(self, delay: float):
        self.__delay = delay

    def get_delay(self):
        return self.__delay

    def get_currencies(self):
        return self.__currencies

    def fetch(self, currencies_ids_lst: list):
        current_time = time.time()

        # контроль частоты
        if current_time - self.__last_request_time < self.__delay:
            raise Exception("Слишком частые запросы")

        response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')

        root = ET.fromstring(response.content)  # XML парсится как дерево :contentReference[oaicite:0]{index=0}

        result = []

        for valute in root.findall("Valute"):
            valute_id = valute.get('ID')

            if valute_id in currencies_ids_lst:
                code = valute.find('CharCode').text
                name = valute.find('Name').text
                value = valute.find('Value').text
                nominal = int(valute.find('Nominal').text)

                currency = Currency(code, name, value, nominal)

                result.append({code: (name, currency.get_value())})
                self.__currencies.append(currency)

        # если не найдено
        for cur_id in currencies_ids_lst:
            if not any(cur_id in str(r) for r in result):
                result.append({cur_id: None})

        self.__last_request_time = current_time
        return result

    def visualize(self):
        names = []
        values = []

        for currency in self.__currencies:
            names.append(currency.get_code())
            val = float(".".join(currency.get_value()))
            values.append(val)

        plt.figure()
        plt.bar(names, values)

        plt.title("Курсы валют")
        plt.xlabel("Валюта")
        plt.ylabel("Курс")

        plt.savefig("currencies.jpg")
        plt.close()

    def __del__(self):
        pass
