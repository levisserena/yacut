from wtforms.validators import ValidationError


class Choice:
    """Проверяет строковое поле формы, чтобы все символы были из перечня."""

    TEXT_ITER_ERROR = 'Переданный перечень не итерируемый объект.'
    TEXT_TYPE_ERROR = 'Переданный перечень содержит элементы не строка.'
    TEXT_VALIDATION = 'Символы не соответствуют перечню доступных: {}'

    def __init__(self, choice=None):
        if choice:
            if not hasattr(choice, '__iter__'):
                raise ValueError(self.TEXT_ITER_ERROR)
            if any([(type(symbol) is not str) for symbol in choice]):
                raise ValueError(self.TEXT_TYPE_ERROR)
            self.choice = choice
        else:
            self.choice = [str(symbol) for symbol in range(10)]

    def __call__(self, form, field):
        if field.data and not all(
            [(symbol in self.choice) for symbol in field.data]
        ):
            raise ValidationError(self.TEXT_VALIDATION.format(self.choice))
        return

    def check(self, field):
        if all([(symbol in self.choice) for symbol in field]):
            return True
        else:
            return False
