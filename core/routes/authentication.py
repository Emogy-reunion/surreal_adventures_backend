from flask import Blueprint
from core.models import Users
from core import db


auth = Blueprint(__name__)
