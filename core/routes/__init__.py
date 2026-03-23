from core.routes.authentication import auth


def register_blueprints(app):
    '''
    registers the applications blueprints with the
    '''
    app.register_blueprint(auth, url_prefix="/api/v1/auth")
