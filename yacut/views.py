from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request

from . import app, db
from .constants import Text as t
from .forms import URLMapForm
from .models import URLMap
from .utils import get_sort_link


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
            category = t.CATEGORY_FOUND
        else:
            db.session.add(URLMap(original=original, short=short))
            db.session.commit()
            category = t.CATEGORY_CREATE
        flash(t.RESPONSE.format(host_url=host_url, short=short), category)
    return render_template('index.html', form=form)


@app.route('/<string:short>/', strict_slashes=False)
def redirect_from_short_to_original(short):
    """Обрабатывает запросы с короткими ссылками - перенаправляет на
    оригинальный адрес."""
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
