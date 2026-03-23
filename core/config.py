'''
stores the application's configuration settings
'''
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Security  
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = 'Lax'

    # Location
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_REFRESH_COOKIE_NAME = 'refresh_token_cookie'

    # csrf
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
