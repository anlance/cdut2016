from flask import Blueprint

bp = Blueprint('news_cdut', __name__)

from app.news_cdut import  routes, models



