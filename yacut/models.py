from datetime import datetime

from flask import request
from sqlalchemy.orm import validates

from settings import (MAX_LENGTH_LINK, MAX_LENGTH_ORIGINAL_LINK,
                      STRING_CHARACTERS)

from . import db

TEXT_VALIDATE_SHORT = ('Короткие ссылки могут быть только из:'
                       'больших и маленьких латинских буквы,'
                       'а так же из цифр в диапазоне от 0 до 9.')


class URLMap(db.Model):
    """Модель для хранения ссылки пользователя и её короткого аналога."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), unique=True,
                         nullable=False)
    short = db.Column(db.String(MAX_LENGTH_LINK), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @validates('short')
    def validate_short(self, key, short):
        if not all([(symbol in STRING_CHARACTERS) for symbol in short]):
            raise ValueError(TEXT_VALIDATE_SHORT)
        return short

    @classmethod
    def filter_short(cls, short):
        """Найдет и вернет экземпляр класса с переданным вариантом короткой
        ссылки."""
        return cls.query.filter_by(short=short).first()

    @classmethod
    def filter_original(cls, original):
        """Найдет и вернет экземпляр класса с переданным вариантом оригинальной
        ссылки."""
        return cls.query.filter_by(original=original).first()

    def to_dict(self):
        return dict(url=self.original,
                    short_link=request.host_url + self.short)

    def from_dict(self, data):
        for field in ('original', 'short'):
            if field in data:
                setattr(self, field, data[field])
