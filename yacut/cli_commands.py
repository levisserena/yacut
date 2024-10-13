import click

from . import app, db
from .constants import Text as t
from .models import URLMap  # noqa: F401


@app.cli.command('create_db')
def create_db():
    """Создает все не созданные таблицы базы данных."""
    try:
        with app.app_context():
            db.create_all()
        click.echo(t.CREATE)
    except Exception as error:
        click.echo(t.ERROR.format(error))
