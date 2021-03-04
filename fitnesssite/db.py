import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

# creates connection to the database
def get_db():
    # if db is not in g, add it there
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# disconnects from the database
def close_db(e=None):
    # removes db from g
    db = g.pop('db', None)

    if db is not None:
        db.close()

# executes SQL statements in schema.sql, reseting the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# establishes a cli command init-db to initialize the database
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database is initialized.')

def init_app(app):
    app.teardown_appcontext(close_db) # calls after returning response
    app.cli.add_command(init_db_command) # adds new cli command that can be called with flask command