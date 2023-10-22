from flask import Blueprint, current_app

sterling_bp = Blueprint('sterling', __name__, url_prefix='/')

from . import views