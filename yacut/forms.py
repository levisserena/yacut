from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional,
                                ValidationError)

from settings import (MAX_LENGTH_LINK, MAX_LENGTH_ORIGINAL_LINK,
                      STRING_CHARACTERS)

from .constants import Text as t
from .models import URLMap
from .validators import Choice


class URLMapForm(FlaskForm):
    """В форме поле original обязательное, short - нет."""
    original_link = URLField(
        t.ORIGINAL,
        validators=[
            DataRequired(message=t.REQUIRED_),
            Length(
                max=MAX_LENGTH_ORIGINAL_LINK,
                message=t.LENGTH_ORIGINAL.format(MAX_LENGTH_ORIGINAL_LINK)
            ),
            URL(message=t.URL)
        ],
    )
    custom_id = StringField(
        t.SHORT,
        validators=[
            Length(
                max=MAX_LENGTH_LINK,
                message=t.LENGTH_SHORT.format(MAX_LENGTH_LINK)
            ),
            Optional(),
            Choice(STRING_CHARACTERS),
        ],
    )
    submit = SubmitField(t.SUBMIT)

    def validate_custom_id(self, field):
        if field.data and URLMap.filter_short(field.data):
            raise ValidationError(t.UNIQUE_SHORT)
