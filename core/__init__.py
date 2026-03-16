from flask import Flask
from core.config import Config


def create_app():
    '''
    initialize the flask's application instance
    return: the application instance
    '''

    app = Flask(__name__)

    app.from_object(Config)

    return app
