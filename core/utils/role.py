'''
used to protect routes by enforcing access based controls
'''
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from core.models import Users
from core import db
from flask import jsonify
import uuid


def role_required(*roles):
    '''
    a decorator factory
    takes the role as an argument
    returns a decorator that can be applied to routes
    '''


    def decorator(func):
        '''
        takes the decorated function as an argument
        returns a wrapper that adds role checking logic to the decorated route's function
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''
            runs before the decorated function is accessed
            '''
            user_id = uuid.UUID(get_jwt_identity())

            if not user_id:
                return jsonify({'error': 'Missing or invalid token!'}), 401

            current_user = db.session.get(Users, user_id)

            if not current_user:
                return jsonify({'error': 'User not found!'}), 404

            #SUPERADMIN BYPASS (global access)
            if current_user.role == 'superadmin':
                return func(*args, **kwargs)

            if current_user.role not in roles:
                return jsonify({'error': 'Unauthorized access!'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
