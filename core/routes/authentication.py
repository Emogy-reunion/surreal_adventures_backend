from flask import Blueprint, request, jsonify
from core.models import Users
from core import db
from werkzeug.datastructures import MultiDict


auth = Blueprint('auth', __name__)


@auth.route("/register", methods=['POST'])
def register():
    '''
    allows users to create accounts
    saves the email and password to the database
    return:
        errors: form errors
        error: on error
        success: on success
    '''
    try:
        json_data = request.get_json() or {}
        form = RegistrationForm(formData=MultiDict(json_data))

        if not form.validate():
            return jsonify({"errors": form.errors}), 400

        email = form.email.data.strip().lower()
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if user:
            return jsonify({'error': 'We couldn’t create your account — this email is already in use.'}), 400
        else:
            new_user = Users(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"success": 'Your account was created successfully. Enjoy your experience.'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500


