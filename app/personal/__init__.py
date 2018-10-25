from flask import Blueprint

bp = Blueprint('personal', __name__)

from app.personal import form, routes
