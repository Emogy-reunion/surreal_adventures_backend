from flask import Flask
from core.config import Config
from core.routes import register_blueprints
from core.extensions import jwt, bcrypt, migrate, db

def create_app():
    '''
    initialize the flask's application instance
    return: the application instance
    '''

    app = Flask(__name__)

    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    import core.models

    register_blueprints(app)

    return app
