def gen_bin_tree(height=4, root=12):

    # Базовый случай: если высота 0 или меньше, возвращаем None
    if height <= 0:
        return None

    # Вычисляем левого и правого потомка по заданным формулам
    left_value = root ** 3  # root в степени 3
    right_value = (root * 2) - 1  # root умножить на 2, минус 1

    # Рекурсивно строим левое и правое поддеревья
    # Высота уменьшается на 1 для следующих уровней
    left_tree = gen_bin_tree(height - 1, left_value)
    right_tree = gen_bin_tree(height - 1, right_value)

    # Создаем узел дерева в виде словаря
    node = {
        'root': root,
        'left': left_tree,
        'right': right_tree
    }

    return node


def print_tree(tree, level=0): # Выводит дерево
    if tree is None:
        return

    # Отступ для визуализации уровней
    indent = "  " * level

    print(f"{indent}root: {tree['root']}")

    if tree['left'] is not None:
        print(f"{indent}left:")
        print_tree(tree['left'], level + 1)

    if tree['right'] is not None:
        print(f"{indent}right:")
        print_tree(tree['right'], level + 1)


# Основная программа
if __name__ == "__main__":
    print("Бинарное дерево")

    # Создаем дерево с параметрами по умолчанию
    tree1 = gen_bin_tree()
    print("Дерево с параметрами по умолчанию (height=4, root=12):")
    print(tree1)
    print("\nВывод:")
    print_tree(tree1)

