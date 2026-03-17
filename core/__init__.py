from flask import Flask
from core.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app():
    '''
    initialize the flask's application instance
    return: the application instance
    '''

    app = Flask(__name__)

    app.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(db, app)

    return app
