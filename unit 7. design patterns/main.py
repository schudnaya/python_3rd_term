import csv
import json
from abc import ABC, abstractmethod
from typing import Dict, Any

import requests
import yaml


class Component(ABC):
    """
    Базовый интерфейс компонента.
    """

    @abstractmethod
    def operation(self) -> Any:
        """
        Метод получения данных.
        """
        pass

    @abstractmethod
    def save(self, filename: str) -> None:
        """
        Метод сохранения данных в файл.
        """
        pass


class CurrencyComponent(Component):
    """
    Базовый компонент.
    Получает курсы валют в JSON.
    """

    URL = "https://www.cbr-xml-daily.ru/daily_json.js"

    def operation(self) -> Dict[str, Any]:
        """
        Получает данные от API ЦБ РФ.
        """

        response = requests.get(self.URL, timeout=10)

        return response.json()

    def save(self, filename: str) -> None:
        """
        Сохраняет JSON в файл.
        """

        data = self.operation()

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


class Decorator(Component):
    """
    Базовый декоратор.
    """

    def __init__(self, component: Component) -> None:
        self.component = component

    def operation(self) -> Any:
        return self.component.operation()

    def save(self, filename: str) -> None:
        self.component.save(filename)


class YamlDecorator(Decorator):
    """
    Декоратор для YAML.
    """

    def operation(self) -> str:
        """
        Возвращает данные в YAML.
        """

        data = self.component.operation()

        yaml_data = yaml.dump(
            data,
            allow_unicode=True
        )

        return yaml_data

    def save(self, filename: str) -> None:
        """
        Сохраняет YAML в файл.
        """

        yaml_data = self.operation()

        with open(filename, "w", encoding="utf-8") as file:
            file.write(yaml_data)


class CsvDecorator(Decorator):
    """
    Декоратор для CSV.
    """

    def operation(self) -> str:
        """
        Возвращает CSV строку.
        """

        data = self.component.operation()

        result = "CharCode,Name,Value\n"

        for value in data["Valute"].values():
            result += (
                f"{value['CharCode']},"
                f"{value['Name']},"
                f"{value['Value']}\n"
            )

        return result

    def save(self, filename: str) -> None:
        """
        Сохраняет CSV в файл.
        """

        data = self.component.operation()

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                ["CharCode", "Name", "Value"]
            )

            for value in data["Valute"].values():
                writer.writerow(
                    [
                        value["CharCode"],
                        value["Name"],
                        value["Value"]
                    ]
                )


if __name__ == "__main__":

    component = CurrencyComponent()

    print("JSON:")
    print(component.operation())

    yaml_component = YamlDecorator(component)

    print("YAML:")
    print(yaml_component.operation())

    csv_component = CsvDecorator(component)

    print("CSV:")
    print(csv_component.operation())

    component.save("rates.json")
    yaml_component.save("rates.yaml")
    csv_component.save("rates.csv")
