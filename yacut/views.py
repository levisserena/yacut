from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_sort_link

TEXT_UNIQUE_ORIGINAL = ('Такой адрес уже есть.'
                        'Короткая ссылка: {host_url}{short}/')
TEXT_UNIQUE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'
TEXT_MAX_LENGTH_LINK = 'Короткая ссылка не должна быть длиннее {} символов.'
TEXT_RESPONSE = '{host_url}{short}'
TEXT_CATEGORY_CREATE = 'create'
TEXT_CATEGORY_FOUND = 'found'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Представление главной страницы."""
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data if form.custom_id.data else get_sort_link()
        host_url = request.host_url
        if (url_map := URLMap.filter_original(original)) is not None:
            short = url_map.short
            category = TEXT_CATEGORY_FOUND
        else:
            db.session.add(URLMap(original=original, short=short))
            db.session.commit()
            category = TEXT_CATEGORY_CREATE
        flash(TEXT_RESPONSE.format(host_url=host_url, short=short), category)
    return render_template('index.html', form=form)


@app.route('/<string:short>/', strict_slashes=False)
def redirect_from_short_to_original(short):
    """Обрабатывает запросы с короткими ссылками - перенаправляет на
    оригинальный адрес."""
    if not (url_map := URLMap.filter_short(short)):
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
