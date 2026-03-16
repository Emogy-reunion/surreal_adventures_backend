from flask import Flask
from core.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQALchemy()

def create_app():
    '''
    initialize the flask's application instance
    return: the application instance
    '''

    app = Flask(__name__)

    app.from_object(Config)
    db.init_app()

    return app
