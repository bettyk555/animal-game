from tree import AnimalTree, TreeNode
from history_stack import HistoryStack
from statistics import QuestionStats


class AnimalGame:
    """Основной класс игры"""

    def __init__(self):
        self.tree = AnimalTree()
        self.current_node = None
        self.history = HistoryStack()
        self.stats = QuestionStats()
        self.depths_history = []  # для префиксных сумм
        self.current_depth = 0

    def start_game(self):
        """Начинает новую игру"""
        self.current_node = self.tree.get_root()
        self.history.clear()
        self.current_depth = 0
        print('\n' + '=' * 50)
        print('ЗАГАДАЙ ЖИВОТНОЕ! Я буду задавать вопросы.')
        print('Отвечай "да" или "нет" (можно "д" или "н")')
        print('Если хочешь отменить последний ответ - напиши "назад"')
        print('=' * 50)

    def play_round(self):
        """Один раунд игры"""
        self.start_game()

        while True:
            # Сохраняем текущий узел в историю
            self.history.push(self.current_node)

            if self.current_node.is_leaf():
                # Дошли до животного - делаем предположение
                print(f'\nЯ думаю, это {self.current_node.data}!')
                print(f'Глубина угадывания: {self.current_depth}')
                correct = input('Я угадал? (да/нет): ').strip().lower()

                if correct in ['да', 'д', 'yes', 'y']:
                    print('Ура!')
                    # Записываем успех для последнего вопроса
                    if self.history.size() > 0:
                        last_node = self.history.peek()
                        if last_node and last_node.is_question:
                            self.stats.record_success(last_node.data)
                    self.depths_history.append(self.current_depth)
                    break
                else:
                    # Не угадали - обучение
                    self.learn_new_animal(self.current_node)
                    break
            else:
                # Ещё вопрос
                answer = self.ask_question(self.current_node)

                if answer == 'undo':
                    # Отмена последнего действия
                    if self.history.size() > 1:
                        # Убираем текущий
                        self.history.pop()
                        # Возвращаем предыдущий
                        self.current_node = self.history.pop()
                        self.current_depth -= 1
                        print('\nОтменили последний ответ. Продолжаем...')
                    else:
                        print('Нечего отменять!')
                    continue
                elif answer == 'yes':
                    self.current_node = self.current_node.yes
                elif answer == 'no':
                    self.current_node = self.current_node.no

                self.current_depth += 1

    def learn_new_animal(self, wrong_node):
        """Обучение: добавляем новое животное"""
        print(f'\nОй! Я не угадал :(')
        print(f'Я думал, это {wrong_node.data}')

        correct_animal = input('Какое животное ты загадал? ').strip().lower()

        if correct_animal == wrong_node.data:
            print('Так это же одно и то же!')
            return

        # Просим пользователя задать вопрос
        print(f'\nПридумай вопрос, который отличает {correct_animal} от {wrong_node.data}')
        print('Вопрос должен подразумевать ответ "да" для одного и "нет" для другого')
        new_question = input("Твой вопрос: ").strip()

        # Уточняем, для кого ответ "да"
        print(f'\nДля {correct_animal} ответ на вопрос "{new_question}" будет "да" или "нет"?')
        answer_for_correct = input('да/нет: ').strip().lower()

        # Добавляем в дерево
        self.tree.add_new_animal(wrong_node, wrong_node.data, correct_animal, new_question)
        print(f'\nСпасибо! Теперь я знаю, что {correct_animal} - это {new_question}')
        print('И я запомнил разницу!')

    def show_statistics(self):
        """Показывает статистику игры"""
        print('\n' + '=' * 50)
        print('СТАТИСТИКА ИГРЫ')
        print('=' * 50)

        # Лучшие вопросы
        best = self.stats.get_best_questions(5)
        if best:
            print('\nСамые эффективные вопросы:')
            for i, q in enumerate(best, 1):
                eff = self.stats.get_effectiveness(q) * 100
                print(f'  {i}. {q} (эффективность: {eff:.1f}%)')

        # Средняя глубина (префиксные суммы)
        avg_depth = self.stats.calculate_average_depth(self.depths_history)
        if self.depths_history:
            print(f'\nСредняя глубина угадывания: {avg_depth:.2f} вопросов')
            print(f'Всего сыграно игр: {len(self.depths_history)}')

        print('\n' + '=' * 50)

    def show_all_questions(self):
        """Вывод всех накопленных вопросов"""
        questions = self.tree.get_all_questions()
        print('\n' + '=' * 50)
        print(f'ВСЕ ВОПРОСЫ В БАЗЕ (всего: {len(questions)})')
        print('=' * 50)
        if not questions:
            print('Вопросов пока нет!')
        else:
            for i, q in enumerate(questions, 1):
                # Статистика по вопросу (если есть)
                eff = self.stats.get_effectiveness(q)
                eff_str = f' (эффективность: {eff*100:.0f}%)' if eff > 0 else ''
                print(f'{i}. {q}{eff_str}')
        print('=' * 50)

    def show_all_animals(self):
        """Вывод всех животных в базе"""
        animals = self.tree.get_all_animals()
        animals.sort()
        print('\n' + '=' * 50)
        print(f'ВСЕ ЖИВОТНЫЕ В БАЗЕ (всего: {len(animals)})')
        print('=' * 50)
        if not animals:
            print('Животных пока нет!')
        else:
            for i, a in enumerate(animals, 1):
                print(f'{i}. {a}')
        print('=' * 50)

    def show_tree(self):
        """Вывод полного дерева"""
        self.tree.print_tree()

    def show_info(self):
        """Вывод общей информации"""
        print('\n' + '=' * 50)
        print('СТАТИСТИКА БАЗЫ ЗНАНИЙ')
        print('=' * 50)
        print(f'Животных в базе: {self.tree.count_animals()}')
        print(f'Вопросов в базе: {self.tree.count_questions()}')
        print(f'Сыграно игр: {len(self.depths_history)}')
        if self.depths_history:
            avg_depth = sum(self.depths_history) / len(self.depths_history)
            print(f'Средняя глубина угадывания: {avg_depth:.2f}')
        print('=' * 50)

    def ask_question(self, node):
        """Задаёт вопрос с возможностью просмотра"""
        print(f'\nВопрос: {node.data}')
        print('[Команды: да/нет/назад/вопросы/животные/дерево/инфо]')
        answer = input('Твой ответ: ').strip().lower()

        if answer in ['назад', 'back', 'b']:
            return 'undo'
        elif answer in ['вопросы', 'quest', 'list', 'все вопросы']:
            self.show_all_questions()
            return self.ask_question(node)
        elif answer in ['животные', 'animals', 'звери']:
            self.show_all_animals()
            return self.ask_question(node)
        elif answer in ['дерево', 'tree', 'структура']:
            self.show_tree()
            return self.ask_question(node)
        elif answer in ['инфо', 'info', 'статистика']:
            self.show_info()
            return self.ask_question(node)
        elif answer in ['да', 'д', 'yes', 'y']:
            self.stats.record_usage(node.data)
            return 'yes'
        elif answer in ['нет', 'н', 'no', 'n']:
            self.stats.record_usage(node.data)
            return 'no'
        else:
            print('Пожалуйста, ответь "да" или "нет"')
            return self.ask_question(node)

    def run(self):
        """Запуск игры (основной цикл)"""
        while True:
            self.play_round()

            print('\n' + '-' * 30)
            again = input('Сыграем ещё раз? (да/нет): ').strip().lower()
            if again not in ['да', 'д', 'yes', 'y']:
                break

        self.show_statistics()
        print('\nСпасибо за игру! Возвращайся ещё!')
