class QuestionStats:
    """Статистика эффективности вопросов"""

    def __init__(self):
        self.success_count = {}
        self.total_count = {}

    def record_success(self, question):
        """Записывает, что вопрос помог угадать"""
        self.success_count[question] = self.success_count.get(question, 0) + 1

    def record_usage(self, question):
        """Записывает использование вопроса"""
        self.total_count[question] = self.total_count.get(question, 0) + 1

    def get_effectiveness(self, question):
        """Возвращает эффективность вопроса (0-1)"""
        if question not in self.total_count or self.total_count[question] == 0:
            return 0
        return self.success_count.get(question, 0) / self.total_count[question]

    def get_best_questions(self, limit=5):
        """Возвращает limit лучших вопросов по эффективности"""
        questions = list(self.total_count.keys())
        if not questions:
            return []

        # Сортировка
        items = [(q, self.get_effectiveness(q)) for q in questions]
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i][1] < items[j][1]:
                    items[i], items[j] = items[j], items[i]

        return [q for q, _ in items[:limit]]

    def calculate_average_depth(self, depths_history):
        """Вычисляет среднюю глубину вопросов (префиксные суммы)"""
        if not depths_history:
            return 0

        prefix_sums = [0]
        for d in depths_history:
            prefix_sums.append(prefix_sums[-1] + d)

        # Среднее
        total = prefix_sums[-1]
        return total / len(depths_history)
