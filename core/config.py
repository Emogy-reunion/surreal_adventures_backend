'''
stores the application's configuration settings
'''
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    IS_PRODUCTION = os.getenv('FLASK_ENV') == 'production' or os.getenv('APP_SETTINGS') == 'production'

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Security  
    JWT_COOKIE_SECURE = IS_PRODUCTION
    JWT_COOKIE_SAMESITE = 'Lax'

    # Location
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'

    # csrf
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'

    SUPER_ADMIN_EMAIL = os.getenv('SUPER_ADMIN_EMAIL')
    SUPER_ADMIN_PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')

    UPLOAD_FOLDER =  os.path.join(BASE_DIR, 'static', 'uploads')
