import json
import os


class TreeNode:
    """Узел дерева решений"""
    def __init__(self, data, is_question=True):
        self.data = data
        self.is_question = is_question
        self.yes = None
        self.no = None

    def is_leaf(self):
        return not self.is_question

    def to_dict(self):
        """Преобразование узла в словарь для JSON"""
        return {
            'data': self.data,
            'is_question': self.is_question,
            'yes': self.yes.to_dict() if self.yes else None,
            'no': self.no.to_dict() if self.no else None
        }

    @classmethod
    def from_dict(cls, data_dict):
        """Восстановление узла из словаря"""
        if data_dict is None:
            return None
        node = cls(data_dict['data'], data_dict['is_question'])
        node.yes = cls.from_dict(data_dict['yes'])
        node.no = cls.from_dict(data_dict['no'])
        return node


class AnimalTree:
    """Дерево решений с сохранением в файл"""

    def __init__(self, save_file='data/animals.json'):
        self.save_file = save_file
        self.root = None

        # Пытаемся загрузить сохранённое дерево
        if os.path.exists(save_file):
            self.load()
            print(f'Загружено сохранённое дерево из {save_file}')
        else:
            self.create_initial_tree()
            print('Создано новое дерево с начальными животными')

    def create_initial_tree(self):
        """Создание начального дерева с 4 животными"""
        # Корень - вопрос
        self.root = TreeNode('Живёт в воде?')

        # Ветка 'да'
        self.root.yes = TreeNode('Это рыба?')
        self.root.yes.yes = TreeNode('щука', is_question=False)
        self.root.yes.no = TreeNode('дельфин', is_question=False)

        # Ветка 'нет'
        self.root.no = TreeNode('Ест мясо?')
        self.root.no.yes = TreeNode('тигр', is_question=False)
        self.root.no.no = TreeNode('слон', is_question=False)

    def get_root(self):
        return self.root

    def save(self):
        """Сохранение дерева в JSON файл"""
        # Создаём папку data, если её нет
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)

        with open(self.save_file, 'w', encoding='utf-8') as f:
            json.dump(self.root.to_dict(), f, ensure_ascii=False, indent=2)
        print(f'Дерево сохранено в {self.save_file}')

    def load(self):
        """Загрузка дерева из JSON файла"""
        with open(self.save_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.root = TreeNode.from_dict(data)
        print(f'Дерево загружено из {self.save_file}')

    def add_new_animal(self, wrong_node, wrong_guess, correct_animal, new_question, answer_for_correct='yes'):
        """Добавление нового животного в дерево"""
        # Создаём новый узел-вопрос
        question_node = TreeNode(new_question, is_question=True)

        # Создаём узлы для животных
        correct_node = TreeNode(correct_animal, is_question=False)
        wrong_node_copy = TreeNode(wrong_guess, is_question=False)

        # Распределяем по веткам
        if answer_for_correct == 'yes':
            question_node.yes = correct_node
            question_node.no = wrong_node_copy
        else:
            question_node.yes = wrong_node_copy
            question_node.no = correct_node

        # Заменяем неправильный узел на новый вопрос
        wrong_node.data = new_question
        wrong_node.is_question = True
        wrong_node.yes = question_node.yes
        wrong_node.no = question_node.no

        # Сохраняем изменения
        self.save()

    def print_tree(self, node=None, level=0):
        """Красивый вывод дерева"""
        if node is None:
            node = self.root
            print('\n' + '=' * 60)
            print('ТЕКУЩЕЕ ДЕРЕВО ВОПРОСОВ И ЖИВОТНЫХ')
            print('=' * 60)

        indent = '  ' * level
        if node.is_question:
            print(f'{indent} {node.data}')
            if node.yes:
                print(f'{indent}   ДА → ', end='')
                self.print_tree(node.yes, level + 1)
            if node.no:
                print(f'{indent}   НЕТ → ', end='')
                self.print_tree(node.no, level + 1)
        else:
            print(f'{indent} {node.data}')

        if level == 0:
            print('=' * 60)

    def count_questions(self, node=None):
        """Подсчёт количества вопросов в дереве"""
        if node is None:
            node = self.root
        if node is None:
            return 0
        count = 1 if node.is_question else 0
        if node.yes:
            count += self.count_questions(node.yes)
        if node.no:
            count += self.count_questions(node.no)
        return count

    def count_animals(self, node=None):
        """Подсчёт количества животных в дереве"""
        if node is None:
            node = self.root
        if node is None:
            return 0
        count = 1 if not node.is_question else 0
        if node.yes:
            count += self.count_animals(node.yes)
        if node.no:
            count += self.count_animals(node.no)
        return count

    def get_all_questions(self, node=None, result=None):
        """Возврат списка всех вопросов"""
        if result is None:
            result = []
            node = self.root
        if node is None:
            return result
        if node.is_question:
            result.append(node.data)
        self.get_all_questions(node.yes, result)
        self.get_all_questions(node.no, result)
        return result

    def get_all_animals(self, node=None, result=None):
        """Возврат списка всех животных"""
        if result is None:
            result = []
            node = self.root
        if node is None:
            return result
        if not node.is_question:
            result.append(node.data)
        self.get_all_animals(node.yes, result)
        self.get_all_animals(node.no, result)
        return result
