from http import HTTPStatus
from re import match

from flask import jsonify, request

from settings import FLASK_DEBUG, MAX_LENGTH_LINK, STRING_CHARACTERS

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import Choice
from .utils import get_sort_link

TEXT_MISSING_REQUEST = 'Отсутствует тело запроса'
TEXT_REQUIRED = '"{}" является обязательным полем!'
TEXT_REGULAR = 'Указанный url-адрес не валидный'
TEXT_UNIQUE = 'Предложенный вариант короткой ссылки уже существует.'
TEXT_CHOICE = 'Указано недопустимое имя для короткой ссылки'
TEXT_NOT_FOUND = 'Указанный id не найден'
KEY_GET_ORIGINAL_LINK = 'url'
KEY_POST_ORIGINAL_LINK = 'url'
KEY_POST_CREATE_ID = 'custom_id'


if FLASK_DEBUG and FLASK_DEBUG in (1, '1', True, 'True'):
    @app.route('/api/config/')
    def config_view():
        """Дает доступ ко всем значениям в конфигурации."""
        return jsonify(
            {key: f'{value}' for key, value in app.config.items()}
        ), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def get_short_link():
    """POST-запрос на создание новой короткой ссылки."""
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(TEXT_MISSING_REQUEST)
    if KEY_POST_ORIGINAL_LINK not in data:
        raise InvalidAPIUsage(TEXT_REQUIRED.format(KEY_POST_ORIGINAL_LINK))
    if not match(r'^(http|ftp|https):\/\/([\w_-]+\.){1,2}[\w]+.*',
                 data[KEY_POST_ORIGINAL_LINK]):
        raise InvalidAPIUsage(TEXT_REGULAR)
    if url_map := URLMap.filter_original(data[KEY_POST_ORIGINAL_LINK]):
        raise InvalidAPIUsage(TEXT_UNIQUE)
    if KEY_POST_CREATE_ID not in data or not data[KEY_POST_CREATE_ID]:
        data[KEY_POST_CREATE_ID] = get_sort_link()
    else:
        if URLMap.filter_short(data[KEY_POST_CREATE_ID]):
            raise InvalidAPIUsage(TEXT_UNIQUE)
        if len(data[KEY_POST_CREATE_ID]) > MAX_LENGTH_LINK or (
            not Choice(STRING_CHARACTERS).check(data[KEY_POST_CREATE_ID])
        ):
            raise InvalidAPIUsage(TEXT_CHOICE)
    url_map = URLMap()
    url_map.from_dict({
        'original': data[KEY_POST_ORIGINAL_LINK],
        'short': data[KEY_POST_CREATE_ID],
    })
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/')
def get_original_link(short):
    """GET-запрос на получение оригинальной ссылки по указанному короткому
    идентификатору."""
    if not (url_map := URLMap.filter_short(short)):
        raise InvalidAPIUsage(TEXT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({KEY_GET_ORIGINAL_LINK: url_map.original})
