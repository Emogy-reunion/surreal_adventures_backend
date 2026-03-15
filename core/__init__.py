from flask import Flask


def create_app():
    '''
    initialize the flask's application instance
    return: the application instance
    '''

    app = Flask(__name__)

    return app
