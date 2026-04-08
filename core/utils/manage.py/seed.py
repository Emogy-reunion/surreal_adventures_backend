import click
from core.models import User
from flask import current_app
from core.extensions import db

def create_initial_admin():
    try:
        email = current_app.config['SUPER_ADMIN_EMAIL']
        password = current_app.config['SUPER_ADMIN_PASSWORD']

        if not email or not password:
            raise ValueError("SUPER_ADMIN_EMAIL or SUPER_ADMIN_PASSWORD not set in config.")

        existing_user = db.session.query(User.id).filter_by(email=email).scalar()

        if exiting_user:
            return

        super_admin = User(email=email, password=password, role = 'superadmin')
        db.session.add(super_admin)
        db.session.commit()
            return
    except Exception as e:
        db.session.rollback()
        raise e


@app.cli.command("setup")
def setup():
    """Set up initial admin and upload folder."""
    with app.app_context():
        create_initial_admin()
        click.echo("Super admin created (if not exists) and upload folder ensured.")
