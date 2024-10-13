from wtforms.validators import ValidationError

from .constants import Text as t, TEN


class Choice:
    """Проверяет строковое поле формы, чтобы все символы были из перечня."""

    def __init__(self, choice=None):
        if choice:
            if not hasattr(choice, '__iter__'):
                raise ValueError(t.ITER_ERROR)
            if any([(type(symbol) is not str) for symbol in choice]):
                raise ValueError(t.TYPE_ERROR)
            self.choice = choice
        else:
            self.choice = [str(symbol) for symbol in range(TEN)]

    def __call__(self, form, field):
        if field.data and not all(
            [(symbol in self.choice) for symbol in field.data]
        ):
            raise ValidationError(t.VALIDATION.format(self.choice))
        return

    def check(self, field):
        return all([(symbol in self.choice) for symbol in field])
