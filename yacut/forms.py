from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional,
                                ValidationError)

from settings import (MAX_LENGTH_LINK, MAX_LENGTH_ORIGINAL_LINK,
                      STRING_CHARACTERS)

from .models import URLMap
from .validators import Choice

TEXT_ORIGINAL = 'Длинная ссылка'
TEXT_SHORT = 'Ваш вариант короткой ссылки'
TEXT_SUBMIT = 'Создать'

TEXT_REQUIRED = 'Обязательное поле'
TEXT_UNIQUE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'
TEXT_LENGTH_ORIGINAL = ('Длина оригинальной ссылки поддерживается только {} '
                        'символов.')
TEXT_LENGTH_SHORT = 'Длина короткой ссылки поддерживается только {} символов.'
TEXT_URL = 'Проверьте, правильно ли введен URL-адрес.'


class URLMapForm(FlaskForm):
    """В форме поле original обязательное, short - нет."""
    original_link = URLField(
        TEXT_ORIGINAL,
        validators=[
            DataRequired(message=TEXT_REQUIRED),
            Length(
                max=MAX_LENGTH_ORIGINAL_LINK,
                message=TEXT_LENGTH_ORIGINAL.format(MAX_LENGTH_ORIGINAL_LINK)
            ),
            URL(message=TEXT_URL)
        ],
    )
    custom_id = StringField(
        TEXT_SHORT,
        validators=[
            Length(
                max=MAX_LENGTH_LINK,
                message=TEXT_LENGTH_SHORT.format(MAX_LENGTH_LINK)
            ),
            Optional(),
            Choice(STRING_CHARACTERS),
        ],
    )
    submit = SubmitField(TEXT_SUBMIT)

    def validate_custom_id(self, field):
        if field.data and URLMap.filter_short(field.data):
            raise ValidationError(TEXT_UNIQUE_SHORT)
