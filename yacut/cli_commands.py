import click

from . import app, db
from .models import URLMap  # noqa: F401

TEXT_CREATE = 'Таблицы базы данных созданы.'
TEXT_ERROR = 'Произошла ошибка:\n{}'


@app.cli.command('create_db')
def create_db():
    """Создает все не созданные таблицы базы данных."""
    try:
        with app.app_context():
            db.create_all()
        click.echo(TEXT_CREATE)
    except Exception as error:
        click.echo(TEXT_ERROR.format(error))
