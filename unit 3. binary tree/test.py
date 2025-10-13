import unittest
from main import gen_bin_tree


class TestBinTree(unittest.TestCase):

    def test_height_zero(self):
        """Тест для высоты 0 - должно вернуть None"""
        result = gen_bin_tree(height=0)
        self.assertIsNone(result)

    def test_height_negative(self):
        """Тест для отрицательной высоты - должно вернуть None"""
        result = gen_bin_tree(height=-1)
        self.assertIsNone(result)

    def test_height_one(self):
        """Тест для высоты 1 - только корень"""
        result = gen_bin_tree(height=1, root=5)
        expected = {
            'root': 5,
            'left': None,
            'right': None
        }
        self.assertEqual(result, expected)

    def test_height_two(self):
        """Тест для высоты 2"""
        result = gen_bin_tree(height=2, root=3)

        # Проверяем корень
        self.assertEqual(result['root'], 3)

        # Проверяем, что есть левое и правое поддеревья
        self.assertIsNotNone(result['left'])
        self.assertIsNotNone(result['right'])

        # Проверяем значения потомков
        self.assertEqual(result['left']['root'], 3 ** 3)  # 27
        self.assertEqual(result['right']['root'], (3 * 2) - 1)  # 5

        # Проверяем, что потомки являются листьями (нет своих детей)
        self.assertIsNone(result['left']['left'])
        self.assertIsNone(result['left']['right'])
        self.assertIsNone(result['right']['left'])
        self.assertIsNone(result['right']['right'])

    def test_default_parameters(self):
        """Тест с параметрами по умолчанию"""
        result = gen_bin_tree()

        # Проверяем корень по умолчанию
        self.assertEqual(result['root'], 12)

        # Проверяем, что дерево имеет правильную структуру (высота 4)
        self.assertIsNotNone(result['left'])
        self.assertIsNotNone(result['right'])

        # Проверяем значения непосредственных потомков
        self.assertEqual(result['left']['root'], 12 ** 3)  # 1728
        self.assertEqual(result['right']['root'], (12 * 2) - 1)  # 23

    def test_large_height(self):
        """Тест с большой высотой (проверка рекурсии)"""
        result = gen_bin_tree(height=5, root=1)

        # Проверяем, что дерево построено без ошибок
        self.assertIsNotNone(result)
        self.assertIsNotNone(result['left'])
        self.assertIsNotNone(result['right'])

        # Проверяем глубину дерева
        # Левый потомок левого потомка...
        left_left = result['left']['left']
        self.assertIsNotNone(left_left)


if __name__ == '__main__':
    unittest.main()
