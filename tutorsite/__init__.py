import os
from flask import Flask

def create_app(test_config=None):
    # creates and configures flask app using specified options
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'tutorsite.sqlite'),
    )

    # loads instance config if test config not passed
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # makes sure that the instance folder exists
    # instance folder contains files specifically for a certain instance of the application
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # registers the database and blueprints with the app
    from . import db, user, post
    db.init_app(app)
    app.register_blueprint(user.user)
    app.register_blueprint(post.post)
    app.add_url_rule('/', endpoint='index')

    return app
