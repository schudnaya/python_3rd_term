import unittest
from currencies_manager import CurrencyManager


class TestCurrencies(unittest.TestCase):

    def test_invalid_id(self):
        manager = CurrencyManager()
        result = manager.fetch(['R9999'])

        self.assertEqual(result[-1], {'R9999': None})

    def test_valid_currency(self):
        manager = CurrencyManager()
        result = manager.fetch(['R01035'])

        currency = result[0]
        key = list(currency.keys())[0]
        name, value = currency[key]

        self.assertIsInstance(name, str)

        val = float(".".join(value))
        self.assertTrue(0 < val < 999)


if __name__ == '__main__':
    unittest.main()
