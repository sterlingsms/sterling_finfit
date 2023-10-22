from flask import Blueprint, current_app

finfit_bp = Blueprint('finfit', __name__, url_prefix='/sterling/api/finfit')

from . import views
