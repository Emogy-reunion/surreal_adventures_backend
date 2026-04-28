from core.routes.authentication import auth
from core.routes.destinations import dest_bp


def register_blueprints(app):
    '''
    registers the applications blueprints with the
    '''
    app.register_blueprint(auth, url_prefix="/api/v1")
    app.register_blueprint(dest_bp, url_prefix="/api/v1")

