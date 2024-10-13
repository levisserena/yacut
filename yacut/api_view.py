from http import HTTPStatus
from re import match

from flask import jsonify, request

from settings import FLASK_DEBUG, MAX_LENGTH_LINK, STRING_CHARACTERS

from . import app, db
from .constants import Text as t
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import Choice
from .utils import get_sort_link


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
        raise InvalidAPIUsage(t.MISSING_REQUEST)
    if t.KEY_POST_ORIGINAL_LINK not in data:
        raise InvalidAPIUsage(t.REQUIRED.format(t.KEY_POST_ORIGINAL_LINK))
    if not match(r'^(http|ftp|https):\/\/([\w_-]+\.){1,2}[\w]+.*',
                 data[t.KEY_POST_ORIGINAL_LINK]):
        raise InvalidAPIUsage(t.REGULAR)
    if url_map := URLMap.filter_original(data[t.KEY_POST_ORIGINAL_LINK]):
        raise InvalidAPIUsage(t.UNIQUE)
    if t.KEY_POST_CREATE_ID not in data or not data[t.KEY_POST_CREATE_ID]:
        data[t.KEY_POST_CREATE_ID] = get_sort_link()
    else:
        if URLMap.filter_short(data[t.KEY_POST_CREATE_ID]):
            raise InvalidAPIUsage(t.UNIQUE)
        if len(data[t.KEY_POST_CREATE_ID]) > MAX_LENGTH_LINK or (
            not Choice(STRING_CHARACTERS).check(data[t.KEY_POST_CREATE_ID])
        ):
            raise InvalidAPIUsage(t.CHOICE)
    url_map = URLMap()
    url_map.from_dict({
        'original': data[t.KEY_POST_ORIGINAL_LINK],
        'short': data[t.KEY_POST_CREATE_ID],
    })
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/')
def get_original_link(short):
    """GET-запрос на получение оригинальной ссылки по указанному короткому
    идентификатору."""
    if not (url_map := URLMap.filter_short(short)):
        raise InvalidAPIUsage(t.NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({t.KEY_GET_ORIGINAL_LINK: url_map.original})
