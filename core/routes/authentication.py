from flask import Blueprint, request, jsonify
from core.models import Users
from core.forms import RegistrationForm, LoginForm
from core.extensions import db
from werkzeug.datastructures import MultiDict
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies
import uuid


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



@auth.route('/login', methods=['POST'])
def login():
    '''
    authenticates the users
    checks if the user has a registered account
    Ensures the user's password matches the stored password
    return:
        errors: form errors (invalid email format)
        error: if an error occurs
        success: successful login
    '''

    try:
        json_data = request.get_json() or {}
        form = LoginForm(formData=MultiDict(json_data))

        if not form.validate():
            return ({'errors': form.errors}), 400

        email = form.email.data.strip().lower()
        password = form.password.data

        user = Users.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": 'Invalid login credentials!'}), 400

        else:
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            response = jsonify({'success': 'Logged in successfully. Enjoy the experience!'})
            response.status_code = 200
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
    except Exception as e:
        return jsonify({"error": 'An unexpected error occurred. Please try again!'}), 500


@auth.route('/refresh_token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    '''
    Create a new access token
    return:
        new access token
    '''

    try:
        user_id = uuid.UUID((get_jwt_identity()))

        # check if user still exists
        user = Users.query.get(user_id)
        if not user:
            return jsonify({"error": "Invalid token"}), 401

        access_token = create_access_token(identity=str(user_id))
        response = jsonify({"success": 'Token refreshed successfully!'})
        response.status_code = 200
        set_access_cookies(response, access_token)

        return response

    except ValueError:
        return jsonify({"error": "Invalid token"}), 40

    except Exception as e:
        return jsonify({"error": 'An unexpected error occurred. Please try again!'}), 500


@auth.route('/logout', methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    '''
    destroys the access tokens by removing the tokens from the cookies
    '''
    try:
        response = jsonify({"success": 'Logged out successfully!'})
        response.status_code = 200
        unset_jwt_cookies(response)
        return response

    except Exception as e:
        return jsonify({"error": 'An unexpected error occurred. Please try again!'}), 500
