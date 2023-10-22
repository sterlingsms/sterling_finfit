from flask import jsonify, request, Response
from . import sterling_bp

@sterling_bp.route('/', methods=['GET'])
@sterling_bp.route('/', methods=['GET'])
def home():
    return 'Hello World!'