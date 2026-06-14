class HistoryStack:
    """Стек для хранения истории вопросов"""

    def __init__(self):
        self.stack = []

    def push(self, item):
        """Добавление элемента в стек"""
        self.stack.append(item)

    def pop(self):
        """Удаление и возврат последнего элемента"""
        if not self.is_empty():
            return self.stack.pop()
        return None

    def peek(self):
        """Вывод последнего элемента без удаления"""
        if not self.is_empty():
            return self.stack[-1]
        return None

    def is_empty(self):
        """Проверка, пуст ли стек"""
        return len(self.stack) == 0

    def clear(self):
        """Очистка стека"""
        self.stack = []

    def size(self):
        """Возврат размера стека"""
        return len(self.stack)
