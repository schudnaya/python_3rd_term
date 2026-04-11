from currencies_manager import CurrencyManager

if __name__ == "__main__":
    manager = CurrencyManager()

    res = manager.fetch(['R01035', 'R01335', 'R01700J'])
    print(res)

    manager.visualize()
